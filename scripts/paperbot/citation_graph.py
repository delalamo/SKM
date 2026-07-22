"""Semantic Scholar citation-graph guard for biological negative examples.

The relevance model's negative corpus should be biologically plausible but far
from the bibliography.  This module provides a deliberately conservative graph
check: a candidate is rejected when it has a direct citation edge (in either
direction) with a positive work, or when it shares at least three cited papers
with the same positive work.

Only caller-selected cache paths are written.  The cache is optional, contains
provider identifiers rather than paper text, and is updated after each
successful API batch so an interrupted audit can resume without repeating all
requests.
"""

from __future__ import annotations

import json
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Iterable, Mapping, Sequence

from .bibliography import CanonicalWork, normalize_arxiv_id, normalize_doi


SEMANTIC_SCHOLAR_BATCH_API = "https://api.semanticscholar.org/graph/v1/paper/batch"
SEMANTIC_SCHOLAR_PROVIDER = "Semantic Scholar Academic Graph"
SEMANTIC_SCHOLAR_CACHE_SCHEMA = 1
SEMANTIC_SCHOLAR_BATCH_SIZE = 500
DEFAULT_REFERENCE_BATCH_SIZE = 50
DEFAULT_MIN_POSITIVE_COVERAGE = 0.60
# One common methods citation is ubiquitous in modern biology and is not
# meaningful graph proximity.  Three references shared with the same positive
# paper is treated as substantive bibliographic coupling.
SHARED_REFERENCE_REJECTION_THRESHOLD = 3
RETRYABLE_STATUS = {429, 500, 502, 503, 504}

JsonRequest = Callable[
  [str, str, Mapping[str, str], Mapping[str, object]], object
]


class SemanticScholarError(RuntimeError):
  """Raised for malformed or unsuccessful Semantic Scholar responses."""


class GraphCoverageError(RuntimeError):
  """Raised when too little of the positive graph is available for an audit."""

  def __init__(self, coverage: CitationGraphCoverage, required: float):
    self.coverage = coverage
    self.required = required
    observed = coverage.positive_reference_coverage
    super().__init__(
      "Semantic Scholar reference coverage for positive works is "
      f"{observed:.1%}; at least {required:.1%} is required"
    )


def _default_json_request(
  method: str,
  url: str,
  headers: Mapping[str, str],
  payload: Mapping[str, object],
  *,
  attempts: int = 8,
  timeout: float = 60.0,
) -> object:
  """Make one retrying JSON request without introducing a new dependency."""

  body = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8")
  request_headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    **headers,
  }
  last_error: Exception | None = None
  for attempt in range(attempts):
    request = urllib.request.Request(
      url, data=body, headers=request_headers, method=method
    )
    try:
      with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.loads(response.read())
    except urllib.error.HTTPError as error:
      if error.code not in RETRYABLE_STATUS:
        raise SemanticScholarError(
          f"Semantic Scholar returned HTTP {error.code}"
        ) from error
      last_error = error
      retry_after = error.headers.get("Retry-After") if error.headers else None
      try:
        delay = (
          min(45.0, max(0.0, float(retry_after)))
          if retry_after
          else min(45.0, 5.0 * (2.0**attempt))
        )
      except ValueError:
        delay = min(45.0, 5.0 * (2.0**attempt))
    except (TimeoutError, urllib.error.URLError, OSError) as error:
      last_error = error
      delay = min(45.0, 5.0 * (2.0**attempt))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
      raise SemanticScholarError("Semantic Scholar returned invalid JSON") from error
    if attempt + 1 < attempts:
      time.sleep(delay)
  detail = f": {last_error}" if last_error is not None else ""
  raise SemanticScholarError(
    f"Semantic Scholar request failed after {attempts} attempts{detail}"
  ) from last_error


def _chunks(values: Sequence[str], size: int) -> Iterable[list[str]]:
  for start in range(0, len(values), size):
    yield list(values[start : start + size])


def _ratio(numerator: int, denominator: int) -> float:
  return numerator / denominator if denominator else 0.0


