from __future__ import annotations

import json
from dataclasses import replace
from pathlib import Path
from typing import Any, Mapping
from unittest.mock import patch

import pytest

from scripts.paperbot.config import PaperbotConfig, load_config
from scripts.paperbot.daily import run_daily
from scripts.paperbot.github import upsert_paper_issue
from scripts.paperbot.jev import (
  QUESTION_NAME,
  BibliographyContext,
  ContextDocument,
  JevClient,
  JevDecider,
  JevError,
  candidate_document,
  decision_hash,
  fill_missing_abstracts,
)

from tests.paperbot.test_daily import MemoryIssueClient, make_config, record, report


BIBTEX = (
  "@article{ab2025, title={Antibody language models for CDR design}, "
  "author={Smith, A}, year={2025}, abstract={We train antibody language "
  "models to design complementarity determining regions.}, doi={10.1000/ab}}\n"
  "@article{fold2024, title={Protein structure prediction with deep learning}, "
  "author={Jones, B}, year={2024}, abstract={A neural network predicts "
  "protein structures.}, doi={10.1000/fold}}\n"
)


class FakeTransport:
  def __init__(self, responses: list[tuple[int, Any]]) -> None:
    self.responses = list(responses)
    self.requests: list[dict[str, Any]] = []
    self.headers: list[Mapping[str, str]] = []

  def __call__(
    self, url: str, body: bytes, headers: Mapping[str, str], timeout: float
  ) -> tuple[int, bytes, Mapping[str, str]]:
    self.requests.append(json.loads(body))
    self.headers.append(headers)
    status, payload = self.responses.pop(0)
    raw = payload if isinstance(payload, bytes) else json.dumps(payload).encode()
    return status, raw, {"Retry-After": "0"} if status == 429 else {}


def answer(probability: float) -> dict[str, Any]:
  return {
    "model": "jev-1.14.0",
    "answers": {QUESTION_NAME: {"type": "noul", "noul": probability}},
    "usage": {"input_tokens": 100, "output_tokens": 1},
  }


def jev_config(tmp_path: Path, bibtex: str = BIBTEX, **overrides: Any) -> PaperbotConfig:
  base = make_config(tmp_path, bibtex)
  return replace(base, decision_backend="jev", jev_max_workers=1, **overrides)


def decider(config: PaperbotConfig, transport: FakeTransport) -> JevDecider:
  client = JevClient(
    "key", model=config.jev_model, endpoint=config.jev_endpoint,
    transport=transport, sleep=lambda _: None,
  )
  return JevDecider(config, client, BibliographyContext.from_config(config))


def test_repository_config_selects_jev() -> None:
  config = load_config()
  assert config.decision_backend == "jev"
  assert config.decision_threshold == config.jev_accept_threshold
  assert config.jev_endpoint.startswith("https://")


def test_config_rejects_unknown_backend(tmp_path: Path) -> None:
  path = tmp_path / "paperbot.toml"
  path.write_text('[decision]\nbackend = "magic"\n', encoding="utf-8")
  with pytest.raises(ValueError, match="decision backend"):
    load_config(path)


def test_context_ranks_similar_bibliography_and_rejected_papers() -> None:
  context = BibliographyContext(
    [
      ContextDocument("Protein structure prediction", "Folding with deep learning."),
      ContextDocument("Antibody CDR design", "Language models design antibody loops."),
      ContextDocument("Unrelated soil ecology", "Microbes in soil."),
    ],
    [ContextDocument("Antibody purification columns", "Chromatography of antibody.")],
    similar_papers=1,
  )
  state = context.state({"title": "Designing antibody CDR loops", "abstract": "language models"})
  assert [p["title"] for p in state["similar_bibliography_papers"]] == ["Antibody CDR design"]
  assert state["previously_rejected_papers"][0]["title"] == "Antibody purification columns"
  # Every remaining title still conveys the breadth of interests.
  assert set(state["other_bibliography_titles"]) == {
    "Protein structure prediction", "Unrelated soil ecology",
  }


