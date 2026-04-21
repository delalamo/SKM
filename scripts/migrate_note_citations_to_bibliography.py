#!/usr/bin/env python3
"""
migrate_note_citations_to_bibliography.py

Bulk-convert paper-style Markdown footnote citations in `content/**/*.md`
into Pandoc citations backed by a central `bibliography.bib`.

Rules:
- Citation-like footnotes are footnote definitions that contain a DOI or URL.
- Ordinary explanatory footnotes are preserved in-place.
- Existing citekeys are preserved when they are globally unambiguous.
- Conflicting citekeys are disambiguated from parsed author/year/title metadata.
- When the same title appears with multiple identities (for example preprint and
  published versions), the higher-quality record is preferred for BibTeX output.

Usage:
    python3 scripts/migrate_note_citations_to_bibliography.py [--dry-run]
"""

from __future__ import annotations

from dataclasses import dataclass
import html
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from utils import REPO_ROOT

CONTENT_DIR = REPO_ROOT / "content"
BIB_PATH = REPO_ROOT / "bibliography.bib"

FM_RE = re.compile(r"\A---\n.*?\n---\n", re.DOTALL)
FOOTNOTE_START_RE = re.compile(r"^\[\^(?P<key>[A-Za-z0-9_-]+)\]:")
DOI_RE = re.compile(r"10\.\d{4,9}/[^\s)>]+", re.IGNORECASE)
URL_RE = re.compile(r"https?://[^\s)>]+", re.IGNORECASE)
TITLE_RE = re.compile(r'"([^"]+)"')
JOURNAL_ITALIC_RE = re.compile(r"\*([^*]+)\*")
PLACEHOLDER_RE = re.compile(r"<<CITE:([A-Za-z0-9_-]+)>>")
PLACEHOLDER_CLUSTER_RE = re.compile(
  r"<<CITE:[A-Za-z0-9_-]+>>(?:[ \t]*(?:,|;|and|&)?[ \t]*<<CITE:[A-Za-z0-9_-]+>>)+"
)
PANDOC_CITATION_CLUSTER_RE = re.compile(r"\[@[A-Za-z0-9_-]+(?:;\s*@[A-Za-z0-9_-]+)+\]")
PANDOC_CITEKEY_RE = re.compile(r"@([A-Za-z0-9_-]+)")

STOPWORDS = {
  "a",
  "an",
  "and",
  "are",
  "as",
  "at",
  "by",
  "for",
  "from",
  "in",
  "into",
  "of",
  "on",
  "or",
  "the",
  "to",
  "using",
  "with",
}
SURNAME_PREFIXES = (
  "da ",
  "de ",
  "del ",
  "della ",
  "der ",
  "di ",
  "du ",
  "la ",
  "le ",
  "monteiro da ",
  "van ",
  "von ",
)


@dataclass
class FootnoteDef:
  key: str
  raw_lines: list[str]
  body: str
  is_citation: bool


@dataclass
class CitationRecord:
  file_path: Path
  original_key: str
  body: str
  title: str
  title_norm: str
  author_raw: str
  year: str
  venue: str
  doi: str
  url: str


def normalize_whitespace(value: str) -> str:
  return " ".join(value.split())


def slugify(value: str) -> str:
  value = unicodedata.normalize("NFKD", value)
  value = value.encode("ascii", "ignore").decode("ascii")
  value = value.lower()
  value = re.sub(r"[^a-z0-9]+", "", value)
  return value


def split_frontmatter_and_body(text: str) -> tuple[str, str]:
  match = FM_RE.match(text)
  if match:
    return text[: match.end()], text[match.end() :]
  return "", text


def footnote_body_from_lines(lines: list[str]) -> str:
  first = lines[0].split(":", 1)[1].strip()
  extras = [line.strip() for line in lines[1:] if line.strip()]
  return normalize_whitespace(" ".join([first, *extras]))


