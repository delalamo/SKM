"""End-to-end daily discovery, ranking, issue, and Project reconciliation."""

from __future__ import annotations

import hashlib
import json
import os
import re
import tempfile
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

from .bibliography import (
  BibliographyEntry,
  CanonicalWork,
  canonicalize_entries,
  load_bibliography,
  render_entry,
)
from .config import PaperbotConfig
from .github import (
  GitHubClient,
  GitHubError,
  ManagedIssue,
  ManagedIssueIndex,
  ProjectClient,
  build_managed_meta,
  ensure_paper_label,
  load_managed_issues,
  reserve_bibtex_key,
  rescore_managed_issues,
  sync_project,
  upsert_paper_issue,
)
from .model import LoadedModel, Specter2Encoder, check_model, load_model, score_documents
from .records import PaperRecord, first_author_key, normalize_title
from .sources import FetchReport, FetchWindow, SourceFailure, fetch_all_sources


ABSTRACT_SECTION_RE = re.compile(
  r"(?:^|\n)## Abstract\s*\n\s*(.*?)\s*\n## BibTeX(?:\n|$)", re.DOTALL
)


@dataclass(frozen=True)
class BibliographyMatch:
  key: str
  work: CanonicalWork


@dataclass
class BibliographyIndex:
  reserved_keys: set[str]
  by_alias: dict[str, BibliographyMatch]

  @classmethod
  def load(cls, path: Path | str) -> "BibliographyIndex":
    entries = load_bibliography(path)
    index = cls({entry.key for entry in entries}, {})
    for work in canonicalize_entries(entries):
      match = BibliographyMatch(work.citekey, work)
      aliases = set(work.identifiers)
      fallback = _bibliography_title_alias(work)
      if fallback:
        aliases.add(fallback)
      for alias in aliases:
        incumbent = index.by_alias.get(alias)
        if incumbent and incumbent.work.work_id != work.work_id:
          raise ValueError(
            f"bibliography identity {alias!r} maps to both "
            f"{incumbent.key!r} and {work.citekey!r}"
          )
        index.by_alias[alias] = match
    return index

  def find(self, record: PaperRecord) -> BibliographyMatch | None:
    matches = {
      match.work.work_id: match
      for alias in record.identity_aliases()
      if (match := self.by_alias.get(alias)) is not None
    }
    if len(matches) > 1:
      keys = ", ".join(sorted(match.key for match in matches.values()))
      raise ValueError(f"paper matches multiple bibliography works: {keys}")
    return next(iter(matches.values()), None)


@dataclass(frozen=True)
class Candidate:
  record: PaperRecord
  bibtex: str
  bibkey: str
  known_bib_key: str | None
  existing_issue_number: int | None
  needs_score: bool


@dataclass(frozen=True)
class CandidateResult:
  work_id: str
  title: str
  score: float
  action: str
  issue_number: int | None
  bibkey: str
  known_bib_key: str | None
  bibtex: str

  def to_dict(self) -> dict[str, Any]:
    return {
      "work_id": self.work_id,
      "title": self.title,
      "score": self.score,
      "action": self.action,
      "issue_number": self.issue_number,
      "bibkey": self.bibkey,
      "known_bib_key": self.known_bib_key,
      "bibtex": self.bibtex,
    }