def test_context_respects_token_budget() -> None:
  accepted = [ContextDocument(f"Antibody paper number {i}", "antibody " * 300) for i in range(50)]
  context = BibliographyContext(accepted, max_context_tokens=1500, max_abstract_chars=400)
  state = context.state({"title": "antibody", "abstract": ""})
  assert len(json.dumps(state)) / 4 <= 1500
  assert all(len(p["abstract"]) <= 402 for p in state["similar_bibliography_papers"])


def test_client_retries_rate_limits_and_sends_bearer_token() -> None:
  transport = FakeTransport([(429, {"detail": "slow"}), (200, answer(0.7))])
  client = JevClient(
    "secret", model="jev-1.14.0", endpoint="https://example.test",
    transport=transport, sleep=lambda _: None,
  )
  result = client.ask({"x": 1}, {"q": {"type": "noul"}})
  assert result["answers"][QUESTION_NAME]["noul"] == 0.7
  assert len(transport.requests) == 2
  assert transport.headers[0]["Authorization"] == "Bearer secret"
  assert transport.requests[0]["model"] == "jev-1.14.0"


def test_client_does_not_retry_validation_errors() -> None:
  transport = FakeTransport([(422, {"detail": []})])
  client = JevClient("k", model="m", endpoint="https://e", transport=transport)
  with pytest.raises(JevError, match="422"):
    client.ask({}, {})
  assert len(transport.requests) == 1


def test_client_requires_api_key() -> None:
  with pytest.raises(ValueError, match="TYPESAFE_API_KEY"):
    JevClient("", model="m", endpoint="https://e")


def test_decider_sends_noul_question_with_bibliography_context(tmp_path: Path) -> None:
  config = jev_config(tmp_path)
  transport = FakeTransport([(200, answer(0.9)), (200, {"answers": {}})])
  jev = decider(config, transport)

  scores = jev.score([
    candidate_document(record()),
    {"title": "Broken", "abstract": ""},
  ])

  assert scores == [0.9, None]
  sent = transport.requests[0]
  assert sent["questions"][QUESTION_NAME]["type"] == "noul"
  assert set(sent["questions"][QUESTION_NAME]["criteria"]) == {"true", "false"}
  titles = [p["title"] for p in sent["state"]["similar_bibliography_papers"]]
  titles += sent["state"]["other_bibliography_titles"]
  assert "Antibody language models for CDR design" in titles
  assert sent["state"]["candidate_paper"]["title"] == "A useful paper"
  assert jev.report()["errors"] and jev.report()["served_models"] == ["jev-1.14.0"]


def test_decision_hash_tracks_prompt_settings_not_bibliography(tmp_path: Path) -> None:
  config = jev_config(tmp_path)
  (tmp_path / "other").mkdir()
  other_bib = jev_config(tmp_path / "other", bibtex="")
  assert decision_hash(config) == decision_hash(other_bib)
  assert decision_hash(config) != decision_hash(replace(config, jev_model="jev-1.13.0"))


@pytest.mark.parametrize(("probability", "action"), [(0.5, "below-cutoff"), (0.51, "would-create")])
def test_daily_uses_jev_probability_and_strict_threshold(
  tmp_path: Path, probability: float, action: str
) -> None:
  config = jev_config(tmp_path)
  fetch = report([record()])
  transport = FakeTransport([(200, answer(probability))])

  with patch(
    "scripts.paperbot.daily.load_model",
    side_effect=AssertionError("the Jev backend must not load SPECTER2"),
  ):
    result = run_daily(
      config, fetch.window, dry_run=True, github_token="token",
      fetch_report=fetch, github_client=MemoryIssueClient(),  # type: ignore[arg-type]
      jev_decider=decider(config, transport),
    )

  assert result.candidates[0].action == action
  assert result.candidates[0].score == probability
  assert result.model_hash == decision_hash(config)
  assert result.decision["backend"] == "jev"
  assert result.ok