def split_content_and_defs(body: str) -> tuple[str, list[FootnoteDef]]:
  lines = body.splitlines()
  start_idx = None
  for idx, line in enumerate(lines):
    if FOOTNOTE_START_RE.match(line):
      start_idx = idx
      break

  if start_idx is None:
    return body.rstrip() + ("\n" if body else ""), []

  content = "\n".join(lines[:start_idx]).rstrip() + "\n"
  def_lines = lines[start_idx:]

  defs: list[FootnoteDef] = []
  current_lines: list[str] = []
  current_key: str | None = None

  def flush_current() -> None:
    nonlocal current_key, current_lines
    if current_key is None:
      return
    body = html.unescape(footnote_body_from_lines(current_lines))
    is_citation = bool(DOI_RE.search(body) or URL_RE.search(body))
    defs.append(
      FootnoteDef(
        key=current_key,
        raw_lines=current_lines[:],
        body=body,
        is_citation=is_citation,
      )
    )
    current_key = None
    current_lines = []

  for line in def_lines:
    match = FOOTNOTE_START_RE.match(line)
    if match:
      flush_current()
      current_key = match.group("key")
      current_lines = [line]
    else:
      current_lines.append(line)
  flush_current()

  return content, defs


def extract_title(body: str) -> str:
  match = TITLE_RE.search(body)
  if match:
    return normalize_whitespace(html.unescape(match.group(1)))
  return ""


def extract_author(body: str) -> str:
  match = re.search(r"^(.*?)\s*\((\d{4}[a-z]?)\)", body)
  if match:
    return normalize_whitespace(match.group(1).strip().rstrip("."))
  return ""


def extract_year(body: str) -> str:
  match = re.search(r"\((\d{4})[a-z]?\)", body)
  if match:
    return match.group(1)
  return ""


def extract_venue(body: str, title: str) -> str:
  italic_match = JOURNAL_ITALIC_RE.search(body)
  if italic_match:
    return normalize_whitespace(html.unescape(italic_match.group(1)))

  if not title:
    return ""

  after_title = body.split(f'"{title}"', 1)[-1]
  after_title = URL_RE.sub("", after_title)
  after_title = DOI_RE.sub("", after_title)
  after_title = after_title.replace("*", " ")
  after_title = normalize_whitespace(after_title.strip(" ."))
  if not after_title:
    return ""

  # Prefer concise venue-like fragments rather than full sentences.
  if len(after_title) <= 80 and not after_title.lower().startswith("available from"):
    return after_title
  return ""


def extract_doi(body: str) -> str:
  match = DOI_RE.search(body)
  if match:
    return match.group(0).rstrip(".,")
  return ""


def extract_url(body: str, doi: str) -> str:
  if doi:
    return f"https://doi.org/{doi}"
  match = URL_RE.search(body)
  if match:
    return match.group(0).rstrip(".,")
  return ""


def to_record(path: Path, definition: FootnoteDef) -> CitationRecord:
  title = extract_title(definition.body)
  doi = extract_doi(definition.body)
  url = extract_url(definition.body, doi)
  return CitationRecord(
    file_path=path,
    original_key=definition.key,
    body=definition.body,
    title=title,
    title_norm=normalize_whitespace(title).lower(),
    author_raw=extract_author(definition.body),
    year=extract_year(definition.body),
    venue=extract_venue(definition.body, title),
    doi=doi,
    url=url,
  )


def citation_identity(record: CitationRecord) -> str:
  if record.title_norm:
    return f"title:{record.title_norm}"
  if record.doi:
    return f"doi:{record.doi.lower()}"
  if record.url:
    return f"url:{record.url.lower()}"
  return f"body:{record.body.lower()}"


def is_preprint(record: CitationRecord) -> bool:
  doi = record.doi.lower()
  url = record.url.lower()
  venue = record.venue.lower()
  return (
    doi.startswith("10.1101/")
    or "arxiv" in doi
    or "arxiv" in url
    or "biorxiv" in venue
    or "openreview.net" in url
  )


def record_quality(record: CitationRecord) -> tuple[int, int, int]:
  score = 0
  if record.venue:
    score += 4
  if record.url:
    score += 1
  if record.doi:
    score += 2
  if not is_preprint(record):
    score += 3
  return (
    score,
    len(record.venue),
    len(record.doi or record.url),
  )