@dataclass(frozen=True)
class DailyResult:
  as_of: str
  logical_since: str
  query_since: str
  dry_run: bool
  model_hash: str
  source_counts: Mapping[str, int]
  fetched_count: int
  stale_open_issues: int
  candidates: tuple[CandidateResult, ...]
  feed_errors: tuple[Mapping[str, Any], ...]
  publish_errors: tuple[str, ...]

  @property
  def blocking_feed_errors(self) -> tuple[Mapping[str, Any], ...]:
    """Return feed failures that make this tranche incomplete without recovery."""

    has_recovery_overlap = datetime.fromisoformat(self.query_since) < datetime.fromisoformat(
      self.logical_since
    )
    if not has_recovery_overlap:
      return self.feed_errors
    return tuple(
      error
      for error in self.feed_errors
      if error.get("retryable") is not True
      or self.source_counts.get(str(error.get("source") or ""), 0) <= 0
    )

  @property
  def ok(self) -> bool:
    return not self.blocking_feed_errors and not self.publish_errors

  def to_dict(self) -> dict[str, Any]:
    return {
      "ok": self.ok,
      "as_of": self.as_of,
      "logical_since": self.logical_since,
      "query_since": self.query_since,
      "dry_run": self.dry_run,
      "model_hash": self.model_hash,
      "source_counts": dict(self.source_counts),
      "fetched_count": self.fetched_count,
      "stale_open_issues": self.stale_open_issues,
      "action_counts": _counts(result.action for result in self.candidates),
      "candidates": [result.to_dict() for result in self.candidates],
      "feed_errors": list(self.feed_errors),
      "blocking_feed_errors": list(self.blocking_feed_errors),
      "publish_errors": list(self.publish_errors),
    }


def run_daily(
  config: PaperbotConfig,
  window: FetchWindow,
  *,
  dry_run: bool,
  github_token: str,
  projects_token: str = "",
  ncbi_api_key: str = "",
  fetch_report: FetchReport | None = None,
  encoder: Specter2Encoder | None = None,
  github_client: GitHubClient | None = None,
  project_client: ProjectClient | None = None,
  defer_project: bool = False,
) -> DailyResult:
  """Run one idempotent discovery tranche.

  Model integrity is checked before a label, issue, comment, state, or Project
  write is attempted. Feed errors are retained while successful providers are
  still processed. A retryable partial-provider failure is recoverable when the
  run has a query overlap; zero-result, non-retryable, and exact-backfill
  failures remain blocking. Callers should use ``DailyResult.ok`` as the exit
  status.
  """

  project_enabled = project_configuration_enabled(config)
  if (
    not dry_run
    and project_enabled
    and project_client is None
    and not defer_project
    and not projects_token
  ):
    raise ValueError("PROJECTS_TOKEN is required when Project publishing is configured")

  model_manifest = check_model(
    config.bibliography_path,
    config.artifact_dir,
    negatives_path=config.negative_corpus_path,
    title_only_exceptions_path=config.abstract_exceptions_path,
  )
  model = load_model(config.artifact_dir)
  if model.model_hash != model_manifest.get("model_hash"):
    raise ValueError("loaded classifier does not match the verified model manifest")

  client = github_client or GitHubClient(config.repository, github_token)
  issue_index = load_managed_issues(client)
  report = fetch_report or fetch_all_sources(
    window,
    contact_email=config.contact_email,
    ncbi_api_key=ncbi_api_key,
    known_pubmed_ids=_managed_pubmed_ids(issue_index),
  )
  bibliography = BibliographyIndex.load(config.bibliography_path)
  candidates = _prepare_candidates(report.records, bibliography, issue_index, model.model_hash)

  stale_issues = [
    issue
    for issue in issue_index.issues
    if issue.state == "open" and issue.meta.get("model_hash") != model.model_hash
  ]
  documents = [(_issue_title(issue), _issue_abstract(issue)) for issue in stale_issues]
  documents.extend(
    (candidate.record.title, candidate.record.abstract)
    for candidate in candidates
    if candidate.needs_score
  )
  scores = _score(documents, model, encoder=encoder)
  stale_scores = {
    issue.number: score for issue, score in zip(stale_issues, scores[: len(stale_issues)])
  }
  candidate_scores = iter(scores[len(stale_issues) :])
  resolved_scores: dict[str, float] = {}
  for candidate in candidates:
    if candidate.needs_score:
      resolved_scores[candidate.record.canonical_id] = next(candidate_scores)
    else:
      existing = issue_index.find(candidate.record)
      if existing and existing.number in stale_scores:
        resolved_scores[candidate.record.canonical_id] = stale_scores[existing.number]
      else:
        resolved_scores[candidate.record.canonical_id] = float(
          existing.meta.get("score", 0.0) if existing else 0.0
        )

  project = project_client if project_enabled else None
  if not dry_run and project_enabled and project is None and not defer_project:
    project = ProjectClient(
      projects_token,
      config.project_owner,
      config.project_number,
      relevance_field=config.project_field,
    )

  publish_errors: list[str] = []
  if not dry_run:
    ensure_paper_label(client)
    try:
      # This also reconciles every current open issue with the Project, making
      # a rerun repair an earlier issue-created/Project-failed split outcome.
      rescore_managed_issues(
        client,
        lambda issue: stale_scores[issue.number],
        model.model_hash,
        project=project,
        index=issue_index,
      )
    except Exception as error:  # continue processing successfully fetched papers
      publish_errors.append(f"open-issue/Project reconciliation failed: {error}")
    issue_index = load_managed_issues(client)

  results: list[CandidateResult] = []
  for candidate in candidates:
    record = candidate.record
    score = resolved_scores[record.canonical_id]
    existing = issue_index.find(record)
    if not candidate.needs_score:
      action = "unchanged"
      issue_number = existing.number if existing else None
    elif dry_run:
      if existing:
        action = "would-update"
        issue_number = existing.number
      elif score > config.relevance_threshold:
        action = "would-create"
        issue_number = None
      else:
        action = "below-cutoff"
        issue_number = None
    else:
      try:
        upsert = upsert_paper_issue(
          client,
          record,
          score,
          candidate.bibtex,
          candidate.bibkey,
          candidate.known_bib_key,
          index=issue_index,
          model_hash=model.model_hash,
          cutoff=config.relevance_threshold,
        )
        action = upsert.action
        issue_number = upsert.issue.number if upsert.issue else None
        if upsert.issue is not None and project is not None:
          sync_project(project, upsert.issue.node_id, score)
      except Exception as error:  # preserve other candidates and fail the run
        action = "publish-failed"
        issue_number = existing.number if existing else None
        publish_errors.append(f"{record.canonical_id}: {error}")
    results.append(
      CandidateResult(
        work_id=record.canonical_id,
        title=record.title,
        score=score,
        action=action,
        issue_number=issue_number,
        bibkey=candidate.bibkey,
        known_bib_key=candidate.known_bib_key,
        bibtex=candidate.bibtex,
      )
    )

  return DailyResult(
    as_of=window.until.isoformat(),
    logical_since=window.logical_since.isoformat(),
    query_since=window.query_since.isoformat(),
    dry_run=dry_run,
    model_hash=model.model_hash,
    source_counts=report.source_counts,
    fetched_count=len(report.records),
    stale_open_issues=len(stale_issues),
    candidates=tuple(results),
    feed_errors=tuple(_failure_dict(error) for error in report.errors),
    publish_errors=tuple(publish_errors),
  )


