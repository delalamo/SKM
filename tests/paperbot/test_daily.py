from __future__ import annotations

import os
from copy import deepcopy
from datetime import UTC, datetime
from pathlib import Path
from types import SimpleNamespace
from typing import Any
from unittest.mock import patch

import pytest

from scripts.paperbot.config import PaperbotConfig
from scripts.paperbot.cli import main as paperbot_main
from scripts.paperbot.daily import (
  BibliographyIndex,
  _managed_pubmed_ids,
  _prepare_candidates,
  run_daily,
  sync_project_queue,
  write_project_queue,
)
from scripts.paperbot.github import GitHubError, load_managed_issues, upsert_paper_issue
from scripts.paperbot.model import LoadedModel
from scripts.paperbot.records import PaperRecord
from scripts.paperbot.sources import FetchReport, FetchWindow, SourceFailure


class MemoryIssueClient:
  def __init__(self) -> None:
    self.issues: list[dict[str, Any]] = []
    self.comments: dict[int, list[dict[str, Any]]] = {}

  def list_issues(self, *, label: str = "paper") -> list[dict[str, Any]]:
    return deepcopy(self.issues)

  def ensure_label(
    self,
    name: str = "paper",
    *,
    color: str = "1d76db",
    description: str = "Paper reading queue",
  ) -> None:
    return None

  def create_issue(self, *, title: str, body: str) -> dict[str, Any]:
    issue = {
      "number": len(self.issues) + 1,
      "node_id": f"ISSUE_{len(self.issues) + 1}",
      "title": title,
      "body": body,
      "state": "open",
      "html_url": "https://example.test/issue",
      "labels": [{"name": "paper"}, {"name": "AI-generated"}],
      "user": {"login": "github-actions[bot]", "type": "Bot"},
    }
    self.issues.append(issue)
    return deepcopy(issue)

  def update_issue(
    self,
    number: int,
    *,
    title: str | None = None,
    body: str | None = None,
    state: str | None = None,
  ) -> dict[str, Any]:
    issue = self.issues[number - 1]
    if title is not None:
      issue["title"] = title
    if body is not None:
      issue["body"] = body
    if state is not None:
      issue["state"] = state
    return deepcopy(issue)

  def list_comments(self, number: int) -> list[dict[str, Any]]:
    return deepcopy(self.comments.get(number, []))

  def create_comment(self, number: int, body: str) -> dict[str, Any]:
    comment = {"body": body}
    self.comments.setdefault(number, []).append(comment)
    return deepcopy(comment)

  def add_labels(self, number: int, labels: list[str]) -> None:
    return None


def record(*, doi: str = "10.1000/new", abstract: str = "A complete abstract.") -> PaperRecord:
  return PaperRecord(
    source="pubmed",
    source_id="12345" if doi == "10.1000/new" else doi,
    title="A useful paper",
    abstract=abstract,
    authors=("Ada Lovelace",),
    venue="Journal of Fixtures",
    created_at=datetime(2026, 7, 21, tzinfo=UTC),
    updated_at=datetime(2026, 7, 22, tzinfo=UTC),
    doi=doi,
    pmid="12345" if doi == "10.1000/new" else "",
    url=f"https://doi.org/{doi}",
  )


def make_config(tmp_path: Path, bibtex: str) -> PaperbotConfig:
  bibliography = tmp_path / "bibliography.bib"
  bibliography.write_text(bibtex, encoding="utf-8")
  artifacts = tmp_path / "artifacts"
  artifacts.mkdir()
  exceptions = artifacts / "abstract_exceptions.json"
  exceptions.write_text("{}\n", encoding="utf-8")
  return PaperbotConfig(
    bibliography_path=bibliography,
    artifact_dir=artifacts,
    abstract_exceptions_path=exceptions,
  )


def report(records: list[PaperRecord], *, failed: bool = False) -> FetchReport:
  window = FetchWindow.ending_at(datetime(2026, 7, 22, tzinfo=UTC))
  errors = (
    (SourceFailure("arxiv", "page", "unavailable", retryable=True),)
    if failed
    else ()
  )
  return FetchReport(window, tuple(records), errors, {"fixture": len(records)})


