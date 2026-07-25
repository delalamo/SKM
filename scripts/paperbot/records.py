"""Canonical paper records and deterministic cross-provider identity handling.

The feed adapters deliberately retain provider-specific identifiers, while this
module supplies the small common vocabulary used by ranking and issue
reconciliation. Identifiers and declared relationships are preferred. Metadata
fallbacks require a normalized full title and first author, with narrow,
fail-closed year bridging for complementary preprint/publication records.
"""

from __future__ import annotations

import hashlib
import html
import json
import re
import unicodedata
from dataclasses import dataclass, field, replace
from datetime import UTC, date, datetime
from typing import Any, Iterable, Mapping, Sequence


DOI_RE = re.compile(r"10\.\d{4,9}/[^\s\]}>\"']+", re.IGNORECASE)
ARXIV_RE = re.compile(
  r"(?:[a-z][a-z0-9.-]*/\d{7}|\d{4}\.\d{4,5})(?:v(?P<version>\d+))?",
  re.IGNORECASE,
)
CHEMRXIV_VERSION_RE = re.compile(
  r"(?P<base>10\.26434/[^\s]+?)(?:-v|/v)(?P<version>\d+)$", re.IGNORECASE
)
TAG_RE = re.compile(r"<[^>]+>")
WHITESPACE_RE = re.compile(r"\s+")
ABSTRACT_TRAILER_RE = re.compile(
  r"\s+(?:(?:competing interests?|conflicts? of interests?|author disclosures?)"
  r"\s*[:.]|TOC\s+Figure\s+O_FIG\b).*$",
  re.IGNORECASE | re.DOTALL,
)
PREPRINT_DOI_PREFIXES = (
  "10.1101/",  # bioRxiv and medRxiv
  "10.21203/rs.",  # Research Square
  "10.26434/chemrxiv",  # ChemRxiv
  "10.48550/arxiv.",
  "10.64898/",  # current bioRxiv and medRxiv DOI prefix
)
GENERIC_TITLES = {
  "not available",
  "not applicable",
  "no title",
  "title unavailable",
  "untitled",
}
CORRECTION_TITLE_PREFIXES = (
  "correction ",
  "corrigendum ",
  "erratum ",
  "expression of concern ",
  "retraction ",
)
PREPRINT_PUBLICATION_YEAR_GAP = 2


def clean_text(value: Any) -> str:
  """Collapse provider markup and whitespace without changing semantics."""

  text = html.unescape(str(value or ""))
  text = TAG_RE.sub(" ", text)
  return WHITESPACE_RE.sub(" ", text).strip()


def clean_abstract(value: Any) -> str:
  """Clean paper text and remove only unmistakable non-abstract trailers."""

  text = clean_text(value).replace(r"\%", "%")
  return ABSTRACT_TRAILER_RE.sub("", text).strip()


def normalize_doi(value: Any) -> str:
  text = clean_text(value).casefold()
  text = re.sub(r"^(?:https?://)?(?:dx\.)?doi\.org/", "", text)
  text = re.sub(r"^doi\s*:\s*", "", text)
  match = DOI_RE.search(text)
  return match.group(0).rstrip(".,;:)") if match else ""


def normalize_pmid(value: Any) -> str:
  text = clean_text(value)
  text = re.sub(
    r"^(?:https?://)?(?:www\.)?pubmed\.ncbi\.nlm\.nih\.gov/", "", text, flags=re.I
  )
  text = re.sub(r"^(?:pmid|pubmed)\s*:\s*", "", text, flags=re.I)
  match = re.fullmatch(r"(\d+)(?:/.*)?", text)
  return match.group(1) if match else ""


def normalize_arxiv_id(value: Any) -> str:
  text = clean_text(value)
  text = re.sub(
    r"^(?:https?://)?(?:export\.|www\.)?arxiv\.org/(?:abs|pdf)/", "", text, flags=re.I
  )
  text = re.sub(r"^arxiv\s*:\s*", "", text, flags=re.I)
  text = re.sub(r"^10\.48550/arxiv\.", "", text, flags=re.I)
  text = re.sub(r"\.pdf$", "", text, flags=re.I)
  match = ARXIV_RE.fullmatch(text)
  if not match:
    return ""
  return re.sub(r"v\d+$", "", match.group(0), flags=re.I).casefold()