def _managed_pubmed_ids(issues: ManagedIssueIndex) -> tuple[str, ...]:
  """Return PMIDs whose managed issues should be checked for revisions."""

  pmids = {
    alias.removeprefix("pmid:")
    for issue in issues.issues
    for alias in issue.meta.get("aliases", [])
    if isinstance(alias, str)
    and alias.startswith("pmid:")
    and alias.removeprefix("pmid:").isdigit()
  }
  return tuple(sorted(pmids, key=int))


def write_project_queue(
  client: GitHubClient,
  path: Path | str,
  *,
  repository: str,
  model_hash: str,
) -> dict[str, Any]:
  """Snapshot managed issues for a token-isolated Project mutation step."""

  index = load_managed_issues(client)
  stale_open = [
    issue.number
    for issue in index.issues
    if issue.state == "open" and issue.meta.get("model_hash") != model_hash
  ]
  if stale_open:
    numbers = ", ".join(f"#{number}" for number in sorted(stale_open))
    raise GitHubError(
      "refusing to prepare a mixed-model Project queue; stale open issues: "
      + numbers
    )
  payload = {
    "schema": 2,
    "repository": repository,
    "model_hash": model_hash,
    "items": [
      {
        "issue_number": issue.number,
        "issue_node_id": issue.node_id,
        "score": float(issue.meta.get("score", 0.0)),
        "state": issue.state,
        "model_hash": str(issue.meta.get("model_hash", "")),
      }
      for issue in sorted(index.issues, key=lambda value: value.number)
    ],
  }
  _atomic_json(Path(path), payload)
  return payload