@pytest.mark.parametrize(
  ("score", "action"), [(0.800, "below-cutoff"), (0.801, "would-create")]
)
def test_daily_uses_strict_cutoff_and_reports_partial_feed_failure(
  tmp_path: Path, score: float, action: str
) -> None:
  config = make_config(
    tmp_path,
    "@article{other2025, title={Other}, author={Other, A}, year={2025}, "
    "abstract={Other abstract.}, doi={10.1000/other}}\n",
  )
  client = MemoryIssueClient()
  fetch = report([record()], failed=True)
  with (
    patch("scripts.paperbot.daily.check_model", return_value={"model_hash": "model"}),
    patch("scripts.paperbot.daily.load_model", return_value=LoadedModel(None, 0, "model")),
    patch("scripts.paperbot.daily._score", return_value=[score]),
  ):
    result = run_daily(
      config,
      fetch.window,
      dry_run=True,
      github_token="token",
      fetch_report=fetch,
      github_client=client,  # type: ignore[arg-type]
    )

  assert result.candidates[0].action == action
  assert not result.ok
  assert result.feed_errors[0]["source"] == "arxiv"


def test_candidate_key_collision_uses_b_and_known_work_reuses_key(tmp_path: Path) -> None:
  config = make_config(
    tmp_path,
    "@article{lovelace2026, title={Existing work}, author={Ada Lovelace}, "
    "year={2026}, abstract={Existing abstract.}, doi={10.1000/existing}}\n",
  )
  bibliography = BibliographyIndex.load(config.bibliography_path)
  issues = load_managed_issues(MemoryIssueClient())

  collided = _prepare_candidates([record()], bibliography, issues, "model")[0]
  known = _prepare_candidates(
    [record(doi="10.1000/existing")], bibliography, issues, "model"
  )[0]

  assert collided.bibkey == "lovelace2026_B"
  assert known.bibkey == "lovelace2026"
  assert known.known_bib_key == "lovelace2026"


def test_unchanged_candidate_is_not_embedded(tmp_path: Path) -> None:
  config = make_config(
    tmp_path,
    "@article{other2025, title={Other}, author={Other, A}, year={2025}, "
    "abstract={Other abstract.}, doi={10.1000/other}}\n",
  )
  client = MemoryIssueClient()
  current = record()
  bibliography = BibliographyIndex.load(config.bibliography_path)
  prepared = _prepare_candidates(
    [current], bibliography, load_managed_issues(client), "model"
  )[0]
  upsert_paper_issue(
    client,  # type: ignore[arg-type]
    current,
    0.9,
    prepared.bibtex,
    prepared.bibkey,
    model_hash="model",
  )
  fetch = report([current])

  with (
    patch("scripts.paperbot.daily.check_model", return_value={"model_hash": "model"}),
    patch("scripts.paperbot.daily.load_model", return_value=LoadedModel(None, 0, "model")),
    patch("scripts.paperbot.daily._score", return_value=[]) as scorer,
  ):
    result = run_daily(
      config,
      fetch.window,
      dry_run=True,
      github_token="token",
      fetch_report=fetch,
      github_client=client,  # type: ignore[arg-type]
    )

  assert result.candidates[0].action == "unchanged"
  assert scorer.call_args.args[0] == []