def arxiv_version(value: Any) -> str:
  text = clean_text(value)
  match = ARXIV_RE.search(text)
  return match.group("version") if match and match.group("version") else ""


def chemrxiv_version(value: Any) -> str:
  doi = normalize_doi(value)
  match = CHEMRXIV_VERSION_RE.fullmatch(doi)
  return match.group("version") if match else ""


def normalize_title(value: Any) -> str:
  text = unicodedata.normalize("NFKD", clean_text(value).casefold())
  text = "".join(character for character in text if not unicodedata.combining(character))
  return WHITESPACE_RE.sub(" ", re.sub(r"[^a-z0-9]+", " ", text)).strip()


def _normalize_name(value: str) -> str:
  text = unicodedata.normalize("NFKD", clean_text(value).casefold())
  text = "".join(character for character in text if not unicodedata.combining(character))
  return re.sub(r"[^a-z0-9]+", "", text)


def first_author_key(authors: Sequence[str]) -> str:
  if not authors:
    return ""
  author = clean_text(authors[0])
  if not author:
    return ""
  if "," in author:
    family = author.split(",", 1)[0]
  else:
    pieces = author.split()
    while pieces and pieces[-1].casefold().rstrip(".") in {"jr", "sr", "ii", "iii", "iv"}:
      pieces.pop()
    family = pieces[-1] if pieces else ""
  return _normalize_name(family)


def ensure_utc(value: datetime | date | str | None) -> datetime | None:
  """Parse provider dates and always return an aware UTC datetime."""

  if value is None or value == "":
    return None
  if isinstance(value, datetime):
    parsed = value
  elif isinstance(value, date):
    parsed = datetime(value.year, value.month, value.day, tzinfo=UTC)
  else:
    text = clean_text(value)
    if not text:
      return None
    if text.endswith("Z"):
      text = f"{text[:-1]}+00:00"
    try:
      parsed = datetime.fromisoformat(text)
    except ValueError:
      parsed = datetime.strptime(text[:10], "%Y-%m-%d")
  if parsed.tzinfo is None:
    parsed = parsed.replace(tzinfo=UTC)
  return parsed.astimezone(UTC)


def _source_name(value: str) -> str:
  return re.sub(r"[^a-z0-9]+", "-", clean_text(value).casefold()).strip("-")


def _chemrxiv_family_doi(doi: str) -> str:
  match = CHEMRXIV_VERSION_RE.fullmatch(doi)
  return match.group("base") if match else ""


def identifier_alias(value: Any, *, default_source: str = "") -> str:
  """Return a namespaced identity token for a DOI, PMID, arXiv ID, or source ID."""

  text = clean_text(value)
  if not text:
    return ""
  prefix_match = re.fullmatch(r"(doi|pmid|arxiv|[a-z][a-z0-9-]*):(.*)", text, flags=re.I)
  if prefix_match:
    prefix, raw = prefix_match.groups()
    prefix = prefix.casefold()
    if prefix == "doi":
      normalized = normalize_doi(raw)
    elif prefix == "pmid":
      normalized = normalize_pmid(raw)
    elif prefix == "arxiv":
      normalized = normalize_arxiv_id(raw)
    else:
      normalized = clean_text(raw).casefold()
    return f"{prefix}:{normalized}" if normalized else ""
  doi = normalize_doi(text)
  if doi:
    return f"doi:{doi}"
  pmid = normalize_pmid(text)
  if pmid:
    return f"pmid:{pmid}"
  arxiv_id = normalize_arxiv_id(text)
  if arxiv_id:
    return f"arxiv:{arxiv_id}"
  source = _source_name(default_source)
  return f"{source}:{text.casefold()}" if source else ""


