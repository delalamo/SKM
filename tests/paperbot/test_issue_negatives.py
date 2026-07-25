from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pytest

from scripts.paperbot.github import GitHubError, build_managed_meta, render_managed_body
from scripts.paperbot.issue_negatives import (
  OMITTED_BIBLIOGRAPHY,
  OMITTED_FIXED,
  load_issue_negative_snapshot,
  sync_issue_negatives,
)
from scripts.paperbot.records import PaperRecord


class MemoryClient:
  def __init__(self, issues: list[dict[str, Any]]) -> None:
    self.issues = deepcopy(issues)
    self.labels: list[str | None] = []

  def list_issues(self, *, label: str | None = "paper") -> list[dict[str, Any]]:
    self.labels.append(label)
    return deepcopy(self.issues)


def record(
  *,
  doi: str = "10.1000/negative",
  pmid: str = "12345",
  source_id: str = "12345",
  title: str = "An irrelevant paper",
  abstract: str = "This complete abstract describes an unrelated topic.",
  authors: tuple[str, ...] = ("Ada Lovelace",),
  updated_at: str = "2026-07-22",
  version: str = "",
  related_ids: tuple[str, ...] = (),
) -> PaperRecord:
  return PaperRecord(
    source="pubmed",
    source_id=source_id,
    title=title,
    abstract=abstract,
    authors=authors,
    venue="Example journal",
    created_at="2026-07-20",
    updated_at=updated_at,
    doi=doi,
    pmid=pmid,
    version=version,
    related_ids=related_ids,
  )


def managed_issue(
  paper: PaperRecord,
  *,
  number: int = 1,
  state: str = "closed",
  labels: tuple[str, ...] = ("paper", "AI-generated", "negative"),
  login: str = "github-actions[bot]",
  prefix: str = "",
  suffix: str = "",
) -> dict[str, Any]:
  bibtex = (
    "@article{lovelace2026,\n"
    f"  title = {{{paper.title}}},\n"
    f"  abstract = {{{paper.abstract}}},\n"
    "}"
  )
  meta = build_managed_meta(
    paper, 0.9, bibtex, "lovelace2026", model_hash="model"
  )
  body = render_managed_body(
    paper, 0.9, bibtex, "lovelace2026", meta=meta
  )
  return {
    "number": number,
    "node_id": f"ISSUE_{number}",
    "title": paper.title,
    "body": f"{prefix}{body}{suffix}",
    "state": state,
    "html_url": f"https://github.test/issues/{number}",
    "labels": [{"name": label} for label in labels],
    "user": {"login": login},
  }


def config(
  tmp_path: Path,
  *,
  bibliography_doi: str = "10.1000/positive",
  fixed: dict[str, Any] | None = None,
) -> SimpleNamespace:
  bibliography = tmp_path / "bibliography.bib"
  bibliography.write_text(
    "@article{positive2026,\n"
    "  title = {A useful paper},\n"
    "  author = {Hopper, Grace},\n"
    "  year = {2026},\n"
    "  abstract = {A useful abstract about the target field.},\n"
    f"  doi = {{{bibliography_doi}}},\n"
    "}\n",
    encoding="utf-8",
  )
  artifacts = tmp_path / "paper_relevance"
  artifacts.mkdir()
  negative_corpus = artifacts / "pubmed_negatives_v1.jsonl"
  if fixed is None:
    negative_corpus.write_text("", encoding="utf-8")
  else:
    import json

    negative_corpus.write_text(
      json.dumps(fixed, sort_keys=True) + "\n", encoding="utf-8"
    )
  return SimpleNamespace(
    repository="delalamo/SKM",
    bibliography_path=bibliography,
    artifact_dir=artifacts,
    negative_corpus_path=negative_corpus,
  )


def test_sync_selects_only_closed_bot_managed_negative_issues(
  tmp_path: Path,
) -> None:
  paper = record()
  selected = managed_issue(
    paper,
    number=1,
    labels=("paper", "NeGaTiVe"),
    prefix="User note before.\n",
    suffix="\nUser note after.",
  )
  client = MemoryClient(
    [
      selected,
      managed_issue(paper, number=2, state="open"),
      managed_issue(paper, number=3, labels=("paper",)),
      managed_issue(paper, number=4, login="someone"),
    ]
  )

  result = sync_issue_negatives(config(tmp_path), client=client)
  snapshot = load_issue_negative_snapshot(
    tmp_path / "paper_relevance" / "issue_negatives.jsonl"
  )

  assert client.labels == [None]
  assert result["eligible_issue_count"] == 1
  assert result["active_count"] == 1
  assert snapshot[0].issue_numbers == (1,)
  assert snapshot[0].abstract == paper.abstract
  assert "User note" not in snapshot[0].abstract


def test_duplicate_issues_contribute_one_canonical_work(tmp_path: Path) -> None:
  paper = record()
  client = MemoryClient(
    [managed_issue(paper, number=9), managed_issue(paper, number=4)]
  )

  result = sync_issue_negatives(config(tmp_path), client=client)
  [row] = load_issue_negative_snapshot(
    tmp_path / "paper_relevance" / "issue_negatives.jsonl"
  )

  assert result["duplicate_issue_count"] == 1
  assert result["active_count"] == 1
  assert row.issue_numbers == (4, 9)