def test_daily_limits_pubmed_revision_checks_to_managed_issue_pmids(
  tmp_path: Path,
) -> None:
  config = make_config(
    tmp_path,
    "@article{other2025, title={Other}, author={Other, A}, year={2025}, "
    "abstract={Other abstract.}, doi={10.1000/other}}\n",
  )
  client = MemoryIssueClient()
  current = record()
  bibliography = BibliographyIndex.load(config.bibliography_path)
  prepared = _prepare_candidates(
    [current], bibliography, load_managed_issues(client), "model"
  )[0]
  upsert_paper_issue(
    client,  # type: ignore[arg-type]
    current,
    0.9,
    prepared.bibtex,
    prepared.bibkey,
    model_hash="model",
  )
  window = FetchWindow.ending_at(datetime(2026, 7, 22, tzinfo=UTC))
  empty = FetchReport(window, (), (), {"pubmed": 0})

  with (
    patch("scripts.paperbot.daily.check_model", return_value={"model_hash": "model"}),
    patch("scripts.paperbot.daily.load_model", return_value=LoadedModel(None, 0, "model")),
    patch("scripts.paperbot.daily.fetch_all_sources", return_value=empty) as fetcher,
    patch("scripts.paperbot.daily._score", return_value=[]),
  ):
    run_daily(
      config,
      window,
      dry_run=True,
      github_token="token",
      github_client=client,  # type: ignore[arg-type]
    )

  assert _managed_pubmed_ids(load_managed_issues(client)) == ("12345",)
  assert fetcher.call_args.kwargs["known_pubmed_ids"] == ("12345",)


def test_daily_publishes_issues_without_project_configuration_or_token(
  tmp_path: Path,
) -> None:
  config = make_config(
    tmp_path,
    "@article{other2025, title={Other}, author={Other, A}, year={2025}, "
    "abstract={Other abstract.}, doi={10.1000/other}}\n",
  )
  client = MemoryIssueClient()
  fetch = report([record()])

  with (
    patch("scripts.paperbot.daily.check_model", return_value={"model_hash": "model"}),
    patch("scripts.paperbot.daily.load_model", return_value=LoadedModel(None, 0, "model")),
    patch("scripts.paperbot.daily._score", return_value=[0.9]),
  ):
    result = run_daily(
      config,
      fetch.window,
      dry_run=False,
      github_token="token",
      projects_token="",
      fetch_report=fetch,
      github_client=client,  # type: ignore[arg-type]
    )

  assert result.candidates[0].action == "created"
  assert client.issues[0]["labels"] == [
    {"name": "paper"},
    {"name": "AI-generated"},
  ]


@pytest.mark.parametrize(
  "config_overrides",
  [
    {"project_owner": "delalamo"},
    {"project_number": 1},
  ],
)
def test_daily_rejects_partial_project_configuration(
  tmp_path: Path, config_overrides: dict[str, Any]
) -> None:
  config = make_config(tmp_path, "")
  config = PaperbotConfig(
    bibliography_path=config.bibliography_path,
    artifact_dir=config.artifact_dir,
    abstract_exceptions_path=config.abstract_exceptions_path,
    **config_overrides,
  )

  with pytest.raises(
    ValueError,
    match="PAPER_PROJECT_OWNER and PAPER_PROJECT_NUMBER must be set together",
  ):
    run_daily(
      config,
      report([]).window,
      dry_run=False,
      github_token="token",
    )


def test_daily_requires_project_token_when_project_is_configured(tmp_path: Path) -> None:
  config = make_config(tmp_path, "")
  config = PaperbotConfig(
    bibliography_path=config.bibliography_path,
    artifact_dir=config.artifact_dir,
    abstract_exceptions_path=config.abstract_exceptions_path,
    project_owner="delalamo",
    project_number=1,
  )

  with pytest.raises(
    ValueError,
    match="PROJECTS_TOKEN is required when Project publishing is configured",
  ):
    run_daily(
      config,
      report([]).window,
      dry_run=False,
      github_token="token",
    )