@dataclass(frozen=True, slots=True)
class PaperRecord:
  """Provider-neutral metadata for one version of one scholarly work."""

  source: str
  source_id: str
  title: str
  abstract: str
  authors: tuple[str, ...] = ()
  venue: str = ""
  created_at: datetime | None = None
  updated_at: datetime | None = None
  url: str = ""
  doi: str = ""
  pmid: str = ""
  arxiv_id: str = ""
  version: str = ""
  categories: tuple[str, ...] = ()
  related_ids: tuple[str, ...] = ()
  license: str = ""
  metadata: Mapping[str, Any] = field(default_factory=dict, compare=False, repr=False)

  def __post_init__(self) -> None:
    source = _source_name(self.source)
    source_id = clean_text(self.source_id)
    title = clean_text(self.title)
    if not source:
      raise ValueError("paper source is required")
    if not source_id:
      raise ValueError("paper source_id is required")
    if not title:
      raise ValueError("paper title is required")
    object.__setattr__(self, "source", source)
    object.__setattr__(self, "source_id", source_id)
    object.__setattr__(self, "title", title)
    object.__setattr__(self, "abstract", clean_abstract(self.abstract))
    object.__setattr__(self, "authors", tuple(clean_text(item) for item in self.authors if clean_text(item)))
    object.__setattr__(self, "venue", clean_text(self.venue))
    object.__setattr__(self, "created_at", ensure_utc(self.created_at))
    object.__setattr__(self, "updated_at", ensure_utc(self.updated_at))
    object.__setattr__(self, "url", clean_text(self.url))
    object.__setattr__(self, "doi", normalize_doi(self.doi))
    object.__setattr__(self, "pmid", normalize_pmid(self.pmid))
    object.__setattr__(self, "arxiv_id", normalize_arxiv_id(self.arxiv_id))
    object.__setattr__(self, "version", clean_text(self.version))
    object.__setattr__(
      self, "categories", tuple(sorted({clean_text(item) for item in self.categories if clean_text(item)}))
    )
    aliases = {
      alias
      for item in self.related_ids
      if (alias := identifier_alias(item, default_source=source))
    }
    object.__setattr__(self, "related_ids", tuple(sorted(aliases)))
    object.__setattr__(self, "license", clean_text(self.license))
    object.__setattr__(self, "metadata", dict(self.metadata))

  @property
  def year(self) -> int | None:
    publication_year = self.metadata.get("publication_year")
    if publication_year is not None:
      match = re.search(r"(?:19|20)\d{2}", str(publication_year))
      if match:
        return int(match.group(0))
    timestamp = self.created_at or self.updated_at
    return timestamp.year if timestamp else None

  @property
  def title_alias(self) -> str:
    title = normalize_title(self.title)
    author = first_author_key(self.authors)
    if not title or not author or self.year is None:
      return ""
    digest = hashlib.sha256(f"{title}\0{author}\0{self.year}".encode()).hexdigest()[:24]
    return f"title:{digest}"

  @property
  def canonical_id(self) -> str:
    family_doi = _chemrxiv_family_doi(self.doi)
    if family_doi:
      return f"doi:{family_doi}"
    if self.doi:
      return f"doi:{self.doi}"
    if self.pmid:
      return f"pmid:{self.pmid}"
    if self.arxiv_id:
      return f"arxiv:{self.arxiv_id}"
    return f"{self.source}:{self.source_id.casefold()}"

  def identity_aliases(self, *, include_title: bool = True) -> frozenset[str]:
    aliases = set(self.related_ids)
    for alias in tuple(aliases):
      if alias.startswith("doi:") and (family := _chemrxiv_family_doi(alias[4:])):
        aliases.add(f"doi:{family}")
    if self.doi:
      aliases.add(f"doi:{self.doi}")
      if family := _chemrxiv_family_doi(self.doi):
        aliases.add(f"doi:{family}")
    if self.pmid:
      aliases.add(f"pmid:{self.pmid}")
    if self.arxiv_id:
      aliases.add(f"arxiv:{self.arxiv_id}")
    aliases.add(f"{self.source}:{self.source_id.casefold()}")
    if include_title and self.title_alias:
      aliases.add(self.title_alias)
    return frozenset(aliases)

  @property
  def metadata_hash(self) -> str:
    """Hash fields whose changes warrant updating an existing issue."""

    payload = self.to_dict()
    payload.pop("metadata", None)
    encoded = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(encoded.encode()).hexdigest()

  def to_dict(self) -> dict[str, Any]:
    return {
      "source": self.source,
      "source_id": self.source_id,
      "canonical_id": self.canonical_id,
      "title": self.title,
      "abstract": self.abstract,
      "authors": list(self.authors),
      "venue": self.venue,
      "created_at": self.created_at.isoformat() if self.created_at else "",
      "updated_at": self.updated_at.isoformat() if self.updated_at else "",
      "url": self.url,
      "doi": self.doi,
      "pmid": self.pmid,
      "arxiv_id": self.arxiv_id,
      "version": self.version,
      "categories": list(self.categories),
      "related_ids": list(self.related_ids),
      "license": self.license,
      "metadata": dict(self.metadata),
    }

  @classmethod
  def from_dict(cls, value: Mapping[str, Any]) -> PaperRecord:
    return cls(
      source=str(value.get("source", "")),
      source_id=str(value.get("source_id", "")),
      title=str(value.get("title", "")),
      abstract=str(value.get("abstract", "")),
      authors=tuple(value.get("authors", ()) or ()),
      venue=str(value.get("venue", "")),
      created_at=ensure_utc(value.get("created_at")),
      updated_at=ensure_utc(value.get("updated_at")),
      url=str(value.get("url", "")),
      doi=str(value.get("doi", "")),
      pmid=str(value.get("pmid", "")),
      arxiv_id=str(value.get("arxiv_id", "")),
      version=str(value.get("version", "")),
      categories=tuple(value.get("categories", ()) or ()),
      related_ids=tuple(value.get("related_ids", ()) or ()),
      license=str(value.get("license", "")),
      metadata=dict(value.get("metadata", {}) or {}),
    )