def test_daily_publishes_jev_accepted_issue(tmp_path: Path) -> None:
  config = jev_config(tmp_path)
  fetch = report([record()])
  client = MemoryIssueClient()

  result = run_daily(
    config, fetch.window, dry_run=False, github_token="token",
    fetch_report=fetch, github_client=client,  # type: ignore[arg-type]
    jev_decider=decider(config, FakeTransport([(200, answer(0.93))])),
  )

  assert result.candidates[0].action == "created"
  assert "**Relevance:** 0.930000" in client.issues[0]["body"]
  assert decision_hash(config) in client.issues[0]["body"]


def test_daily_reports_failed_decisions_without_publishing(tmp_path: Path) -> None:
  config = jev_config(tmp_path)
  fetch = report([record()])
  client = MemoryIssueClient()

  result = run_daily(
    config, fetch.window, dry_run=False, github_token="token",
    fetch_report=fetch, github_client=client,  # type: ignore[arg-type]
    jev_decider=decider(config, FakeTransport([(400, {"detail": "bad"})])),
  )

  assert result.candidates[0].action == "decision-failed"
  assert not client.issues
  assert not result.ok


def test_daily_redecides_open_issues_from_previous_backend(tmp_path: Path) -> None:
  config = jev_config(tmp_path)
  client = MemoryIssueClient()
  current = record()
  upsert_paper_issue(
    client, current, 0.95, "@misc{x}", "lovelace2026", model_hash="specter-hash",  # type: ignore[arg-type]
  )
  fetch = report([])
  transport = FakeTransport([(200, answer(0.2))])

  result = run_daily(
    config, fetch.window, dry_run=False, github_token="token",
    fetch_report=fetch, github_client=client,  # type: ignore[arg-type]
    jev_decider=decider(config, transport),
  )

  assert result.ok
  assert result.stale_open_issues == 1
  assert transport.requests[0]["state"]["candidate_paper"]["abstract"] == current.abstract
  assert "**Relevance:** 0.200000" in client.issues[0]["body"]


def test_daily_fetches_missing_abstracts_before_deciding(tmp_path: Path) -> None:
  config = jev_config(tmp_path)
  fetch = report([record(abstract="")])
  transport = FakeTransport([(200, answer(0.9))])
  looked_up: list[Mapping[str, str]] = []

  def lookup(fields: Mapping[str, str]) -> str:
    looked_up.append(fields)
    return "A fetched abstract about antibodies."

  result = run_daily(
    config, fetch.window, dry_run=True, github_token="token",
    fetch_report=fetch, github_client=MemoryIssueClient(),  # type: ignore[arg-type]
    jev_decider=decider(config, transport), abstract_lookup=lookup,
  )

  assert looked_up[0]["doi"] == "10.1000/new"
  assert transport.requests[0]["state"]["candidate_paper"]["abstract"] == (
    "A fetched abstract about antibodies."
  )
  assert result.decision["abstracts"] == {
    "missing": 1, "reused": 0, "fetched": 1, "unresolved": 0,
  }


def test_fill_missing_abstracts_prefers_known_text_and_tolerates_failures() -> None:
  records = [record(abstract=""), record(doi="10.1000/b", abstract=""), record()]

  def lookup(fields: Mapping[str, str]) -> str:
    raise OSError("offline")

  filled, stats = fill_missing_abstracts(
    records,
    known_abstract=lambda value: "Known." if value.doi == "10.1000/new" else "",
    lookup=lookup,
  )

  assert [value.abstract for value in filled] == ["Known.", "", "A complete abstract."]
  assert filled[0].canonical_id == records[0].canonical_id
  assert stats == {"missing": 2, "reused": 1, "fetched": 0, "unresolved": 1}


def test_daily_aborts_before_writing_when_jev_rejects_the_credential(tmp_path: Path) -> None:
  config = jev_config(tmp_path)
  fetch = report([record(), record(doi="10.1000/b")])
  client = MemoryIssueClient()
  transport = FakeTransport([(401, {"detail": {"error_type": "authentication_error"}})])

  with pytest.raises(JevError, match="401"):
    run_daily(
      config, fetch.window, dry_run=False, github_token="token",
      fetch_report=fetch, github_client=client,  # type: ignore[arg-type]
      jev_decider=decider(config, transport),
    )
  assert not client.issues
  assert len(transport.requests) == 1
