"""BibTeX parsing and canonical training-corpus helpers for paperbot.

This module deliberately has no third-party dependencies.  It is used by both
the bibliography backfill command and the model freshness check, so its output
must remain stable across machines and Python patch releases.
"""

from __future__ import annotations

import hashlib
import html
import json
import re
import unicodedata
import urllib.parse
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Mapping, Sequence


DOI_RE = re.compile(r"10\.\d{4,9}/[^\s\]}>,;]+", re.IGNORECASE)
PMID_RE = re.compile(r"(?:pmid\s*[:/]?\s*|pubmed\.ncbi\.nlm\.nih\.gov/)(\d+)", re.IGNORECASE)
ARXIV_RE = re.compile(
  r"(?:arxiv\s*:\s*|arxiv\.org/(?:abs|pdf)/)"
  r"((?:[a-z-]+(?:\.[A-Z]{2})?/\d{7}|\d{4}\.\d{4,5}))(?:v\d+)?",
  re.IGNORECASE,
)
BARE_ARXIV_RE = re.compile(
  r"^(?:[a-z-]+(?:\.[A-Z]{2})?/\d{7}|\d{4}\.\d{4,5})(?:v\d+)?$",
  re.IGNORECASE,
)
CHEMRXIV_VERSION_RE = re.compile(
  r"(?P<base>10\.26434/[^\s]+?)(?:-v|/v)\d+$",
  re.IGNORECASE,
)
RELATION_FIELDS = {
  "relation",
  "related",
  "relateddoi",
  "related-doi",
  "related_doi",
  "preprint",
  "preprintdoi",
  "preprint_doi",
  "published",
  "publisheddoi",
  "published_doi",
}
PREPRINT_DOI_PREFIXES = (
  "doi:10.1101/",  # bioRxiv and medRxiv
  "doi:10.21203/rs.",  # Research Square
  "doi:10.26434/",  # ChemRxiv
  "doi:10.48550/arxiv.",
  "doi:10.64898/",  # current bioRxiv and medRxiv DOI prefix
)
DEFAULT_FIELD_ORDER = (
  "title",
  "author",
  "year",
  "journal",
  "booktitle",
  "publisher",
  "volume",
  "number",
  "pages",
  "abstract",
  "doi",
  "pmid",
  "eprint",
  "archiveprefix",
  "url",
)
ABSTRACT_TRAILER_RE = re.compile(
  r"\s+(?:competing interests?|conflicts? of interests?|author disclosures?)\s*[:.]\s*.*$",
  re.IGNORECASE | re.DOTALL,
)


@dataclass(frozen=True)
class BibliographyEntry:
  entry_type: str
  key: str
  fields: Mapping[str, str]

  @property
  def title(self) -> str:
    return self.fields.get("title", "").strip()

  @property
  def abstract(self) -> str:
    return normalize_abstract(self.fields.get("abstract", ""))


@dataclass(frozen=True)
class CanonicalWork:
  """One training example, possibly represented by several BibTeX entries."""

  work_id: str
  citekey: str
  aliases: tuple[str, ...]
  identifiers: tuple[str, ...]
  entry_type: str
  fields: Mapping[str, str]

  @property
  def title(self) -> str:
    return self.fields.get("title", "").strip()

  @property
  def abstract(self) -> str:
    return normalize_abstract(self.fields.get("abstract", ""))

  @property
  def year(self) -> str:
    return self.fields.get("year", "").strip()


class AbstractCompletenessError(ValueError):
  """Raised when a training work has no abstract and no explicit exception."""

  def __init__(self, missing: Sequence[CanonicalWork]) -> None:
    self.missing = tuple(missing)
    labels = ", ".join(work.citekey for work in self.missing[:10])
    if len(self.missing) > 10:
      labels += f", and {len(self.missing) - 10} more"
    super().__init__(f"Missing abstracts for {len(self.missing)} canonical works: {labels}")