def sync_project_queue(
  config: PaperbotConfig,
  path: Path | str,
  *,
  projects_token: str,
  expected_model_hash: str,
  project_client: ProjectClient | None = None,
) -> int:
  """Apply a prepared queue with the Projects credential in this process only."""

  if not project_configuration_enabled(config):
    raise ValueError(
      "GitHub Project synchronization is disabled; set PAPER_PROJECT_OWNER and "
      "PAPER_PROJECT_NUMBER together to enable it"
    )

  payload = json.loads(Path(path).read_text(encoding="utf-8"))
  if payload.get("schema") != 2 or payload.get("repository") != config.repository:
    raise ValueError("invalid or wrong-repository Project queue")
  if payload.get("model_hash") != expected_model_hash:
    raise ValueError("Project queue was prepared under a different relevance model")
  project = project_client
  if project is None:
    if not projects_token:
      raise ValueError("PROJECTS_TOKEN is required for Project synchronization")
    project = ProjectClient(
      projects_token,
      config.project_owner,
      config.project_number,
      relevance_field=config.project_field,
    )
  errors: list[str] = []
  count = 0
  for item in payload.get("items", []):
    try:
      if item.get("state") == "open" and item.get("model_hash") != expected_model_hash:
        raise ValueError("open issue has a score from a different relevance model")
      sync_project(project, str(item["issue_node_id"]), float(item["score"]))
      count += 1
    except Exception as error:
      errors.append(f"issue #{item.get('issue_number', '?')}: {error}")
  if errors:
    raise GitHubError("Project synchronization failed:\n- " + "\n- ".join(errors))
  return count


def project_configuration_enabled(config: PaperbotConfig) -> bool:
  """Return whether Project sync is enabled, rejecting half-configuration."""

  owner_set = bool(config.project_owner.strip())
  number_set = config.project_number is not None
  if owner_set != number_set:
    raise ValueError(
      "PAPER_PROJECT_OWNER and PAPER_PROJECT_NUMBER must be set together"
    )
  return owner_set


def _prepare_candidates(
  records: Sequence[PaperRecord],
  bibliography: BibliographyIndex,
  issues: ManagedIssueIndex,
  model_hash: str,
) -> list[Candidate]:
  reserved = set(bibliography.reserved_keys)
  reserved.update(issues.reserved_bibkeys)
  candidates: list[Candidate] = []
  for record in sorted(records, key=lambda value: value.canonical_id):
    known = bibliography.find(record)
    existing = issues.find(record)
    if existing:
      bibkey = str(existing.meta.get("bibkey") or (known.key if known else ""))
      if not bibkey:
        bibkey = reserve_bibtex_key(_preferred_bibkey(record), reserved)
      else:
        reserved.add(bibkey)
    elif known:
      bibkey = known.key
      reserved.add(bibkey)
    else:
      bibkey = reserve_bibtex_key(_preferred_bibkey(record), reserved)
    bibtex = render_paper_bibtex(record, bibkey, known.work if known else None)
    known_bib_key = known.key if known else None
    preview = build_managed_meta(
      record,
      0.0,
      bibtex,
      bibkey,
      model_hash=model_hash,
      known_bib_key=known_bib_key,
    )
    needs_score = (
      existing is None
      or existing.meta.get("metadata_hash") != preview.get("metadata_hash")
      or existing.meta.get("known_bib_key") != known_bib_key
    )
    candidates.append(
      Candidate(
        record=record,
        bibtex=bibtex,
        bibkey=bibkey,
        known_bib_key=known_bib_key,
        existing_issue_number=existing.number if existing else None,
        needs_score=needs_score,
      )
    )
  return candidates