def semantic_scholar_identifier(identifier: str) -> str:
  """Convert a canonical bibliography identifier into Semantic Scholar syntax."""

  prefix, separator, value = (identifier or "").strip().partition(":")
  if not separator:
    return ""
  prefix = prefix.casefold()
  if prefix == "doi":
    normalized = normalize_doi(value)
    return f"DOI:{normalized}" if normalized else ""
  if prefix == "pmid":
    normalized = value.strip()
    return f"PMID:{normalized}" if normalized.isdigit() else ""
  if prefix == "arxiv":
    normalized = normalize_arxiv_id(value)
    return f"ARXIV:{normalized}" if normalized else ""
  return ""


def positive_identifiers_from_works(
  works: Iterable[CanonicalWork],
) -> dict[str, tuple[str, ...]]:
  """Return supported Semantic Scholar identifiers for canonical positives."""

  result: dict[str, tuple[str, ...]] = {}
  for work in sorted(works, key=lambda item: item.work_id):
    identifiers = {
      converted
      for identifier in work.identifiers
      if (converted := semantic_scholar_identifier(identifier))
    }
    result[work.work_id] = tuple(sorted(identifiers))
  return result


@dataclass(frozen=True)
class GraphNode:
  paper_id: str
  references: frozenset[str]
  references_available: bool

  @classmethod
  def from_api(cls, requested_id: str, payload: object) -> GraphNode | None:
    if payload is None:
      return None
    if not isinstance(payload, dict):
      raise SemanticScholarError(
        f"invalid graph response for Semantic Scholar paper {requested_id}"
      )
    paper_id = str(payload.get("paperId") or requested_id).strip()
    raw_references = payload.get("references")
    # An empty list is ambiguous in the Academic Graph: it may describe a
    # genuinely reference-free item or a paper whose edges were not indexed.
    # It cannot prove distance from the positive corpus, so fail closed.
    available = isinstance(raw_references, list) and bool(raw_references)
    references: set[str] = set()
    if available:
      for reference in raw_references:
        if isinstance(reference, dict) and reference.get("paperId"):
          references.add(str(reference["paperId"]).strip())
    return cls(paper_id, frozenset(references), available and bool(references))

  def to_cache(self) -> dict[str, object]:
    return {
      "paper_id": self.paper_id,
      "references": sorted(self.references),
      "references_available": self.references_available,
    }

  @classmethod
  def from_cache(cls, payload: object) -> GraphNode | None:
    if payload is None:
      return None
    if not isinstance(payload, dict):
      raise SemanticScholarError("invalid Semantic Scholar node cache entry")
    paper_id = payload.get("paper_id")
    references = payload.get("references")
    available = payload.get("references_available")
    if (
      not isinstance(paper_id, str)
      or not isinstance(references, list)
      or not all(isinstance(value, str) for value in references)
      or not isinstance(available, bool)
    ):
      raise SemanticScholarError("invalid Semantic Scholar node cache entry")
    # Normalize schema-v1 caches written before empty lists became fail-closed.
    return cls(paper_id, frozenset(references), available and bool(references))