class _DisjointSet:
  def __init__(self, size: int):
    self.parent = list(range(size))

  def find(self, item: int) -> int:
    while self.parent[item] != item:
      self.parent[item] = self.parent[self.parent[item]]
      item = self.parent[item]
    return item

  def union(self, left: int, right: int) -> None:
    left_root, right_root = self.find(left), self.find(right)
    if left_root != right_root:
      self.parent[right_root] = left_root


def _version_number(value: str) -> int:
  match = re.search(r"\d+", value)
  return int(match.group(0)) if match else 0


def _timestamp_value(value: datetime | None) -> float:
  return value.timestamp() if value else float("-inf")


def _latest_key(record: PaperRecord) -> tuple[float, int, int, int, int, str]:
  return (
    _timestamp_value(record.updated_at or record.created_at),
    int(record.metadata.get("record_kind") == "publication-relation"),
    _version_number(record.version),
    int(bool(record.abstract)),
    len(record.abstract),
    record.canonical_id,
  )


def _preferred_doi(records: Sequence[PaperRecord]) -> str:
  dois = {record.doi for record in records if record.doi}
  if not dois:
    return ""
  # Prefer a version-of-record DOI to an arXiv/preprint DOI, then sort for
  # independence from provider order.
  def rank(doi: str) -> tuple[int, str]:
    return int(_is_preprint_doi(doi)), doi

  return min(dois, key=rank)


def _is_preprint_doi(doi: str) -> bool:
  return doi.startswith(PREPRINT_DOI_PREFIXES)


def _title_author_key(record: PaperRecord) -> tuple[str, str] | None:
  """Return the exact metadata fallback key, rejecting inherently ambiguous titles."""

  title = normalize_title(record.title)
  author = first_author_key(record.authors)
  if not title or not author or title in GENERIC_TITLES:
    return None
  if title.startswith(CORRECTION_TITLE_PREFIXES):
    return None
  return title, author