def _unescape_bibtex(value: str) -> str:
  # Do not attempt a lossy general LaTeX conversion.  These substitutions only
  # remove braces used to preserve capitalization and common escaped symbols.
  value = value.replace(r"\&", "&").replace(r"\_", "_").replace(r"\%", "%")
  return value.replace("{", "").replace("}", "")


def normalize_abstract(value: str) -> str:
  """Return clean, single-line abstract text suitable for embedding."""

  if not value:
    return ""
  value = _unescape_percent(value)
  value = re.sub(r"(?is)<script.*?>.*?</script>|<style.*?>.*?</style>", " ", value)
  value = re.sub(r"(?s)<[^>]+>", " ", value)
  value = html.unescape(value)
  value = unicodedata.normalize("NFKC", value).replace("\xa0", " ")
  value = re.sub(r"\s+", " ", value).strip()
  value = ABSTRACT_TRAILER_RE.sub("", value).strip()
  return value


def normalize_doi(value: str) -> str:
  value = urllib.parse.unquote(html.unescape(value or "")).strip()
  value = re.sub(r"^(?:https?://)?(?:dx\.)?doi\.org/", "", value, flags=re.IGNORECASE)
  match = DOI_RE.search(value)
  value = match.group(0) if match else value
  value = value.rstrip(".,;:)]}").lower()
  # bioRxiv/medRxiv use one base DOI for all versions.
  value = re.sub(r"(10\.1101/[0-9.]+)v\d+$", r"\1", value, flags=re.IGNORECASE)
  # ChemRxiv has used both ``-vN`` and ``/vN`` suffixes for versions of the
  # same work. Match PaperRecord.canonical_id so bibliography versions cannot
  # receive duplicate positive training weight.
  if match := CHEMRXIV_VERSION_RE.fullmatch(value):
    value = match.group("base")
  return value


def normalize_arxiv_id(value: str) -> str:
  match = ARXIV_RE.search(value or "")
  if match:
    return match.group(1).lower()
  bare = (value or "").strip()
  if BARE_ARXIV_RE.fullmatch(bare):
    return re.sub(r"v\d+$", "", bare, flags=re.IGNORECASE).lower()
  return ""


def normalize_title(value: str) -> str:
  value = _unescape_bibtex(html.unescape(value or ""))
  value = unicodedata.normalize("NFKD", value)
  value = "".join(char for char in value if not unicodedata.combining(char))
  return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()


def _first_author_surname(value: str) -> str:
  first = re.split(r"\s+and\s+", value or "", maxsplit=1, flags=re.IGNORECASE)[0].strip()
  if not first:
    return ""
  surname = first.split(",", 1)[0] if "," in first else first.split()[-1]
  return re.sub(r"[^a-z0-9]+", "", _unescape_bibtex(surname).lower())


def parse_bibtex(text: str) -> list[BibliographyEntry]:
  """Parse ordinary braced/quoted BibTeX entries while preserving all fields."""

  entries: list[BibliographyEntry] = []
  cursor = 0
  while True:
    match = re.search(r"@(\w+)\s*([({])", text[cursor:], re.IGNORECASE)
    if not match:
      break
    entry_type = match.group(1).lower()
    open_delimiter = match.group(2)
    close_delimiter = "}" if open_delimiter == "{" else ")"
    body_start = cursor + match.end()
    end = _balanced_end(
      text, body_start, open_delimiter, close_delimiter, honor_top_level_quotes=True
    )
    body = text[body_start:end]
    cursor = end + 1
    if entry_type in {"comment", "preamble", "string"}:
      continue
    comma = _top_level_comma(body)
    if comma < 0:
      continue
    key = body[:comma].strip()
    if not key:
      continue
    entries.append(BibliographyEntry(entry_type, key, _parse_fields(body[comma + 1 :])))
  return entries