class SemanticScholarClient:
  """Batched Semantic Scholar client with optional resumable JSON caching."""

  def __init__(
    self,
    *,
    api_key: str = "",
    cache_path: Path | None = None,
    request: JsonRequest = _default_json_request,
    batch_size: int = SEMANTIC_SCHOLAR_BATCH_SIZE,
    reference_batch_size: int | None = None,
    min_interval: float = 1.05,
    sleep: Callable[[float], None] = time.sleep,
    monotonic: Callable[[], float] = time.monotonic,
  ):
    if not 1 <= batch_size <= SEMANTIC_SCHOLAR_BATCH_SIZE:
      raise ValueError(
        f"Semantic Scholar batch_size must be between 1 and {SEMANTIC_SCHOLAR_BATCH_SIZE}"
      )
    if reference_batch_size is None:
      reference_batch_size = min(batch_size, DEFAULT_REFERENCE_BATCH_SIZE)
    if not 1 <= reference_batch_size <= SEMANTIC_SCHOLAR_BATCH_SIZE:
      raise ValueError(
        "Semantic Scholar reference_batch_size must be between 1 and "
        f"{SEMANTIC_SCHOLAR_BATCH_SIZE}"
      )
    self.api_key = api_key.strip()
    self.cache_path = cache_path
    self.request = request
    self.batch_size = batch_size
    # Nested reference data is subject to a 10 MB / 9,999-edge response limit.
    # Smaller batches make silent provider-side truncation substantially less
    # likely while retaining the much larger batch for identifier resolution.
    self.reference_batch_size = reference_batch_size
    self.min_interval = max(0.0, min_interval)
    self.sleep = sleep
    self.monotonic = monotonic
    self._last_request: float | None = None
    self._resolutions: dict[str, str | None] = {}
    self._nodes: dict[str, GraphNode | None] = {}
    self._load_cache()

  def _headers(self) -> dict[str, str]:
    headers = {"User-Agent": "SKM-Paperbot/1.0"}
    if self.api_key:
      headers["x-api-key"] = self.api_key
    return headers

  def _load_cache(self) -> None:
    if self.cache_path is None or not self.cache_path.exists():
      return
    try:
      payload = json.loads(self.cache_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
      raise SemanticScholarError(
        f"cannot read Semantic Scholar cache {self.cache_path}"
      ) from error
    if (
      not isinstance(payload, dict)
      or payload.get("schema_version") != SEMANTIC_SCHOLAR_CACHE_SCHEMA
      or payload.get("provider") != SEMANTIC_SCHOLAR_PROVIDER
    ):
      raise SemanticScholarError("incompatible Semantic Scholar cache")
    raw_resolutions = payload.get("resolutions", {})
    raw_nodes = payload.get("nodes", {})
    if not isinstance(raw_resolutions, dict) or not isinstance(raw_nodes, dict):
      raise SemanticScholarError("invalid Semantic Scholar cache")
    for identifier, paper_id in raw_resolutions.items():
      if not isinstance(identifier, str) or not (
        paper_id is None or isinstance(paper_id, str)
      ):
        raise SemanticScholarError("invalid Semantic Scholar resolution cache entry")
      self._resolutions[identifier] = paper_id
    for paper_id, node in raw_nodes.items():
      if not isinstance(paper_id, str):
        raise SemanticScholarError("invalid Semantic Scholar node cache key")
      self._nodes[paper_id] = GraphNode.from_cache(node)

  def _save_cache(self) -> None:
    if self.cache_path is None:
      return
    self.cache_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
      "schema_version": SEMANTIC_SCHOLAR_CACHE_SCHEMA,
      "provider": SEMANTIC_SCHOLAR_PROVIDER,
      "resolutions": {
        key: self._resolutions[key] for key in sorted(self._resolutions)
      },
      "nodes": {
        key: self._nodes[key].to_cache() if self._nodes[key] is not None else None
        for key in sorted(self._nodes)
      },
    }
    encoded = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    temporary = self.cache_path.with_name(f".{self.cache_path.name}.tmp")
    temporary.write_text(encoded, encoding="utf-8")
    temporary.replace(self.cache_path)

  def _rate_limit(self) -> None:
    if self._last_request is not None and self.min_interval:
      delay = self.min_interval - (self.monotonic() - self._last_request)
      if delay > 0:
        self.sleep(delay)
    self._last_request = self.monotonic()

  def _batch_request(self, identifiers: list[str], fields: str) -> list[object]:
    self._rate_limit()
    query = urllib.parse.urlencode({"fields": fields})
    payload = self.request(
      "POST",
      f"{SEMANTIC_SCHOLAR_BATCH_API}?{query}",
      self._headers(),
      {"ids": identifiers},
    )
    if not isinstance(payload, list) or len(payload) != len(identifiers):
      raise SemanticScholarError(
        "Semantic Scholar batch response did not align with the requested IDs"
      )
    return payload

  def resolve_identifiers(
    self, identifiers: Iterable[str]
  ) -> dict[str, str | None]:
    requested = sorted({value.strip() for value in identifiers if value.strip()})
    missing = [value for value in requested if value not in self._resolutions]
    for batch in _chunks(missing, self.batch_size):
      payload = self._batch_request(batch, "paperId,externalIds")
      for identifier, paper in zip(batch, payload, strict=True):
        if paper is None:
          self._resolutions[identifier] = None
        elif isinstance(paper, dict) and paper.get("paperId"):
          self._resolutions[identifier] = str(paper["paperId"]).strip()
        else:
          raise SemanticScholarError(
            f"invalid resolution response for {identifier}"
          )
      self._save_cache()
    return {identifier: self._resolutions[identifier] for identifier in requested}

  def fetch_nodes(
    self, paper_ids: Iterable[str]
  ) -> dict[str, GraphNode | None]:
    requested = sorted({value.strip() for value in paper_ids if value.strip()})
    missing = [value for value in requested if value not in self._nodes]
    for batch in _chunks(missing, self.reference_batch_size):
      payload = self._batch_request(batch, "paperId,references.paperId")
      for paper_id, paper in zip(batch, payload, strict=True):
        self._nodes[paper_id] = GraphNode.from_api(paper_id, paper)
      self._save_cache()
    return {paper_id: self._nodes[paper_id] for paper_id in requested}


