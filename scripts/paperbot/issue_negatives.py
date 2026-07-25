"""Deterministic human-feedback negatives collected from managed GitHub issues."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path
import re
import tempfile
from typing import Any, Iterable, Mapping, Sequence

from .bibliography import (
  CanonicalWork,
  canonicalize_entries,
  embedding_input_hash,
  load_bibliography,
)
from .github import (
  GITHUB_ACTIONS_BOT_LOGIN,
  MANAGED_BLOCK_BEGIN,
  MANAGED_BLOCK_END,
  META_PREFIX,
  GitHubClient,
  GitHubError,
  normalize_alias,
  parse_managed_meta,
)
from .records import first_author_key, normalize_title


ISSUE_NEGATIVE_SCHEMA = 1
ISSUE_NEGATIVE_CORPUS = "issue_negatives.jsonl"
ISSUE_NEGATIVE_MATRIX = "issue_negative_embeddings.npy"
ISSUE_NEGATIVE_MANIFEST = "issue_negative_manifest.jsonl"
OMITTED_BIBLIOGRAPHY = "bibliography_overlap"
OMITTED_FIXED = "fixed_negative_overlap"
_OMISSION_REASONS = {OMITTED_BIBLIOGRAPHY, OMITTED_FIXED}
_SHA256_RE = re.compile(r"[0-9a-f]{64}")
_MANAGED_BLOCK_RE = re.compile(
  re.escape(MANAGED_BLOCK_BEGIN)
  + r"(.*?)"
  + re.escape(MANAGED_BLOCK_END),
  re.DOTALL,
)
_ABSTRACT_RE = re.compile(
  r"(?:^|\n)## Abstract\s*\n\s*(.*?)\s*\n## BibTeX(?:\n|$)",
  re.DOTALL,
)
_VERSION_RE = re.compile(r"\d+")
_ISSUE_URL_NUMBER_RE = re.compile(r"/issues/(\d+)(?:[/?#].*)?$")
_MANAGED_HASH_FIELDS = frozenset({
  "title",
  "abstract",
  "bibtex",
  "identifiers",
  "version",
  "authors",
  "venue",
  "url",
  "created",
  "updated",
  "license",
})
_PREPRINT_DOI_PREFIXES = (
  "10.1101/",
  "10.21203/rs.",
  "10.26434/",
  "10.48550/arxiv.",
  "10.64898/",
)


@dataclass(frozen=True)
class IssueNegativeRecord:
  schema_version: int
  work_id: str
  aliases: tuple[str, ...]
  issue_numbers: tuple[int, ...]
  issue_urls: tuple[str, ...]
  selected_issue_number: int
  title: str
  abstract: str
  input_hash: str
  metadata_hash: str
  active: bool
  omission_reasons: tuple[str, ...] = ()
  bibliography_keys: tuple[str, ...] = ()
  fixed_negative_ids: tuple[str, ...] = ()

  def to_dict(self) -> dict[str, Any]:
    return {
      "schema_version": self.schema_version,
      "work_id": self.work_id,
      "aliases": list(self.aliases),
      "issue_numbers": list(self.issue_numbers),
      "issue_urls": list(self.issue_urls),
      "selected_issue_number": self.selected_issue_number,
      "title": self.title,
      "abstract": self.abstract,
      "input_hash": self.input_hash,
      "metadata_hash": self.metadata_hash,
      "active": self.active,
      "omission_reasons": list(self.omission_reasons),
      "bibliography_keys": list(self.bibliography_keys),
      "fixed_negative_ids": list(self.fixed_negative_ids),
    }

  @classmethod
  def from_mapping(
    cls, value: Mapping[str, Any], *, context: str = "issue-negative record"
  ) -> IssueNegativeRecord:
    schema_version = value.get("schema_version")
    if (
      not isinstance(schema_version, int)
      or isinstance(schema_version, bool)
      or schema_version != ISSUE_NEGATIVE_SCHEMA
    ):
      raise ValueError(f"{context} has an unsupported schema")
    raw_work_id = value.get("work_id")
    work_id_text = (
      raw_work_id.strip() if isinstance(raw_work_id, str) else ""
    )
    work_id = normalize_alias(work_id_text)
    aliases_value = value.get("aliases")
    numbers_value = value.get("issue_numbers")
    urls_value = value.get("issue_urls")
    title = str(value.get("title") or "").strip()
    abstract = str(value.get("abstract") or "").strip()
    input_hash = str(value.get("input_hash") or "").strip().casefold()
    metadata_hash = str(value.get("metadata_hash") or "").strip().casefold()
    selected_issue_number = value.get("selected_issue_number")
    active = value.get("active")
    omission_reasons_value = value.get("omission_reasons")
    bibliography_keys_value = value.get("bibliography_keys")
    fixed_negative_ids_value = value.get("fixed_negative_ids")
    if (
      not work_id
      or work_id != work_id_text
      or not title
      or not abstract
    ):
      raise ValueError(f"{context} is missing its identity, title, or abstract")
    if (
      not isinstance(aliases_value, list)
      or any(not isinstance(alias, str) for alias in aliases_value)
    ):
      raise ValueError(f"{context} aliases must be a list")
    raw_aliases = tuple(alias.strip() for alias in aliases_value)
    aliases = tuple(normalize_alias(alias) for alias in raw_aliases)
    if (
      not aliases
      or any(not alias for alias in aliases)
      or aliases != raw_aliases
      or aliases != tuple(sorted(set(aliases)))
      or work_id not in aliases
    ):
      raise ValueError(f"{context} aliases are invalid or noncanonical")
    if (
      not isinstance(numbers_value, list)
      or not numbers_value
      or any(
        not isinstance(number, int) or isinstance(number, bool) or number <= 0
        for number in numbers_value
      )
    ):
      raise ValueError(f"{context} issue numbers are invalid")
    issue_numbers = tuple(numbers_value)
    if issue_numbers != tuple(sorted(set(issue_numbers))):
      raise ValueError(f"{context} issue numbers are not unique and sorted")
    if (
      not isinstance(selected_issue_number, int)
      or isinstance(selected_issue_number, bool)
      or selected_issue_number not in issue_numbers
    ):
      raise ValueError(f"{context} selected issue number is invalid")
    if (
      not isinstance(urls_value, list)
      or not urls_value
      or any(not isinstance(url, str) or not url.strip() for url in urls_value)
    ):
      raise ValueError(f"{context} issue URLs are invalid")
    issue_urls = tuple(str(url).strip() for url in urls_value)
    url_numbers = {
      int(match.group(1))
      for url in issue_urls
      if (match := _ISSUE_URL_NUMBER_RE.search(url))
    }
    if (
      issue_urls != tuple(sorted(set(issue_urls)))
      or len(url_numbers) != len(issue_urls)
      or url_numbers != set(issue_numbers)
    ):
      raise ValueError(f"{context} issue URLs are not unique and sorted")
    if _SHA256_RE.fullmatch(metadata_hash) is None:
      raise ValueError(f"{context} metadata hash is invalid")
    if (
      _SHA256_RE.fullmatch(input_hash) is None
      or input_hash != embedding_input_hash(title, abstract)
    ):
      raise ValueError(f"{context} SPECTER2 input hash is invalid")
    if active is not True and active is not False:
      raise ValueError(f"{context} active flag is invalid")
    if not isinstance(omission_reasons_value, list):
      raise ValueError(f"{context} omission reasons must be a list")
    omission_reasons = tuple(str(reason) for reason in omission_reasons_value)
    if (
      omission_reasons != tuple(sorted(set(omission_reasons)))
      or any(reason not in _OMISSION_REASONS for reason in omission_reasons)
      or active == bool(omission_reasons)
    ):
      raise ValueError(f"{context} has invalid omission reasons")
    bibliography_keys = _canonical_string_list(
      bibliography_keys_value, f"{context} bibliography keys"
    )
    fixed_negative_ids = _canonical_string_list(
      fixed_negative_ids_value, f"{context} fixed-negative IDs"
    )
    if bool(bibliography_keys) != (OMITTED_BIBLIOGRAPHY in omission_reasons):
      raise ValueError(f"{context} bibliography overlap provenance is invalid")
    if bool(fixed_negative_ids) != (OMITTED_FIXED in omission_reasons):
      raise ValueError(f"{context} fixed-negative overlap provenance is invalid")
    return cls(
      schema_version=ISSUE_NEGATIVE_SCHEMA,
      work_id=work_id,
      aliases=aliases,
      issue_numbers=issue_numbers,
      issue_urls=issue_urls,
      selected_issue_number=selected_issue_number,
      title=title,
      abstract=abstract,
      input_hash=input_hash,
      metadata_hash=metadata_hash,
      active=bool(active),
      omission_reasons=omission_reasons,
      bibliography_keys=bibliography_keys,
      fixed_negative_ids=fixed_negative_ids,
    )


def _canonical_string_list(value: Any, context: str) -> tuple[str, ...]:
  if not isinstance(value, list):
    raise ValueError(f"{context} must be a list")
  result = tuple(str(item).strip() for item in value)
  if any(not item for item in result) or result != tuple(sorted(set(result))):
    raise ValueError(f"{context} must contain unique sorted strings")
  return result


@dataclass(frozen=True)
class _Candidate:
  number: int
  node_id: str
  url: str
  work_id: str
  aliases: tuple[str, ...]
  title: str
  abstract: str
  input_hash: str
  metadata_hash: str
  version: str
  managed_updated: str


class _UnionFind:
  def __init__(self, size: int) -> None:
    self.parents = list(range(size))

  def find(self, index: int) -> int:
    while self.parents[index] != index:
      self.parents[index] = self.parents[self.parents[index]]
      index = self.parents[index]
    return index

  def union(self, left: int, right: int) -> None:
    left_root = self.find(left)
    right_root = self.find(right)
    if left_root != right_root:
      self.parents[max(left_root, right_root)] = min(left_root, right_root)


def load_issue_negative_snapshot(path: Path | str) -> list[IssueNegativeRecord]:
  snapshot_path = Path(path)
  if not snapshot_path.exists():
    return []
  records: list[IssueNegativeRecord] = []
  for line_number, line in enumerate(
    snapshot_path.read_text(encoding="utf-8").splitlines(), 1
  ):
    if not line.strip():
      continue
    try:
      payload = json.loads(line)
    except json.JSONDecodeError as error:
      raise ValueError(
        f"Invalid issue-negative JSON at {snapshot_path}:{line_number}"
      ) from error
    if not isinstance(payload, Mapping):
      raise ValueError(
        f"Expected an object at {snapshot_path}:{line_number}"
      )
    records.append(
      IssueNegativeRecord.from_mapping(
        payload, context=f"{snapshot_path.name}:{line_number}"
      )
    )
  ordering = [(record.work_id, record.issue_numbers) for record in records]
  if ordering != sorted(ordering):
    raise ValueError("Issue-negative snapshot is not deterministically sorted")
  if len({record.work_id for record in records}) != len(records):
    raise ValueError("Issue-negative snapshot contains duplicate work identities")
  issue_owners: dict[int, str] = {}
  for record in records:
    for issue_number in record.issue_numbers:
      previous = issue_owners.get(issue_number)
      if previous is not None:
        raise ValueError(
          f"GitHub issue #{issue_number} appears in issue-negative works "
          f"{previous} and {record.work_id}"
        )
      issue_owners[issue_number] = record.work_id
  return records


def sync_issue_negatives(
  config: Any,
  *,
  github_token: str = "",
  client: GitHubClient | None = None,
) -> dict[str, Any]:
  """Snapshot current closed ``negative`` issues for the next model fit."""

  configured_repository = str(config.repository)
  workflow_repository = os.getenv("GITHUB_REPOSITORY", "").strip()
  if (
    workflow_repository
    and workflow_repository.casefold() != configured_repository.casefold()
  ):
    raise ValueError(
      "Configured paper repository does not match GITHUB_REPOSITORY"
    )
  github = client or GitHubClient(configured_repository, github_token)
  works = canonicalize_entries(load_bibliography(config.bibliography_path))
  positive_aliases, positive_inputs, positive_titles = _bibliography_identity(
    works
  )
  fixed_aliases, fixed_inputs, fixed_titles = _fixed_negative_identity(
    Path(config.negative_corpus_path)
  )
  raw_candidates = _eligible_candidates(github)
  records = _canonical_records(
    raw_candidates,
    positive_aliases=positive_aliases,
    positive_inputs=positive_inputs,
    positive_titles=positive_titles,
    fixed_aliases=fixed_aliases,
    fixed_inputs=fixed_inputs,
    fixed_titles=fixed_titles,
  )
  output_path = Path(config.artifact_dir) / ISSUE_NEGATIVE_CORPUS
  _write_snapshot(output_path, records)
  omissions: dict[str, int] = {}
  for record in records:
    for reason in record.omission_reasons:
      omissions[reason] = omissions.get(reason, 0) + 1
  return {
    "ok": True,
    "path": str(output_path),
    "eligible_issue_count": len(raw_candidates),
    "canonical_work_count": len(records),
    "active_count": sum(record.active for record in records),
    "duplicate_issue_count": len(raw_candidates) - len(records),
    "omission_counts": dict(sorted(omissions.items())),
  }


def _eligible_candidates(client: GitHubClient) -> list[_Candidate]:
  seen: dict[int, _Candidate] = {}
  seen_nodes: dict[str, _Candidate] = {}
  # Do not use a server-side label filter: selection must remain correct if the
  # repository spells the label with different capitalization.
  for raw in client.list_issues(label=None):
    if "pull_request" in raw:
      continue
    if str(raw.get("state") or "").casefold() != "closed":
      continue
    labels = {
      str(label.get("name", "") if isinstance(label, Mapping) else label).casefold()
      for label in (raw.get("labels") or [])
    }
    if "negative" not in labels:
      continue
    author = raw.get("user")
    login = str(
      author.get("login", "") if isinstance(author, Mapping) else ""
    ).casefold()
    if login != GITHUB_ACTIONS_BOT_LOGIN.casefold():
      continue
    # A closed negative produced by another workflow is outside paperbot's
    # corpus. Conversely, anything carrying the paper label or a paperbot
    # marker is clearly intended managed data and must validate fail-closed.
    body = str(raw.get("body") or "")
    if (
      "paper" not in labels
      and MANAGED_BLOCK_BEGIN not in body
      and MANAGED_BLOCK_END not in body
      and META_PREFIX not in body
    ):
      continue
    candidate = _candidate_from_issue(raw)
    previous = seen.get(candidate.number)
    if previous is not None and previous != candidate:
      raise GitHubError(
        f"GitHub issue #{candidate.number} appeared more than once with "
        "different managed content"
      )
    previous_node = seen_nodes.get(candidate.node_id)
    if previous_node is not None and previous_node != candidate:
      raise GitHubError(
        f"GitHub issue node {candidate.node_id!r} appeared with conflicting "
        f"issue numbers #{previous_node.number} and #{candidate.number}"
      )
    seen[candidate.number] = candidate
    seen_nodes[candidate.node_id] = candidate
  return sorted(seen.values(), key=lambda candidate: candidate.number)


def _candidate_from_issue(raw: Mapping[str, Any]) -> _Candidate:
  raw_number = raw.get("number")
  if (
    not isinstance(raw_number, int)
    or isinstance(raw_number, bool)
    or raw_number <= 0
  ):
    raise GitHubError("Managed negative issue is missing its issue number")
  number = raw_number
  node_id = str(raw.get("node_id") or "").strip()
  if not node_id:
    raise GitHubError(
      f"Managed negative issue #{number} is missing its immutable node ID"
    )
  body = str(raw.get("body") or "")
  block_matches = list(_MANAGED_BLOCK_RE.finditer(body))
  if (
    len(block_matches) != 1
    or body.count(MANAGED_BLOCK_BEGIN) != 1
    or body.count(MANAGED_BLOCK_END) != 1
  ):
    raise GitHubError(
      f"Managed negative issue #{number} must contain exactly one complete "
      "paperbot block"
    )
  block_match = block_matches[0]
  block = block_match.group(1)
  managed_body = block_match.group(0)
  if body.count(META_PREFIX) != 1 or managed_body.count(META_PREFIX) != 1:
    raise GitHubError(
      f"Managed negative issue #{number} must contain exactly one metadata marker"
    )
  meta = parse_managed_meta(managed_body)
  if meta is None:
    raise GitHubError(
      f"Managed negative issue #{number} is missing paperbot metadata"
    )
  abstract_match = _ABSTRACT_RE.search(block)
  if (
    len(re.findall(r"(?m)^## Abstract\s*$", block)) != 1
    or len(re.findall(r"(?m)^## BibTeX\s*$", block)) != 1
  ):
    raise GitHubError(
      f"Managed negative issue #{number} must contain exactly one abstract "
      "and BibTeX section"
    )
  title = str(raw.get("title") or "").strip()
  abstract = (
    abstract_match.group(1).strip() if abstract_match is not None else ""
  )
  if not title or not abstract:
    raise GitHubError(
      f"Managed negative issue #{number} has no complete title and abstract"
    )
  field_hashes = meta.get("field_hashes")
  if not isinstance(field_hashes, Mapping):
    raise GitHubError(
      f"Managed negative issue #{number} has no field hashes"
    )
  if set(field_hashes) != _MANAGED_HASH_FIELDS or any(
    not isinstance(value, str) or _SHA256_RE.fullmatch(value) is None
    for value in field_hashes.values()
  ):
    raise GitHubError(
      f"Managed negative issue #{number} has incomplete or invalid field hashes"
    )
  for field, value in (("title", title), ("abstract", abstract)):
    expected = str(field_hashes.get(field) or "")
    actual = hashlib.sha256(value.encode("utf-8")).hexdigest()
    if expected != actual:
      raise GitHubError(
        f"Managed negative issue #{number} {field} does not match its "
        "paperbot hash"
      )
  aliases_value = meta.get("aliases")
  if not isinstance(aliases_value, list):
    raise GitHubError(
      f"Managed negative issue #{number} has invalid aliases"
    )
  expected_identifiers = hashlib.sha256(
    json.dumps(aliases_value, separators=(",", ":")).encode("utf-8")
  ).hexdigest()
  if str(field_hashes.get("identifiers") or "") != expected_identifiers:
    raise GitHubError(
      f"Managed negative issue #{number} identifiers do not match their hash"
    )
  for field in ("version", "updated"):
    value = str(meta.get(field) or "")
    expected = str(field_hashes.get(field) or "")
    actual = hashlib.sha256(value.encode("utf-8")).hexdigest()
    if expected != actual:
      raise GitHubError(
        f"Managed negative issue #{number} {field} does not match its "
        "paperbot hash"
      )
  aliases = tuple(normalize_alias(str(alias)) for alias in aliases_value)
  raw_work_id = str(meta.get("work_id") or "")
  work_id = normalize_alias(raw_work_id)
  if (
    not work_id
    or work_id != raw_work_id
    or any(not alias for alias in aliases)
    or list(aliases) != aliases_value
    or aliases != tuple(sorted(set(aliases)))
    or work_id not in aliases
  ):
    raise GitHubError(
      f"Managed negative issue #{number} has noncanonical identity metadata"
    )
  metadata_hash = str(meta.get("metadata_hash") or "").strip().casefold()
  if _SHA256_RE.fullmatch(metadata_hash) is None:
    raise GitHubError(
      f"Managed negative issue #{number} has an invalid metadata hash"
    )
  url = str(raw.get("html_url") or "").strip()
  if not url:
    raise GitHubError(
      f"Managed negative issue #{number} has no GitHub issue URL"
    )
  return _Candidate(
    number=number,
    node_id=node_id,
    url=url,
    work_id=work_id,
    aliases=aliases,
    title=title,
    abstract=abstract,
    input_hash=embedding_input_hash(title, abstract),
    metadata_hash=metadata_hash,
    version=str(meta.get("version") or ""),
    managed_updated=str(meta.get("updated") or ""),
  )


def _canonical_records(
  candidates: Sequence[_Candidate],
  *,
  positive_aliases: Mapping[str, set[str]],
  positive_inputs: Mapping[str, set[str]],
  positive_titles: Mapping[str, set[str]],
  fixed_aliases: Mapping[str, set[str]],
  fixed_inputs: Mapping[str, set[str]],
  fixed_titles: Mapping[str, set[str]],
) -> list[IssueNegativeRecord]:
  groups = _UnionFind(len(candidates))
  alias_owner: dict[str, int] = {}
  title_aliases: dict[str, list[int]] = {}
  input_indexes: dict[str, list[int]] = {}
  for index, candidate in enumerate(candidates):
    for alias in candidate.aliases:
      if alias.startswith("title:"):
        title_aliases.setdefault(alias, []).append(index)
        continue
      previous = alias_owner.get(alias)
      if previous is None:
        alias_owner[alias] = index
      else:
        groups.union(index, previous)
    input_indexes.setdefault(candidate.input_hash, []).append(index)

  # Exact duplicate model inputs normally identify duplicate paper threads.
  # Refuse to use that shortcut if the threads also carry contradictory
  # same-stage identifiers: identical publisher text is not proof that two
  # separately identified journal articles are one work.
  for input_hash, indexes in sorted(input_indexes.items()):
    roots = sorted({groups.find(index) for index in indexes})
    if len(roots) < 2:
      continue
    components = _candidate_components(candidates, groups, roots)
    if _identity_components_conflict(tuple(components.values())):
      numbers = sorted(
        candidate.number
        for members in components.values()
        for candidate in members
      )
      raise GitHubError(
        f"Exact SPECTER2 input {input_hash} ambiguously matches managed "
        f"negative issues {', '.join(f'#{number}' for number in numbers)}"
      )
    first, *rest = roots
    for root in rest:
      groups.union(first, root)

  # The strict title/first-author/year fallback can join a preprint to its
  # publication, but it must not silently collapse distinct strong identities.
  for title_alias, indexes in sorted(title_aliases.items()):
    roots = sorted({groups.find(index) for index in indexes})
    if len(roots) < 2:
      continue
    components = _candidate_components(candidates, groups, roots)
    if _identity_components_conflict(tuple(components.values())):
      numbers = sorted(
        candidate.number
        for members in components.values()
        for candidate in members
      )
      raise GitHubError(
        f"Strict title identity {title_alias} ambiguously matches managed "
        f"negative issues {', '.join(f'#{number}' for number in numbers)}"
      )
    first, *rest = roots
    for root in rest:
      groups.union(first, root)
  components: dict[int, list[_Candidate]] = {}
  for index, candidate in enumerate(candidates):
    components.setdefault(groups.find(index), []).append(candidate)

  records: list[IssueNegativeRecord] = []
  for members in components.values():
    representative = max(members, key=_candidate_revision_key)
    aliases = tuple(
      sorted({alias for member in members for alias in member.aliases})
    )
    issue_numbers = tuple(sorted(member.number for member in members))
    issue_urls = tuple(
      sorted({member.url for member in members if member.url})
    )
    member_titles = {
      normalized
      for member in members
      if (normalized := normalize_title(member.title))
    }
    bibliography_keys = set().union(
      *(positive_aliases.get(alias, set()) for alias in aliases),
      *(positive_inputs.get(member.input_hash, set()) for member in members),
      *(positive_titles.get(title, set()) for title in member_titles),
    )
    fixed_negative_ids = set().union(
      *(fixed_aliases.get(alias, set()) for alias in aliases),
      *(fixed_inputs.get(member.input_hash, set()) for member in members),
      *(fixed_titles.get(title, set()) for title in member_titles),
    )
    omission_reasons = tuple(
      reason
      for reason, applies in (
        (OMITTED_BIBLIOGRAPHY, bool(bibliography_keys)),
        (OMITTED_FIXED, bool(fixed_negative_ids)),
      )
      if applies
    )
    records.append(
      IssueNegativeRecord(
        schema_version=ISSUE_NEGATIVE_SCHEMA,
        work_id=representative.work_id,
        aliases=aliases,
        issue_numbers=issue_numbers,
        issue_urls=issue_urls,
        selected_issue_number=representative.number,
        title=representative.title,
        abstract=representative.abstract,
        input_hash=representative.input_hash,
        metadata_hash=representative.metadata_hash,
        active=not omission_reasons,
        omission_reasons=omission_reasons,
        bibliography_keys=tuple(sorted(bibliography_keys)),
        fixed_negative_ids=tuple(sorted(fixed_negative_ids)),
      )
    )
  records.sort(key=lambda record: (record.work_id, record.issue_numbers))
  if len({record.work_id for record in records}) != len(records):
    raise GitHubError(
      "Issue-negative canonicalization produced duplicate work identities"
    )
  return records


def _candidate_components(
  candidates: Sequence[_Candidate],
  groups: _UnionFind,
  roots: Sequence[int],
) -> dict[int, list[_Candidate]]:
  wanted = set(roots)
  components = {root: [] for root in roots}
  for index, candidate in enumerate(candidates):
    root = groups.find(index)
    if root in wanted:
      components[root].append(candidate)
  return components


def _identity_components_conflict(
  components: Sequence[Sequence[_Candidate]],
) -> bool:
  """Reject fallback merges carrying contradictory same-stage identifiers."""

  identities = [_component_strong_identities(component) for component in components]
  for kind in ("pmid", "arxiv"):
    nonempty = [
      identity[kind]
      for identity in identities
      if isinstance(identity[kind], set) and identity[kind]
    ]
    if len(nonempty) > 1 and not set.intersection(*nonempty):
      return True
  preprint_dois = [
    identity["preprint_doi"]
    for identity in identities
    if identity["preprint_doi"]
  ]
  publication_dois = [
    identity["publication_doi"]
    for identity in identities
    if isinstance(identity["publication_doi"], set)
    and identity["publication_doi"]
  ]
  if (
    len(preprint_dois) > 1
    and not set.intersection(*preprint_dois)
  ) or (
    len(publication_dois) > 1
    and not set.intersection(*publication_dois)
  ):
    return True
  source_kinds = set().union(
    *(
      set(identity["source_ids"])
      for identity in identities
      if isinstance(identity["source_ids"], Mapping)
    )
  )
  for kind in source_kinds:
    nonempty = [
      identity["source_ids"][kind]
      for identity in identities
      if isinstance(identity["source_ids"], Mapping)
      and identity["source_ids"].get(kind)
    ]
    if len(nonempty) > 1 and not set.intersection(*nonempty):
      return True
  return False


def _component_strong_identities(
  candidates: Sequence[_Candidate],
) -> dict[str, set[str] | dict[str, set[str]]]:
  result = {
    "pmid": set(),
    "arxiv": set(),
    "preprint_doi": set(),
    "publication_doi": set(),
    "source_ids": {},
  }
  for candidate in candidates:
    for alias in candidate.aliases:
      kind, _, value = alias.partition(":")
      if kind in {"pmid", "arxiv"}:
        result[kind].add(value)
      elif kind == "doi":
        destination = (
          "preprint_doi" if _is_preprint_doi(value) else "publication_doi"
        )
        result[destination].add(value)
      elif kind and kind != "title" and value:
        source_ids = result["source_ids"]
        assert isinstance(source_ids, dict)
        source_ids.setdefault(kind, set()).add(value)
  return result


def _is_preprint_doi(doi: str) -> bool:
  return doi.startswith(_PREPRINT_DOI_PREFIXES)


def _candidate_revision_key(
  candidate: _Candidate,
) -> tuple[str, int, int, str]:
  version_match = _VERSION_RE.search(candidate.version)
  version = int(version_match.group(0)) if version_match else 0
  return (
    candidate.managed_updated,
    version,
    candidate.number,
    candidate.metadata_hash,
  )


def _bibliography_identity(
  works: Sequence[CanonicalWork],
) -> tuple[
  dict[str, set[str]],
  dict[str, set[str]],
  dict[str, set[str]],
]:
  aliases: dict[str, set[str]] = {}
  inputs: dict[str, set[str]] = {}
  titles: dict[str, set[str]] = {}
  for work in works:
    work_aliases = {
      alias
      for value in (work.work_id, *work.identifiers)
      if (alias := normalize_alias(str(value)))
    }
    title_alias = strict_title_alias(
      work.title, str(work.fields.get("author") or ""), work.year
    )
    if title_alias:
      work_aliases.add(title_alias)
    for alias in work_aliases:
      aliases.setdefault(alias, set()).add(work.citekey)
    inputs.setdefault(
      embedding_input_hash(work.title, work.abstract), set()
    ).add(work.citekey)
    if normalized_title := normalize_title(work.title):
      titles.setdefault(normalized_title, set()).add(work.citekey)
  return aliases, inputs, titles


def _fixed_negative_identity(
  path: Path,
) -> tuple[
  dict[str, set[str]],
  dict[str, set[str]],
  dict[str, set[str]],
]:
  aliases: dict[str, set[str]] = {}
  inputs: dict[str, set[str]] = {}
  titles: dict[str, set[str]] = {}
  if not path.exists():
    return aliases, inputs, titles
  for line_number, line in enumerate(
    path.read_text(encoding="utf-8").splitlines(), 1
  ):
    if not line.strip():
      continue
    try:
      payload = json.loads(line)
    except json.JSONDecodeError as error:
      raise ValueError(
        f"Invalid fixed-negative JSON at {path.name}:{line_number}"
      ) from error
    if not isinstance(payload, Mapping):
      raise ValueError(
        f"Expected an object at {path.name}:{line_number}"
      )
    fixed_id = str(
      payload.get("work_id") or payload.get("paper_id") or ""
    ).strip()
    if not fixed_id:
      raise ValueError(
        f"Fixed negative at {path.name}:{line_number} has no work identity"
      )
    aliases_value = payload.get("aliases") or []
    if not isinstance(aliases_value, list):
      raise ValueError(
        f"Fixed negative aliases at {path.name}:{line_number} must be a list"
      )
    row_aliases: set[str] = set()
    for value in (
      payload.get("work_id"),
      payload.get("paper_id"),
      f"pmid:{payload.get('pmid')}" if payload.get("pmid") else "",
      f"doi:{payload.get('doi')}" if payload.get("doi") else "",
      f"arxiv:{payload.get('arxiv_id')}" if payload.get("arxiv_id") else "",
      *aliases_value,
    ):
      if alias := normalize_alias(str(value or "")):
        row_aliases.add(alias)
    title = str(payload.get("title") or "").strip()
    abstract = str(payload.get("abstract") or "").strip()
    if normalized_title := normalize_title(title):
      titles.setdefault(normalized_title, set()).add(fixed_id)
    if title and abstract:
      inputs.setdefault(embedding_input_hash(title, abstract), set()).add(
        fixed_id
      )
    authors = payload.get("authors") or []
    author_text = (
      " and ".join(str(author) for author in authors)
      if isinstance(authors, list)
      else str(authors)
    )
    title_alias = strict_title_alias(
      title, author_text, str(payload.get("published_year") or "")
    )
    if title_alias:
      row_aliases.add(title_alias)
    for alias in row_aliases:
      aliases.setdefault(alias, set()).add(fixed_id)
  return aliases, inputs, titles


def strict_title_alias(title: str, authors: str, year: str) -> str:
  """Return the title/first-author/year alias used for strict work matching."""

  normalized_title = normalize_title(title)
  author_items = tuple(
    item.strip()
    for item in re.split(r"\s+and\s+", authors, flags=re.IGNORECASE)
    if item.strip()
  )
  author = first_author_key(author_items)
  year_match = re.search(r"(?:19|20)\d{2}", year)
  if not normalized_title or not author or year_match is None:
    return ""
  digest = hashlib.sha256(
    f"{normalized_title}\0{author}\0{year_match.group(0)}".encode("utf-8")
  ).hexdigest()[:24]
  return f"title:{digest}"


def _write_snapshot(
  path: Path, records: Iterable[IssueNegativeRecord]
) -> None:
  path.parent.mkdir(parents=True, exist_ok=True)
  content = "".join(
    json.dumps(
      record.to_dict(),
      ensure_ascii=False,
      sort_keys=True,
      separators=(",", ":"),
    )
    + "\n"
    for record in records
  )
  descriptor, temporary_name = tempfile.mkstemp(
    prefix=f".{path.name}.", dir=path.parent
  )
  temporary = Path(temporary_name)
  try:
    with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
      handle.write(content)
      handle.flush()
      os.fsync(handle.fileno())
    os.replace(temporary, path)
  finally:
    if temporary.exists():
      temporary.unlink()


__all__ = [
  "ISSUE_NEGATIVE_CORPUS",
  "ISSUE_NEGATIVE_MANIFEST",
  "ISSUE_NEGATIVE_MATRIX",
  "ISSUE_NEGATIVE_SCHEMA",
  "IssueNegativeRecord",
  "load_issue_negative_snapshot",
  "strict_title_alias",
  "sync_issue_negatives",
]