def test_bibliography_overlap_is_recorded_and_omitted(tmp_path: Path) -> None:
  paper = record()
  configuration = config(tmp_path, bibliography_doi=paper.doi)

  result = sync_issue_negatives(
    configuration, client=MemoryClient([managed_issue(paper)])
  )
  [row] = load_issue_negative_snapshot(
    configuration.artifact_dir / "issue_negatives.jsonl"
  )

  assert result["active_count"] == 0
  assert result["omission_counts"] == {OMITTED_BIBLIOGRAPHY: 1}
  assert row.active is False
  assert row.omission_reasons == (OMITTED_BIBLIOGRAPHY,)
  assert row.bibliography_keys == ("positive2026",)


def test_fixed_negative_overlap_receives_no_extra_weight(tmp_path: Path) -> None:
  paper = record()
  configuration = config(
    tmp_path,
    fixed={
      "paper_id": "pmid:12345",
      "work_id": f"doi:{paper.doi}",
      "pmid": "12345",
      "doi": paper.doi,
      "title": paper.title,
      "abstract": paper.abstract,
      "authors": ["Lovelace, Ada"],
      "published_year": 2026,
    },
  )

  result = sync_issue_negatives(
    configuration, client=MemoryClient([managed_issue(paper)])
  )
  [row] = load_issue_negative_snapshot(
    configuration.artifact_dir / "issue_negatives.jsonl"
  )

  assert result["active_count"] == 0
  assert result["omission_counts"] == {OMITTED_FIXED: 1}
  assert row.omission_reasons == (OMITTED_FIXED,)
  assert row.fixed_negative_ids == (f"doi:{paper.doi}",)


def test_unchanged_sync_is_byte_identical(tmp_path: Path) -> None:
  configuration = config(tmp_path)
  client = MemoryClient([managed_issue(record())])

  sync_issue_negatives(configuration, client=client)
  path = configuration.artifact_dir / "issue_negatives.jsonl"
  first = path.read_bytes()
  sync_issue_negatives(configuration, client=client)

  assert path.read_bytes() == first


def test_managed_title_hash_mismatch_fails_closed(tmp_path: Path) -> None:
  issue = managed_issue(record())
  issue["title"] = "Edited title"

  with pytest.raises(GitHubError, match="title.*hash"):
    sync_issue_negatives(config(tmp_path), client=MemoryClient([issue]))


def test_repeated_issue_number_with_different_content_fails(tmp_path: Path) -> None:
  first = managed_issue(record(), number=7)
  second = managed_issue(
    record(
      doi="10.1000/other",
      title="Another irrelevant paper",
      abstract="Another complete and unrelated abstract.",
    ),
    number=7,
  )

  with pytest.raises(GitHubError, match="appeared more than once"):
    sync_issue_negatives(
      config(tmp_path), client=MemoryClient([first, second])
    )


def test_workflow_repository_mismatch_fails_before_reading_issues(
  tmp_path: Path,
  monkeypatch: pytest.MonkeyPatch,
) -> None:
  client = MemoryClient([managed_issue(record())])
  monkeypatch.setenv("GITHUB_REPOSITORY", "someone/untrusted-fork")

  with pytest.raises(ValueError, match="does not match GITHUB_REPOSITORY"):
    sync_issue_negatives(config(tmp_path), client=client)

  assert client.labels == []


def test_unrelated_actions_issue_with_negative_label_is_ignored(
  tmp_path: Path,
) -> None:
  unrelated = {
    "number": 50,
    "node_id": "ISSUE_50",
    "title": "A deployment failed",
    "body": "This is not a paperbot issue.",
    "state": "closed",
    "html_url": "https://github.test/issues/50",
    "labels": [{"name": "negative"}],
    "user": {"login": "github-actions[bot]"},
  }

  result = sync_issue_negatives(
    config(tmp_path), client=MemoryClient([unrelated])
  )

  assert result["eligible_issue_count"] == 0
  assert result["canonical_work_count"] == 0


def test_lifecycle_reopen_and_label_removal_deactivate_on_next_sync(
  tmp_path: Path,
) -> None:
  configuration = config(tmp_path)
  issue = managed_issue(record())

  sync_issue_negatives(configuration, client=MemoryClient([issue]))
  assert len(load_issue_negative_snapshot(
    configuration.artifact_dir / "issue_negatives.jsonl"
  )) == 1

  issue["state"] = "open"
  sync_issue_negatives(configuration, client=MemoryClient([issue]))
  assert load_issue_negative_snapshot(
    configuration.artifact_dir / "issue_negatives.jsonl"
  ) == []

  issue["state"] = "closed"
  issue["labels"] = [{"name": "paper"}]
  sync_issue_negatives(configuration, client=MemoryClient([issue]))
  assert load_issue_negative_snapshot(
    configuration.artifact_dir / "issue_negatives.jsonl"
  ) == []

  issue["labels"].append({"name": "NEGATIVE"})
  sync_issue_negatives(configuration, client=MemoryClient([issue]))
  assert len(load_issue_negative_snapshot(
    configuration.artifact_dir / "issue_negatives.jsonl"
  )) == 1