def read_existing_bib_keys() -> set[str]:
  return set(read_existing_bib_entries())


def read_existing_bib_entries() -> dict[str, str]:
  if not BIB_PATH.exists():
    return {}

  entries: dict[str, str] = {}
  current_lines: list[str] = []
  depth = 0

  for line in BIB_PATH.read_text("utf-8").splitlines():
    if not current_lines:
      if re.match(r"^@\w+\{[^,]+,", line):
        current_lines = [line]
        depth = line.count("{") - line.count("}")
      continue

    current_lines.append(line)
    depth += line.count("{") - line.count("}")
    if depth <= 0:
      entry = "\n".join(current_lines).strip()
      match = re.match(r"^@\w+\{([^,]+),", current_lines[0])
      if match:
        entries[match.group(1)] = entry
      current_lines = []
      depth = 0

  return entries


def extract_bib_field(entry: str, field_name: str) -> str:
  match = re.search(rf"^\s*{re.escape(field_name)}\s*=\s*\{{(.*)\}},?$", entry, re.MULTILINE)
  if not match:
    return ""
  return normalize_whitespace(html.unescape(match.group(1).strip()))


def existing_entry_matches_record(entry: str, record: CitationRecord) -> bool:
  existing_title = extract_bib_field(entry, "title").lower()
  existing_doi = extract_bib_field(entry, "doi").lower()
  existing_url = extract_bib_field(entry, "url").lower()

  if record.doi and existing_doi and record.doi.lower() == existing_doi:
    return True
  if record.url and existing_url and record.url.lower() == existing_url:
    return True
  if record.title_norm and existing_title and record.title_norm == existing_title:
    return True
  return False


def find_matching_existing_key(
  existing_entries: dict[str, str], records: list[CitationRecord]
) -> str | None:
  for key, entry in existing_entries.items():
    if any(existing_entry_matches_record(entry, record) for record in records):
      return key
  return None


def build_record_index() -> tuple[
  dict[Path, list[FootnoteDef]],
  dict[str, list[CitationRecord]],
  dict[str, str],
]:
  file_defs: dict[Path, list[FootnoteDef]] = {}
  groups: dict[str, list[CitationRecord]] = defaultdict(list)

  for path in sorted(CONTENT_DIR.rglob("*.md")):
    _, body = split_frontmatter_and_body(path.read_text("utf-8"))
    _, defs = split_content_and_defs(body)
    file_defs[path] = defs
    for definition in defs:
      if definition.is_citation:
        record = to_record(path, definition)
        groups[citation_identity(record)].append(record)

  existing_entries = read_existing_bib_entries()
  existing_keys = set(existing_entries)
  key_to_groups: dict[str, set[str]] = defaultdict(set)
  group_key_counts: dict[str, Counter[str]] = {}

  for identity, records in groups.items():
    counter = Counter(record.original_key for record in records)
    group_key_counts[identity] = counter
    for key in counter:
      key_to_groups[key].add(identity)

  conflicted_keys = {key for key, ids in key_to_groups.items() if len(ids) > 1}
  used_keys: set[str] = set(existing_keys)
  canonical_keys: dict[str, str] = {}

  for identity, records in sorted(groups.items()):
    counter = group_key_counts[identity]
    candidate_keys = list(counter.keys())

    matching_existing_key = find_matching_existing_key(existing_entries, records)
    if matching_existing_key is not None:
      canonical_keys[identity] = matching_existing_key
      continue

    existing_candidates = [
      key
      for key in candidate_keys
      if key in existing_keys
      and key not in conflicted_keys
      and existing_entry_matches_record(existing_entries[key], records[0])
    ]
    if existing_candidates:
      chosen = sorted(
        existing_candidates,
        key=lambda key: (-counter[key], len(key), key),
      )[0]
      canonical_keys[identity] = chosen
      used_keys.add(chosen)
      continue

    unique_candidates = [
      key for key in candidate_keys if key not in conflicted_keys and key not in existing_keys
    ]
    if unique_candidates:
      chosen = sorted(
        unique_candidates,
        key=lambda key: (-counter[key], len(key), key),
      )[0]
      canonical_keys[identity] = chosen
      used_keys.add(chosen)
      continue

    canonical_keys[identity] = generate_key(records[0], used_keys)

  return file_defs, groups, canonical_keys