def _balanced_end(
  text: str,
  start: int,
  opener: str,
  closer: str,
  *,
  honor_top_level_quotes: bool = False,
) -> int:
  depth = 1
  quoted = False
  escaped = False
  for index in range(start, len(text)):
    char = text[index]
    if escaped:
      escaped = False
      continue
    if char == "\\":
      escaped = True
      continue
    # At entry scope, quotes delimit a quoted field only at depth one. Quotes
    # inside a braced value are ordinary abstract text. At braced-field scope
    # all quotes are ordinary text.
    if char == '"' and honor_top_level_quotes and depth == 1:
      quoted = not quoted
      continue
    if quoted:
      continue
    if char == opener:
      depth += 1
    elif char == closer:
      depth -= 1
      if depth == 0:
        return index
  raise ValueError("Unterminated BibTeX entry")


def _top_level_comma(value: str) -> int:
  brace_depth = 0
  quoted = False
  escaped = False
  for index, char in enumerate(value):
    if escaped:
      escaped = False
    elif char == "\\":
      escaped = True
    elif char == '"' and brace_depth == 0:
      quoted = not quoted
    elif not quoted and char == "{":
      brace_depth += 1
    elif not quoted and char == "}":
      brace_depth -= 1
    elif not quoted and brace_depth == 0 and char == ",":
      return index
  return -1


def _parse_fields(body: str) -> dict[str, str]:
  fields: dict[str, str] = {}
  index = 0
  while index < len(body):
    while index < len(body) and (body[index].isspace() or body[index] == ","):
      index += 1
    name_match = re.match(r"[A-Za-z][A-Za-z0-9_-]*", body[index:])
    if not name_match:
      break
    name = name_match.group(0).lower()
    index += name_match.end()
    while index < len(body) and body[index].isspace():
      index += 1
    if index >= len(body) or body[index] != "=":
      break
    index += 1
    while index < len(body) and body[index].isspace():
      index += 1
    value, index = _parse_field_value(body, index)
    fields[name] = html.unescape(value.strip())
  return fields


def _parse_field_value(body: str, index: int) -> tuple[str, int]:
  if index >= len(body):
    return "", index
  delimiter = body[index]
  if delimiter == "{":
    end = _balanced_end(body, index + 1, "{", "}")
    return body[index + 1 : end], end + 1
  if delimiter == '"':
    escaped = False
    result: list[str] = []
    index += 1
    while index < len(body):
      char = body[index]
      if char == '"' and not escaped:
        return "".join(result), index + 1
      result.append(char)
      escaped = char == "\\" and not escaped
      if char != "\\":
        escaped = False
      index += 1
    raise ValueError("Unterminated quoted BibTeX value")
  end = index
  while end < len(body) and body[end] not in ",\n\r":
    end += 1
  return body[index:end].strip(), end


def load_bibliography(path: Path | str) -> list[BibliographyEntry]:
  return parse_bibtex(Path(path).read_text(encoding="utf-8"))


def render_bibtex(entries: Iterable[BibliographyEntry]) -> str:
  return "\n\n".join(render_entry(entry) for entry in entries) + "\n"


def render_entry(entry: BibliographyEntry) -> str:
  fields = {name.lower(): str(value) for name, value in entry.fields.items()}
  ordered = [name for name in DEFAULT_FIELD_ORDER if fields.get(name, "").strip()]
  ordered.extend(sorted(name for name, value in fields.items() if name not in DEFAULT_FIELD_ORDER and value.strip()))
  lines = [f"@{entry.entry_type}{{{entry.key},"]
  for name in ordered:
    # Nested braces are valid BibTeX and preserve intentional capitalization.
    lines.append(f"  {name} = {{{_escape_percent(fields[name].strip())}}},")
  lines.append("}")
  return "\n".join(lines)


def _escape_percent(value: str) -> str:
  """Escape TeX comment characters without double-escaping existing ``\\%``."""

  output: list[str] = []
  for char in value:
    if char == "%":
      backslashes = 0
      for previous in reversed(output):
        if previous != "\\":
          break
        backslashes += 1
      if backslashes % 2 == 0:
        output.append("\\")
    output.append(char)
  return "".join(output)


def _unescape_percent(value: str) -> str:
  """Decode only the BibTeX percent escape for semantic model text."""

  output: list[str] = []
  for char in value:
    if char == "%":
      backslashes = 0
      for previous in reversed(output):
        if previous != "\\":
          break
        backslashes += 1
      if backslashes % 2 == 1:
        output.pop()
    output.append(char)
  return "".join(output)