@pytest.mark.parametrize(
  ("edit", "message"),
  [
    (
      lambda issue: issue.update(
        body=issue["body"].replace(
          "<!-- paperbot:managed:end -->", ""
        )
      ),
      "complete paperbot block",
    ),
    (
      lambda issue: issue.update(
        body=issue["body"].replace(
          "## BibTeX", "## Abstract\n\nInjected text\n\n## BibTeX"
        )
      ),
      "exactly one abstract",
    ),
    (
      lambda issue: issue.update(
        body=issue["body"].replace(
          record().abstract, "An edited abstract."
        )
      ),
      "abstract.*hash",
    ),
  ],
)
def test_malformed_managed_negatives_fail_closed(
  tmp_path: Path, edit: Any, message: str
) -> None:
  issue = managed_issue(record())
  edit(issue)

  with pytest.raises(GitHubError, match=message):
    sync_issue_negatives(config(tmp_path), client=MemoryClient([issue]))


def test_identifier_hash_mismatch_fails_closed(tmp_path: Path) -> None:
  issue = managed_issue(record())
  marker = '"identifiers":"'
  position = issue["body"].index(marker) + len(marker)
  issue["body"] = (
    issue["body"][:position] + "0" * 64 + issue["body"][position + 64 :]
  )

  with pytest.raises(GitHubError, match="identifiers.*hash"):
    sync_issue_negatives(config(tmp_path), client=MemoryClient([issue]))


def test_transitive_aliases_merge_once_and_keep_latest_revision(
  tmp_path: Path,
) -> None:
  first = record(
    doi="10.1101/2026.01.01.1",
    pmid="",
    source_id="preprint",
    updated_at="2026-07-20",
  )
  middle = record(
    doi="",
    pmid="222",
    source_id="pubmed",
    abstract="A revised but still irrelevant abstract.",
    related_ids=("doi:10.1101/2026.01.01.1",),
    updated_at="2026-07-21",
    version="2",
  )
  latest = record(
    doi="10.1000/publication",
    pmid="",
    source_id="publication",
    abstract="The latest irrelevant abstract.",
    related_ids=("pmid:222",),
    updated_at="2026-07-22",
    version="3",
  )
  configuration = config(tmp_path)

  result = sync_issue_negatives(
    configuration,
    client=MemoryClient([
      managed_issue(latest, number=13),
      managed_issue(first, number=11),
      managed_issue(middle, number=12),
    ]),
  )
  [row] = load_issue_negative_snapshot(
    configuration.artifact_dir / "issue_negatives.jsonl"
  )

  assert result["canonical_work_count"] == 1
  assert result["duplicate_issue_count"] == 2
  assert row.issue_numbers == (11, 12, 13)
  assert row.selected_issue_number == 13
  assert row.abstract == latest.abstract


def test_title_fallback_with_conflicting_publication_dois_fails(
  tmp_path: Path,
) -> None:
  first = record(
    doi="10.1000/first",
    pmid="",
    source_id="first",
    abstract="First abstract.",
  )
  second = record(
    doi="10.1000/second",
    pmid="",
    source_id="second",
    abstract="Second abstract.",
  )

  with pytest.raises(GitHubError, match="ambiguously matches"):
    sync_issue_negatives(
      config(tmp_path),
      client=MemoryClient([
        managed_issue(first, number=1),
        managed_issue(second, number=2),
      ]),
    )


def test_same_node_id_with_conflicting_issue_numbers_fails(tmp_path: Path) -> None:
  first = managed_issue(record(), number=1)
  second = managed_issue(
    record(
      doi="10.1000/second",
      pmid="",
      source_id="second",
      title="A different paper",
      abstract="A different abstract.",
    ),
    number=2,
  )
  second["node_id"] = first["node_id"]

  with pytest.raises(GitHubError, match="node.*conflicting"):
    sync_issue_negatives(
      config(tmp_path), client=MemoryClient([first, second])
    )


def test_strict_title_author_year_match_omits_preprint_now_in_bibliography(
  tmp_path: Path,
) -> None:
  paper = record(
    doi="10.1101/2026.01.01.1",
    pmid="",
    source_id="preprint",
    abstract="A preprint abstract that differs from the bibliography.",
  )
  configuration = config(tmp_path)
  configuration.bibliography_path.write_text(
    "@article{published2026,\n"
    "  title = {An irrelevant paper},\n"
    "  author = {Lovelace, Ada},\n"
    "  year = {2026},\n"
    "  abstract = {The later journal abstract.},\n"
    "  doi = {10.1000/publication},\n"
    "}\n",
    encoding="utf-8",
  )

  result = sync_issue_negatives(
    configuration, client=MemoryClient([managed_issue(paper)])
  )
  [row] = load_issue_negative_snapshot(
    configuration.artifact_dir / "issue_negatives.jsonl"
  )

  assert result["active_count"] == 0
  assert row.omission_reasons == (OMITTED_BIBLIOGRAPHY,)
  assert row.bibliography_keys == ("published2026",)