def _component_identity(records: Sequence[PaperRecord]) -> dict[str, set[str] | set[int]]:
  preprints: set[str] = set()
  publications: set[str] = set()
  pmids: set[str] = set()
  years: set[int] = set()
  for record in records:
    if record.doi:
      target = preprints if _is_preprint_doi(record.doi) else publications
      target.add(f"doi:{record.doi}")
    if record.arxiv_id:
      preprints.add(f"arxiv:{record.arxiv_id}")
    if record.pmid:
      pmids.add(record.pmid)
    if record.year is not None:
      years.add(record.year)
  return {
    "preprints": preprints,
    "publications": publications,
    "pmids": pmids,
    "years": years,
  }


def _roots_by_component(
  values: Sequence[PaperRecord], groups: _DisjointSet
) -> dict[int, list[PaperRecord]]:
  components: dict[int, list[PaperRecord]] = {}
  for index, record in enumerate(values):
    components.setdefault(groups.find(index), []).append(record)
  return components


def _union_strict_title_matches(
  values: Sequence[PaperRecord], groups: _DisjointSet
) -> None:
  """Apply title/author/year fallback unless strong identifiers conflict."""

  components = _roots_by_component(values, groups)
  buckets: dict[tuple[str, str, int], set[int]] = {}
  for root, records in components.items():
    for record in records:
      key = _title_author_key(record)
      if key is not None and record.year is not None:
        buckets.setdefault((*key, record.year), set()).add(root)

  for roots in buckets.values():
    if len(roots) < 2:
      continue
    identities = [_component_identity(components[root]) for root in roots]
    # A strict metadata fallback can bridge providers and identifier-less
    # records, but it must not conflate two distinct journal articles,
    # preprints, or PubMed records with the same title.
    for field in ("preprints", "publications", "pmids"):
      combined = set().union(*(identity[field] for identity in identities))
      if len(combined) > 1:
        break
    else:
      first, *rest = sorted(roots)
      for root in rest:
        groups.union(first, root)


def _year_sets_within(left: set[int], right: set[int], gap: int) -> bool:
  return bool(left and right) and min(abs(a - b) for a in left for b in right) <= gap


def _union_preprint_publication_matches(
  values: Sequence[PaperRecord], groups: _DisjointSet
) -> None:
  """Bridge an unambiguous preprint/publication pair across nearby years.

  Provider publication-relation metadata remains the primary mechanism. This
  narrow fallback covers delayed or missing relationship data seen in the live
  feeds: the normalized full title and first author must be identical, exactly
  two unmatched components may exist, and their identifier roles must be
  complementary. Ambiguous buckets fail closed.
  """

  components = _roots_by_component(values, groups)
  buckets: dict[tuple[str, str], set[int]] = {}
  for root, records in components.items():
    for record in records:
      if key := _title_author_key(record):
        buckets.setdefault(key, set()).add(root)

  candidate_edges: set[tuple[int, int]] = set()
  for roots in buckets.values():
    if len(roots) != 2:
      continue
    left_root, right_root = sorted(roots)
    left = _component_identity(components[left_root])
    right = _component_identity(components[right_root])
    left_preprint = bool(left["preprints"])
    right_preprint = bool(right["preprints"])
    left_publication = bool(left["publications"] or left["pmids"])
    right_publication = bool(right["publications"] or right["pmids"])

    cross_stage = (
      left_preprint
      and not right_preprint
      and right_publication
      and not left["publications"]
    ) or (
      right_preprint
      and not left_preprint
      and left_publication
      and not right["publications"]
    )
    if cross_stage and _year_sets_within(
      left["years"], right["years"], PREPRINT_PUBLICATION_YEAR_GAP
    ):
      candidate_edges.add((left_root, right_root))
      continue

    # PubMed occasionally lacks a DOI while a provider's publication record
    # has it. An adjacent-year DOI/PMID complement is similarly unambiguous.
    doi_pmid_complement = (
      bool(left["publications"])
      and not left["pmids"]
      and not left_preprint
      and bool(right["pmids"])
      and not right["publications"]
      and not right_preprint
    ) or (
      bool(right["publications"])
      and not right["pmids"]
      and not right_preprint
      and bool(left["pmids"])
      and not left["publications"]
      and not left_preprint
    )
    if doi_pmid_complement and _year_sets_within(left["years"], right["years"], 1):
      candidate_edges.add((left_root, right_root))

  neighbors: dict[int, set[int]] = {}
  for left_root, right_root in candidate_edges:
    neighbors.setdefault(left_root, set()).add(right_root)
    neighbors.setdefault(right_root, set()).add(left_root)
  for left_root, right_root in sorted(candidate_edges):
    # A component may retain several historical titles. Refuse to let bucket
    # iteration order select one of multiple plausible cross-stage matches.
    if len(neighbors[left_root]) == 1 and len(neighbors[right_root]) == 1:
      groups.union(left_root, right_root)