def entry_identifiers(entry: BibliographyEntry) -> set[str]:
  fields = entry.fields
  identifiers: set[str] = set()
  doi = normalize_doi(fields.get("doi", ""))
  if doi:
    identifiers.add(f"doi:{doi}")
  pmid = re.sub(r"\D", "", fields.get("pmid", ""))
  if not pmid:
    match = PMID_RE.search(fields.get("url", ""))
    pmid = match.group(1) if match else ""
  if pmid:
    identifiers.add(f"pmid:{pmid}")
  arxiv = normalize_arxiv_id(" ".join(
    [fields.get("eprint", ""), fields.get("url", ""), fields.get("journal", ""), fields.get("note", "")]
  ))
  if arxiv:
    identifiers.add(f"arxiv:{arxiv}")
  for name in RELATION_FIELDS:
    for related_doi in DOI_RE.findall(fields.get(name, "")):
      identifiers.add(f"doi:{normalize_doi(related_doi)}")
    related_arxiv = normalize_arxiv_id(fields.get(name, ""))
    if related_arxiv:
      identifiers.add(f"arxiv:{related_arxiv}")
  return identifiers


def fallback_identity(entry: BibliographyEntry) -> str:
  title = normalize_title(entry.fields.get("title", ""))
  author = _first_author_surname(entry.fields.get("author", ""))
  year_match = re.search(r"(?:19|20)\d{2}", entry.fields.get("year", ""))
  if not title or not author or not year_match:
    return ""
  return f"title:{title}|author:{author}|year:{year_match.group(0)}"


def _preprint_match_identity(entry: BibliographyEntry) -> str:
  title = normalize_title(entry.fields.get("title", ""))
  author = _first_author_surname(entry.fields.get("author", ""))
  return f"title:{title}|author:{author}" if title and author else ""


def _has_preprint_identifier(identifiers: set[str]) -> bool:
  return any(
    identifier.startswith("arxiv:")
    or identifier.startswith(PREPRINT_DOI_PREFIXES)
    for identifier in identifiers
  )


def _is_preprint_publication_pair(left: set[str], right: set[str]) -> bool:
  if not left or not right or left & right:
    return False
  return {_identifier_stage(left), _identifier_stage(right)} == {
    "preprint",
    "publication",
  }


def _identifier_stage(identifiers: set[str]) -> str:
  """Classify one already-deduplicated identity component for safe bridging."""

  has_preprint = _has_preprint_identifier(identifiers)
  has_publication_doi = any(
    identifier.startswith("doi:")
    and not identifier.startswith(PREPRINT_DOI_PREFIXES)
    for identifier in identifiers
  )
  if has_preprint and has_publication_doi:
    return "mixed"
  if has_preprint:
    return "preprint"
  # A PMID-only bibliography record is ordinarily the publication side of a
  # preprint/publication pair. PMID is neutral when a preprint DOI is present.
  if has_publication_doi or any(
    identifier.startswith("pmid:") for identifier in identifiers
  ):
    return "publication"
  return ""


class _UnionFind:
  def __init__(self, size: int) -> None:
    self.parents = list(range(size))

  def find(self, index: int) -> int:
    while self.parents[index] != index:
      self.parents[index] = self.parents[self.parents[index]]
      index = self.parents[index]
    return index

  def union(self, left: int, right: int) -> None:
    left_root, right_root = self.find(left), self.find(right)
    if left_root != right_root:
      self.parents[max(left_root, right_root)] = min(left_root, right_root)