@pytest.mark.parametrize(
  ("project_owner", "project_number", "expected_defer"),
  [
    ("", None, False),
    ("delalamo", 1, True),
  ],
)
def test_daily_cli_only_prepares_project_queue_when_configured(
  tmp_path: Path,
  project_owner: str,
  project_number: int | None,
  expected_defer: bool,
) -> None:
  base = make_config(tmp_path, "")
  config = PaperbotConfig(
    bibliography_path=base.bibliography_path,
    artifact_dir=base.artifact_dir,
    abstract_exceptions_path=base.abstract_exceptions_path,
    project_owner=project_owner,
    project_number=project_number,
  )
  result = SimpleNamespace(to_dict=lambda: {"ok": True}, model_hash="model", ok=True)
  queue_path = tmp_path / "project-queue.json"

  with (
    patch.dict(os.environ, {"GITHUB_TOKEN": "token"}, clear=True),
    patch("scripts.paperbot.cli.load_config", return_value=config),
    patch("scripts.paperbot.cli.GitHubClient", return_value=MemoryIssueClient()),
    patch("scripts.paperbot.cli.run_daily", return_value=result) as daily,
    patch(
      "scripts.paperbot.cli.write_project_queue", return_value={"items": []}
    ) as write_queue,
    patch("scripts.paperbot.cli._print_json"),
  ):
    exit_code = paperbot_main(["daily", "--project-queue", str(queue_path)])

  assert exit_code == 0
  assert daily.call_args.kwargs["defer_project"] is expected_defer
  assert write_queue.called is expected_defer


def test_existing_issue_is_reconciled_when_work_enters_bibliography(
  tmp_path: Path,
) -> None:
  client = MemoryIssueClient()
  current = record()
  empty_config = make_config(
    tmp_path,
    "@article{other2025, title={Other}, author={Other, A}, year={2025}, "
    "abstract={Other abstract.}, doi={10.1000/other}}\n",
  )
  prepared = _prepare_candidates(
    [current],
    BibliographyIndex.load(empty_config.bibliography_path),
    load_managed_issues(client),
    "model",
  )[0]
  upsert_paper_issue(
    client,  # type: ignore[arg-type]
    current,
    0.9,
    prepared.bibtex,
    prepared.bibkey,
    model_hash="model",
  )
  empty_config.bibliography_path.write_text(
    "@article{lovelace2026, title={A useful paper}, author={Ada Lovelace}, "
    "year={2026}, abstract={A complete abstract.}, doi={10.1000/new}}\n",
    encoding="utf-8",
  )

  refreshed = _prepare_candidates(
    [current],
    BibliographyIndex.load(empty_config.bibliography_path),
    load_managed_issues(client),
    "model",
  )[0]

  assert refreshed.known_bib_key == "lovelace2026"
  assert refreshed.needs_score


def test_project_queue_can_repair_items_in_isolated_step(tmp_path: Path) -> None:
  client = MemoryIssueClient()
  current = record()
  upsert_paper_issue(
    client,  # type: ignore[arg-type]
    current,
    0.9,
    "@article{lovelace2026}",
    "lovelace2026",
    model_hash="model",
  )
  queue_path = tmp_path / "queue.json"
  write_project_queue(
    client,  # type: ignore[arg-type]
    queue_path,
    repository="delalamo/SKM",
    model_hash="model",
  )
  config = PaperbotConfig(project_owner="delalamo", project_number=1)

  class Project:
    def __init__(self) -> None:
      self.calls: list[tuple[str, float]] = []

    def sync(self, node_id: str, score: float) -> str:
      self.calls.append((node_id, score))
      return "ITEM"

  project = Project()
  count = sync_project_queue(
    config,
    queue_path,
    projects_token="unused",
    expected_model_hash="model",
    project_client=project,  # type: ignore[arg-type]
  )

  assert count == 1
  assert project.calls == [("ISSUE_1", 0.9)]


def test_project_queue_refuses_stale_open_issue_after_partial_rescore(
  tmp_path: Path,
) -> None:
  client = MemoryIssueClient()
  current = record()
  upsert_paper_issue(
    client,  # type: ignore[arg-type]
    current,
    0.9,
    "@article{lovelace2026}",
    "lovelace2026",
    model_hash="old-model",
  )

  with pytest.raises(GitHubError, match="mixed-model"):
    write_project_queue(
      client,  # type: ignore[arg-type]
      tmp_path / "queue.json",
      repository="delalamo/SKM",
      model_hash="new-model",
    )