def _merge_group(records: Sequence[PaperRecord]) -> PaperRecord:
  latest = max(records, key=_latest_key)
  created = min((record.created_at for record in records if record.created_at), default=None)
  updated = max((record.updated_at for record in records if record.updated_at), default=None)
  doi = _preferred_doi(records)
  pmid = min((record.pmid for record in records if record.pmid), default="")
  arxiv_id = min((record.arxiv_id for record in records if record.arxiv_id), default="")
  abstract = latest.abstract or max((record.abstract for record in records), key=len, default="")
  authors = latest.authors or max((record.authors for record in records), key=len, default=())
  categories = tuple(sorted({item for record in records for item in record.categories}))
  related = {item for record in records for item in record.related_ids}
  for record in records:
    related.update(record.identity_aliases(include_title=False))
  primary_tokens = {
    f"doi:{doi}" if doi else "",
    f"pmid:{pmid}" if pmid else "",
    f"arxiv:{arxiv_id}" if arxiv_id else "",
    f"{latest.source}:{latest.source_id.casefold()}",
  }
  related.difference_update(primary_tokens)
  metadata = dict(latest.metadata)
  publication_records = [
    record
    for record in records
    if record.metadata.get("record_kind") == "publication-relation"
  ]
  publication = max(publication_records, key=_latest_key) if publication_records else None
  if publication and publication.metadata.get("publication_year"):
    metadata["publication_year"] = publication.metadata["publication_year"]
  if len(records) > 1:
    metadata["merged_sources"] = sorted({record.source for record in records})
  return replace(
    latest,
    abstract=abstract,
    authors=authors,
    venue=(publication.venue if publication and publication.venue else latest.venue)
    or next((record.venue for record in records if record.venue), ""),
    created_at=created,
    updated_at=updated,
    doi=doi,
    pmid=pmid,
    arxiv_id=arxiv_id,
    categories=categories,
    related_ids=tuple(sorted(related)),
    license=latest.license or next((record.license for record in records if record.license), ""),
    url=publication.url if publication and publication.url else latest.url,
    metadata=metadata,
  )


def deduplicate_records(records: Iterable[PaperRecord]) -> list[PaperRecord]:
  """Transitively merge exact identities and conservative metadata fallbacks."""

  values = list(records)
  if not values:
    return []
  groups = _DisjointSet(len(values))
  owner: dict[str, int] = {}
  for index, record in enumerate(values):
    for alias in sorted(record.identity_aliases(include_title=False)):
      if alias in owner:
        groups.union(index, owner[alias])
      else:
        owner[alias] = index
  _union_strict_title_matches(values, groups)
  _union_preprint_publication_matches(values, groups)
  grouped: dict[int, list[PaperRecord]] = {}
  for index, record in enumerate(values):
    grouped.setdefault(groups.find(index), []).append(record)
  merged = [_merge_group(group) for group in grouped.values()]
  return sorted(merged, key=lambda record: (record.canonical_id, record.metadata_hash))


__all__ = [
  "PaperRecord",
  "arxiv_version",
  "chemrxiv_version",
  "clean_abstract",
  "clean_text",
  "deduplicate_records",
  "ensure_utc",
  "first_author_key",
  "identifier_alias",
  "normalize_arxiv_id",
  "normalize_doi",
  "normalize_pmid",
  "normalize_title",
]