def canonicalize_entries(entries: Sequence[BibliographyEntry]) -> list[CanonicalWork]:
  """Merge duplicate entries without giving aliases duplicate training weight."""

  union = _UnionFind(len(entries))
  identities_by_entry = [entry_identifiers(entry) for entry in entries]
  owner: dict[str, int] = {}
  for index, identifiers in enumerate(identities_by_entry):
    for identifier in sorted(identifiers):
      if identifier in owner:
        union.union(index, owner[identifier])
      else:
        owner[identifier] = index

  # Link an arXiv/bioRxiv preprint to its version of record when the normalized
  # title and first author are exact.  Publication years commonly differ, so
  # this relation intentionally precedes the title/author/year fallback.
  publication_groups: dict[str, list[int]] = {}
  for index, entry in enumerate(entries):
    relation = _preprint_match_identity(entry)
    if not relation:
      continue
    publication_groups.setdefault(relation, []).append(index)
  publication_edges: set[tuple[int, int]] = set()
  for indexes in publication_groups.values():
    components = _component_identifiers(union, identities_by_entry, indexes)
    identified = [
      (root, identifiers)
      for root, identifiers in components.items()
      if identifiers
    ]
    # Exact title/author metadata can bridge one unambiguous preprint and one
    # publication. With more identified components, choosing a publication
    # would depend on input order and could collapse distinct strong IDs.
    if (
      len(identified) == 2
      and _is_preprint_publication_pair(identified[0][1], identified[1][1])
    ):
      publication_edges.add(tuple(sorted((identified[0][0], identified[1][0]))))
  publication_neighbors: dict[int, set[int]] = {}
  for left, right in publication_edges:
    publication_neighbors.setdefault(left, set()).add(right)
    publication_neighbors.setdefault(right, set()).add(left)
  for left, right in sorted(publication_edges):
    # A preprint component can appear under multiple historical titles. Merge
    # only one-to-one candidate edges so traversal/input order cannot choose
    # arbitrarily among several plausible versions of record.
    if (
      len(publication_neighbors[left]) == 1
      and len(publication_neighbors[right]) == 1
    ):
      union.union(left, right)

  # A title fallback can attach an identifier-less alias to an identified work,
  # but it must never merge two entries carrying conflicting strong identifiers.
  fallback_groups: dict[str, list[int]] = {}
  for index, entry in enumerate(entries):
    fallback = fallback_identity(entry)
    if not fallback:
      continue
    fallback_groups.setdefault(fallback, []).append(index)
  for indexes in fallback_groups.values():
    components = _component_identifiers(union, identities_by_entry, indexes)
    identified_roots = [
      root for root, identifiers in components.items() if identifiers
    ]
    identifierless_roots = [
      root for root, identifiers in components.items() if not identifiers
    ]
    if len(identified_roots) == 1:
      destination = identified_roots[0]
      for root in identifierless_roots:
        union.union(destination, root)
    elif not identified_roots and identifierless_roots:
      destination, *duplicates = identifierless_roots
      for root in duplicates:
        union.union(destination, root)
    elif len(identifierless_roots) > 1:
      # Preserve duplicate identifier-less aliases as one unresolved work, but
      # do not arbitrarily attach that work to one of several conflicting IDs.
      destination, *duplicates = identifierless_roots
      for root in duplicates:
        union.union(destination, root)

  grouped: dict[int, list[int]] = {}
  for index in range(len(entries)):
    grouped.setdefault(union.find(index), []).append(index)

  works: list[CanonicalWork] = []
  for indexes in grouped.values():
    component = [entries[index] for index in indexes]
    aliases = tuple(sorted(entry.key for entry in component))
    identifiers = tuple(sorted(set().union(*(identities_by_entry[index] for index in indexes))))
    merged = _merge_fields(component)
    work_id = _choose_work_id(identifiers, component)
    entry_type = sorted(component, key=lambda entry: (-_entry_richness(entry), entry.key))[0].entry_type
    works.append(CanonicalWork(work_id, aliases[0], aliases, identifiers, entry_type, merged))
  return sorted(works, key=lambda work: (work.work_id, work.citekey))


def _component_identifiers(
  union: _UnionFind,
  identities_by_entry: Sequence[set[str]],
  indexes: Sequence[int],
) -> dict[int, set[str]]:
  """Return strong identifiers accumulated by each current union component."""

  wanted_roots = {union.find(index) for index in indexes}
  components = {root: set() for root in wanted_roots}
  for index, identifiers in enumerate(identities_by_entry):
    root = union.find(index)
    if root in components:
      components[root].update(identifiers)
  return components