@dataclass(frozen=True)
class CitationGraphCoverage:
  positive_work_total: int
  positive_work_resolved: int
  positive_work_with_references: int
  positive_paper_id_total: int
  positive_paper_id_with_references: int
  negative_work_total: int
  negative_work_resolved: int
  negative_work_with_references: int

  @property
  def positive_resolution_coverage(self) -> float:
    return _ratio(self.positive_work_resolved, self.positive_work_total)

  @property
  def positive_reference_coverage(self) -> float:
    return _ratio(self.positive_work_with_references, self.positive_work_total)

  @property
  def negative_resolution_coverage(self) -> float:
    return _ratio(self.negative_work_resolved, self.negative_work_total)

  @property
  def negative_reference_coverage(self) -> float:
    return _ratio(self.negative_work_with_references, self.negative_work_total)

  def to_dict(self) -> dict[str, object]:
    return {
      "positive": {
        "works_total": self.positive_work_total,
        "works_resolved": self.positive_work_resolved,
        "works_with_references": self.positive_work_with_references,
        "paper_ids_resolved": self.positive_paper_id_total,
        "paper_ids_with_references": self.positive_paper_id_with_references,
        "resolution_fraction": self.positive_resolution_coverage,
        "reference_fraction": self.positive_reference_coverage,
      },
      "negative": {
        "works_total": self.negative_work_total,
        "works_resolved": self.negative_work_resolved,
        "works_with_references": self.negative_work_with_references,
        "resolution_fraction": self.negative_resolution_coverage,
        "reference_fraction": self.negative_reference_coverage,
      },
    }


@dataclass(frozen=True)
class NegativeGraphAudit:
  negative_id: str
  pmid: str
  paper_ids: tuple[str, ...]
  references_available: bool
  reference_count: int
  accepted: bool
  rejection_reason: str | None
  same_positive_work_ids: tuple[str, ...]
  direct_positive_work_ids: tuple[str, ...]
  shared_positive_work_ids: tuple[str, ...]
  shared_reference_ids: tuple[str, ...]
  max_shared_reference_count: int

  def to_dict(self) -> dict[str, object]:
    return {
      "provider": SEMANTIC_SCHOLAR_PROVIDER,
      "pmid": self.pmid,
      "paper_ids": list(self.paper_ids),
      "resolved": bool(self.paper_ids),
      "references_available": self.references_available,
      "reference_count": self.reference_count,
      "accepted": self.accepted,
      "rejection_reason": self.rejection_reason,
      "same_positive_work_count": len(self.same_positive_work_ids),
      "direct_positive_work_count": len(self.direct_positive_work_ids),
      "shared_positive_work_count": len(self.shared_positive_work_ids),
      "shared_reference_count": len(self.shared_reference_ids),
      "max_shared_reference_count": self.max_shared_reference_count,
      "shared_reference_rejection_threshold": (
        SHARED_REFERENCE_REJECTION_THRESHOLD
      ),
      "same_positive_work_ids": list(self.same_positive_work_ids),
      "direct_positive_work_ids": list(self.direct_positive_work_ids),
      "shared_positive_work_ids": list(self.shared_positive_work_ids),
      "shared_reference_ids": list(self.shared_reference_ids),
    }