def render_paper_bibtex(
  record: PaperRecord, key: str, known_work: CanonicalWork | None = None
) -> str:
  fields = dict(known_work.fields) if known_work else {}
  year = str(record.year or fields.get("year") or datetime.now(UTC).year)
  fields.update(
    {
      "title": record.title,
      "author": " and ".join(record.authors) or fields.get("author", ""),
      "year": year,
      "abstract": record.abstract,
      "url": record.url or fields.get("url", ""),
    }
  )
  if record.doi:
    fields["doi"] = record.doi
    fields["url"] = f"https://doi.org/{record.doi}"
  if record.venue and record.venue.casefold() not in {
    "arxiv",
    "biorxiv",
    "medrxiv",
    "chemrxiv",
  }:
    fields["journal"] = record.venue
  if record.arxiv_id:
    fields["eprint"] = record.arxiv_id
    fields["archiveprefix"] = "arXiv"
  if record.version:
    fields["note"] = f"Version {record.version}"
  entry_type = known_work.entry_type if known_work else (
    "article" if fields.get("journal") else "misc"
  )
  return render_entry(BibliographyEntry(entry_type, key, fields))


def _preferred_bibkey(record: PaperRecord) -> str:
  surname = first_author_key(record.authors) or "paper"
  year = record.year or datetime.now(UTC).year
  return re.sub(r"[^a-z0-9]", "", f"{surname}{year}".casefold()) or f"paper{year}"


def _bibliography_title_alias(work: CanonicalWork) -> str:
  authors = re.split(r"\s+and\s+", work.fields.get("author", ""), maxsplit=1, flags=re.I)
  author = first_author_key(tuple(authors[:1]))
  title = normalize_title(work.title)
  year_match = re.search(r"(?:19|20)\d{2}", work.year)
  if not title or not author or not year_match:
    return ""
  digest = hashlib.sha256(
    f"{title}\0{author}\0{year_match.group(0)}".encode("utf-8")
  ).hexdigest()[:24]
  return f"title:{digest}"


def _issue_title(issue: ManagedIssue) -> str:
  title = issue.title.strip()
  if not title:
    raise GitHubError(f"managed issue #{issue.number} has no title")
  return title


def _issue_abstract(issue: ManagedIssue) -> str:
  match = ABSTRACT_SECTION_RE.search(issue.body)
  if not match or not match.group(1).strip():
    raise GitHubError(f"managed issue #{issue.number} has no abstract to rescore")
  return match.group(1).strip()


def _score(
  documents: Sequence[tuple[str, str]],
  model: LoadedModel,
  *,
  encoder: Specter2Encoder | None,
) -> list[float]:
  if not documents:
    return []
  values = score_documents(documents, model, encoder=encoder)
  return [float(value) for value in values]


def _failure_dict(error: SourceFailure) -> dict[str, Any]:
  return {
    "source": error.source,
    "operation": error.operation,
    "message": error.message,
    "retryable": error.retryable,
    "status": error.status,
  }


def _counts(values: Iterable[str]) -> dict[str, int]:
  result: dict[str, int] = {}
  for value in values:
    result[value] = result.get(value, 0) + 1
  return dict(sorted(result.items()))


def _atomic_json(path: Path, payload: Mapping[str, Any]) -> None:
  path.parent.mkdir(parents=True, exist_ok=True)
  with tempfile.NamedTemporaryFile(
    "w", encoding="utf-8", dir=path.parent, delete=False
  ) as handle:
    temporary = Path(handle.name)
    json.dump(payload, handle, ensure_ascii=False, indent=2, sort_keys=True)
    handle.write("\n")
    handle.flush()
    os.fsync(handle.fileno())
  os.replace(temporary, path)


__all__ = [
  "BibliographyIndex",
  "CandidateResult",
  "DailyResult",
  "render_paper_bibtex",
  "run_daily",
  "sync_project_queue",
  "project_configuration_enabled",
  "write_project_queue",
]