def generate_key(record: CitationRecord, used_keys: set[str]) -> str:
  author_root = extract_author_root(record)
  year = record.year or "ref"
  base = f"{author_root}{year}" if author_root else f"ref{year}"

  if base and base not in used_keys:
    used_keys.add(base)
    return base

  title_words = significant_title_words(record.title)
  candidate = base
  for word in title_words:
    candidate = f"{candidate}{word}"
    if candidate not in used_keys:
      used_keys.add(candidate)
      return candidate

  suffix = ord("a")
  while True:
    candidate = f"{base}{chr(suffix)}"
    if candidate not in used_keys:
      used_keys.add(candidate)
      return candidate
    suffix += 1


def extract_author_root(record: CitationRecord) -> str:
  raw = record.author_raw.strip()
  if not raw:
    return "ref"

  parts = re.split(r"\s+(?:&|and)\s+|\s+et al\.?", raw, maxsplit=1, flags=re.IGNORECASE)
  author = parts[0].strip()
  return slugify(author) or "ref"


def significant_title_words(title: str) -> list[str]:
  words = []
  for token in re.findall(r"[A-Za-z0-9]+", unicodedata.normalize("NFKD", title).lower()):
    if token in STOPWORDS or len(token) <= 2:
      continue
    slug = slugify(token)
    if slug:
      words.append(slug)
  return words


def format_author_field(author_raw: str) -> str:
  raw = normalize_whitespace(html.unescape(author_raw).rstrip("."))
  if not raw:
    return "Unknown"
  # Treat the entire display string as a literal author so bibliography output
  # preserves citation-style names like "Gurev et al." or "Stein & Mchaourab".
  return "{" + raw + "}"


def bib_escape(value: str) -> str:
  return value.replace("\\", "\\\\")


def bib_entry_type(record: CitationRecord) -> str:
  venue = record.venue.lower()
  if venue:
    return "article"
  return "misc"


def build_bib_entry(key: str, records: list[CitationRecord]) -> str:
  record = max(records, key=record_quality)
  entry_type = bib_entry_type(record)
  fields = [
    ("title", record.title or record.body),
    ("author", format_author_field(record.author_raw) or "Unknown"),
    ("year", record.year or "0000"),
  ]

  if record.venue:
    fields.append(("journal", record.venue))
  if record.doi:
    fields.append(("doi", record.doi))
  if record.url:
    fields.append(("url", record.url))

  lines = [f"@{entry_type}{{{key},"]
  for field_name, value in fields:
    lines.append(f"  {field_name} = {{{bib_escape(value)}}},")
  lines[-1] = lines[-1].rstrip(",")
  lines.append("}")
  return "\n".join(lines)


def placeholder_for(key: str) -> str:
  return f"<<CITE:{key}>>"


def collapse_placeholder_cluster(match: re.Match[str]) -> str:
  keys: list[str] = []
  seen: set[str] = set()
  for key in PLACEHOLDER_RE.findall(match.group(0)):
    if key not in seen:
      seen.add(key)
      keys.append(key)
  if len(keys) == 1:
    return f"[@{keys[0]}]"
  return "[@" + "; @".join(keys) + "]"


def replace_reference_style_citations(content: str, key_map: dict[str, str]) -> str:
  for original_key, canonical_key in key_map.items():
    pattern = re.compile(
      rf"(?<!\[)\[(?!\^)([^\[\]\n]+)\]\[\^{re.escape(original_key)}\]"
    )
    content = pattern.sub(rf"\1 {placeholder_for(canonical_key)}", content)
  return content


def replace_footnote_refs(content: str, key_map: dict[str, str]) -> str:
  for original_key, canonical_key in key_map.items():
    content = re.sub(
      rf"\[\^{re.escape(original_key)}\]",
      placeholder_for(canonical_key),
      content,
    )
  return content