@dataclass(frozen=True)
class CitationGraphAudit:
  records: Mapping[str, NegativeGraphAudit]
  coverage: CitationGraphCoverage
  min_positive_coverage: float

  @property
  def accepted_ids(self) -> tuple[str, ...]:
    return tuple(
      negative_id
      for negative_id in sorted(self.records)
      if self.records[negative_id].accepted
    )

  @property
  def rejected_ids(self) -> tuple[str, ...]:
    return tuple(
      negative_id
      for negative_id in sorted(self.records)
      if not self.records[negative_id].accepted
    )

  def metadata(self) -> dict[str, object]:
    rejection_counts: dict[str, int] = {}
    for record in self.records.values():
      if record.rejection_reason:
        rejection_counts[record.rejection_reason] = (
          rejection_counts.get(record.rejection_reason, 0) + 1
        )
    return {
      "provider": SEMANTIC_SCHOLAR_PROVIDER,
      "api": SEMANTIC_SCHOLAR_BATCH_API,
      "rule": (
        "reject unresolved or reference-unavailable negatives, direct citation "
        "identity with a positive, edges in either direction, and candidates "
        "sharing at least "
        f"{SHARED_REFERENCE_REJECTION_THRESHOLD} cited papers with one positive work"
      ),
      "minimum_positive_reference_coverage": self.min_positive_coverage,
      "coverage": self.coverage.to_dict(),
      "accepted": len(self.accepted_ids),
      "rejected": len(self.rejected_ids),
      "rejection_counts": {
        key: rejection_counts[key] for key in sorted(rejection_counts)
      },
    }


def _resolved_by_work(
  identifiers_by_work: Mapping[str, Iterable[str]],
  resolutions: Mapping[str, str | None],
) -> dict[str, tuple[str, ...]]:
  result: dict[str, tuple[str, ...]] = {}
  for work_id in sorted(identifiers_by_work):
    paper_ids = {
      paper_id
      for identifier in identifiers_by_work[work_id]
      if (paper_id := resolutions.get(identifier))
    }
    result[work_id] = tuple(sorted(paper_ids))
  return result