def _entry_richness(entry: BibliographyEntry) -> int:
  return sum(bool(str(value).strip()) for value in entry.fields.values()) + (10 if entry.abstract else 0)


def _merge_fields(entries: Sequence[BibliographyEntry]) -> dict[str, str]:
  ranked = sorted(entries, key=lambda entry: (-_entry_richness(entry), entry.key))
  names = sorted(set().union(*(entry.fields.keys() for entry in ranked)))
  merged: dict[str, str] = {}
  for name in names:
    values = [str(entry.fields.get(name, "")).strip() for entry in ranked if str(entry.fields.get(name, "")).strip()]
    if values:
      merged[name] = max(values, key=len) if name == "abstract" else values[0]
  if "abstract" in merged:
    merged["abstract"] = normalize_abstract(merged["abstract"])
  return merged


def _choose_work_id(identifiers: Sequence[str], entries: Sequence[BibliographyEntry]) -> str:
  doi_candidates = sorted(
    identifier for identifier in identifiers
    if identifier.startswith("doi:") and not identifier.startswith("doi:10.1101/")
  )
  if doi_candidates:
    return doi_candidates[0]
  for prefix in ("doi:", "pmid:", "arxiv:"):
    candidates = sorted(identifier for identifier in identifiers if identifier.startswith(prefix))
    if candidates:
      return candidates[0]
  fallback = next((fallback_identity(entry) for entry in entries if fallback_identity(entry)), "")
  payload = fallback or "|".join(sorted(entry.key for entry in entries))
  return "fallback:" + hashlib.sha256(payload.encode("utf-8")).hexdigest()[:24]


def load_title_only_exceptions(path: Path | str | None) -> dict[str, str]:
  if path is None or not Path(path).exists():
    return {}
  payload = json.loads(Path(path).read_text(encoding="utf-8"))
  if isinstance(payload, dict) and payload.get("schema_version") == 1:
    payload = payload.get("entries", {})
  if not isinstance(payload, dict) or not all(isinstance(key, str) and isinstance(value, str) and value.strip() for key, value in payload.items()):
    raise ValueError("Title-only exceptions must be a JSON object of identifier-to-reason strings")
  return payload


def missing_abstracts(
  works: Sequence[CanonicalWork],
  exceptions: Mapping[str, str] | None = None,
) -> list[CanonicalWork]:
  exceptions = exceptions or {}
  return [
    work for work in works
    if not work.abstract
    and work.work_id not in exceptions
    and work.citekey not in exceptions
    and not any(alias in exceptions for alias in work.aliases)
  ]


def require_abstracts(
  works: Sequence[CanonicalWork],
  exceptions: Mapping[str, str] | None = None,
) -> None:
  missing = missing_abstracts(works, exceptions)
  if missing:
    raise AbstractCompletenessError(missing)


def embedding_input_hash(title: str, abstract: str) -> str:
  payload = normalize_title(title) + "\x1f" + normalize_abstract(abstract)
  return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def semantic_bibliography_hash(
  works: Sequence[CanonicalWork],
  exceptions: Mapping[str, str] | None = None,
) -> str:
  exceptions = exceptions or {}
  payload = []
  for work in sorted(works, key=lambda item: item.work_id):
    exception = exceptions.get(work.work_id) or exceptions.get(work.citekey) or next(
      (exceptions[alias] for alias in work.aliases if alias in exceptions), ""
    )
    if work.abstract:
      exception = ""
    payload.append({
      "work_id": work.work_id,
      "citekey": work.citekey,
      "aliases": list(work.aliases),
      "title": normalize_title(work.title),
      "abstract": work.abstract,
      "title_only_reason": exception,
    })
  encoded = json.dumps(payload, ensure_ascii=False, separators=(",", ":"), sort_keys=True).encode("utf-8")
  return hashlib.sha256(encoded).hexdigest()