def render_pandoc_citations(content: str) -> str:
  content = PLACEHOLDER_CLUSTER_RE.sub(collapse_placeholder_cluster, content)
  content = PLACEHOLDER_RE.sub(lambda m: f"[@{m.group(1)}]", content)
  return content


def sort_pandoc_citation_clusters(content: str) -> str:
  first_seen: dict[str, int] = {}
  for index, match in enumerate(PANDOC_CITEKEY_RE.finditer(content)):
    key = match.group(1)
    if key not in first_seen:
      first_seen[key] = index

  def reorder_cluster(match: re.Match[str]) -> str:
    seen: set[str] = set()
    keys: list[str] = []
    for key in PANDOC_CITEKEY_RE.findall(match.group(0)):
      if key not in seen:
        seen.add(key)
        keys.append(key)
    ordered = sorted(keys, key=lambda key: first_seen.get(key, sys.maxsize))
    return "[@" + "; @".join(ordered) + "]"

  return PANDOC_CITATION_CLUSTER_RE.sub(reorder_cluster, content)


def rebuild_file(frontmatter: str, content: str, defs: list[FootnoteDef]) -> str:
  rebuilt = frontmatter + content.rstrip() + "\n"
  if defs:
    rebuilt += "\n"
    rebuilt += "\n".join("\n".join(definition.raw_lines).rstrip() for definition in defs) + "\n"
  return rebuilt


def migrate_file(
  path: Path,
  definitions: list[FootnoteDef],
  canonical_keys: dict[str, str],
  dry_run: bool,
) -> tuple[bool, int]:
  original = path.read_text("utf-8")
  frontmatter, body = split_frontmatter_and_body(original)
  content, _defs = split_content_and_defs(body)

  citation_key_map = {}
  kept_defs = []
  removed_citation_defs = 0

  for definition in definitions:
    if definition.is_citation:
      record = to_record(path, definition)
      citation_key_map[definition.key] = canonical_keys[citation_identity(record)]
      removed_citation_defs += 1
    else:
      kept_defs.append(definition)

  if not citation_key_map:
    return False, 0

  updated_content = replace_reference_style_citations(content, citation_key_map)
  updated_content = replace_footnote_refs(updated_content, citation_key_map)
  updated_content = render_pandoc_citations(updated_content)
  updated_content = sort_pandoc_citation_clusters(updated_content)

  updated = rebuild_file(frontmatter, updated_content, kept_defs)
  changed = updated != original
  if changed and not dry_run:
    path.write_text(updated, "utf-8")
  return changed, removed_citation_defs


def write_bibliography(
  groups: dict[str, list[CitationRecord]],
  canonical_keys: dict[str, str],
  dry_run: bool,
) -> int:
  entries = read_existing_bib_entries()
  for identity, records in groups.items():
    key = canonical_keys[identity]
    if key not in entries:
      entries[key] = build_bib_entry(key, records)

  bibliography = "\n\n".join(entries[key] for key in sorted(entries)) + "\n"
  if not dry_run:
    BIB_PATH.write_text(bibliography, "utf-8")
  return len(entries)


def main() -> None:
  dry_run = "--dry-run" in sys.argv[1:]

  file_defs, groups, canonical_keys = build_record_index()
  changed_files = 0
  removed_defs = 0

  bib_entries = write_bibliography(groups, canonical_keys, dry_run)

  for path, definitions in sorted(file_defs.items()):
    changed, removed = migrate_file(path, definitions, canonical_keys, dry_run)
    if changed:
      changed_files += 1
      print(f"  ✓  {path.name}")
    removed_defs += removed

  mode = "Would update" if dry_run else "Updated"
  print(
    f"\n{mode} {changed_files} content file(s), removed {removed_defs} citation footnote "
    f"definition(s), and wrote {bib_entries} bibliography entr{'y' if bib_entries == 1 else 'ies'}."
  )


if __name__ == "__main__":
  main()