def audit_negative_graph_distance(
  positive_identifiers: Mapping[str, Iterable[str]],
  negative_pmids: Mapping[str, str],
  *,
  client: SemanticScholarClient,
  min_positive_coverage: float = DEFAULT_MIN_POSITIVE_COVERAGE,
) -> CitationGraphAudit:
  """Reject negative candidates that are graph-adjacent to any positive work.

  Positive works can provide several identifiers because Semantic Scholar does
  not always merge a preprint with its version of record.  All resolved graph
  nodes are retained.  A negative must resolve from its PMID and have reference
  data; missing data never counts as evidence that a paper is distant.
  """

  if not 0.0 < min_positive_coverage <= 1.0:
    raise ValueError("min_positive_coverage must be greater than zero and at most one")
  if not positive_identifiers:
    raise ValueError("at least one positive work is required for a graph audit")

  normalized_positives: dict[str, tuple[str, ...]] = {}
  for work_id in sorted(positive_identifiers):
    normalized_positives[work_id] = tuple(
      sorted(
        {
          value.strip()
          for value in positive_identifiers[work_id]
          if value and value.strip()
        }
      )
    )
  normalized_negatives: dict[str, str] = {}
  for negative_id in sorted(negative_pmids):
    pmid = str(negative_pmids[negative_id]).strip()
    if not pmid.isdigit():
      raise ValueError(f"negative {negative_id} has invalid PMID {pmid!r}")
    normalized_negatives[negative_id] = pmid

  negative_identifiers = {
    negative_id: (f"PMID:{pmid}",)
    for negative_id, pmid in normalized_negatives.items()
  }
  all_identifiers = {
    identifier
    for values in (*normalized_positives.values(), *negative_identifiers.values())
    for identifier in values
  }
  resolutions = client.resolve_identifiers(all_identifiers)
  positive_papers = _resolved_by_work(normalized_positives, resolutions)
  negative_papers = _resolved_by_work(negative_identifiers, resolutions)
  all_paper_ids = {
    paper_id
    for values in (*positive_papers.values(), *negative_papers.values())
    for paper_id in values
  }
  nodes = client.fetch_nodes(all_paper_ids)

  def has_all_references(paper_ids: tuple[str, ...]) -> bool:
    return bool(paper_ids) and all(
      nodes.get(paper_id) is not None
      and nodes[paper_id].references_available  # type: ignore[union-attr]
      for paper_id in paper_ids
    )

  coverage = CitationGraphCoverage(
    positive_work_total=len(positive_papers),
    positive_work_resolved=sum(bool(values) for values in positive_papers.values()),
    positive_work_with_references=sum(
      has_all_references(values) for values in positive_papers.values()
    ),
    positive_paper_id_total=sum(len(values) for values in positive_papers.values()),
    positive_paper_id_with_references=sum(
      nodes.get(paper_id) is not None
      and nodes[paper_id].references_available  # type: ignore[union-attr]
      for values in positive_papers.values()
      for paper_id in values
    ),
    negative_work_total=len(negative_papers),
    negative_work_resolved=sum(bool(values) for values in negative_papers.values()),
    negative_work_with_references=sum(
      has_all_references(values) for values in negative_papers.values()
    ),
  )
  if coverage.positive_reference_coverage < min_positive_coverage:
    raise GraphCoverageError(coverage, min_positive_coverage)

  positive_paper_to_works: dict[str, set[str]] = {}
  positive_reference_to_works: dict[str, set[str]] = {}
  for work_id, paper_ids in positive_papers.items():
    for paper_id in paper_ids:
      positive_paper_to_works.setdefault(paper_id, set()).add(work_id)
      node = nodes.get(paper_id)
      if node is None or not node.references_available:
        continue
      for reference_id in node.references:
        positive_reference_to_works.setdefault(reference_id, set()).add(work_id)

  audits: dict[str, NegativeGraphAudit] = {}
  for negative_id in sorted(negative_papers):
    pmid = normalized_negatives[negative_id]
    paper_ids = negative_papers[negative_id]
    graph_available = has_all_references(paper_ids)
    references: set[str] = set()
    if graph_available:
      for paper_id in paper_ids:
        node = nodes[paper_id]
        assert node is not None
        references.update(node.references)

    same_works: set[str] = set()
    for paper_id in paper_ids:
      same_works.update(positive_paper_to_works.get(paper_id, ()))

    direct_works: set[str] = set()
    for cited_id in references:
      direct_works.update(positive_paper_to_works.get(cited_id, ()))
    for paper_id in paper_ids:
      direct_works.update(positive_reference_to_works.get(paper_id, ()))

    shared_reference_ids = references & positive_reference_to_works.keys()
    shared_by_work: dict[str, set[str]] = {}
    for reference_id in shared_reference_ids:
      for work_id in positive_reference_to_works[reference_id]:
        shared_by_work.setdefault(work_id, set()).add(reference_id)
    max_shared_reference_count = max(
      (len(values) for values in shared_by_work.values()),
      default=0,
    )
    coupled_works = {
      work_id
      for work_id, values in shared_by_work.items()
      if len(values) >= SHARED_REFERENCE_REJECTION_THRESHOLD
    }

    if not paper_ids:
      reason = "unresolved"
    elif not graph_available:
      reason = "references_unavailable"
    elif same_works:
      reason = "same_work"
    elif direct_works:
      reason = "direct_citation"
    elif coupled_works:
      reason = "shared_reference"
    else:
      reason = None
    audits[negative_id] = NegativeGraphAudit(
      negative_id=negative_id,
      pmid=pmid,
      paper_ids=paper_ids,
      references_available=graph_available,
      reference_count=len(references),
      accepted=reason is None,
      rejection_reason=reason,
      same_positive_work_ids=tuple(sorted(same_works)),
      direct_positive_work_ids=tuple(sorted(direct_works)),
      shared_positive_work_ids=tuple(sorted(coupled_works)),
      shared_reference_ids=tuple(sorted(shared_reference_ids)),
      max_shared_reference_count=max_shared_reference_count,
    )

  return CitationGraphAudit(audits, coverage, min_positive_coverage)
