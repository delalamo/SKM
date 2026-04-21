#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import subprocess
import sys
import unicodedata
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from migrate_note_citations_to_bibliography import split_content_and_defs
from reconcile_bibliography import (
  BARE_DOI_RE,
  BIB_PATH,
  CONTENT_DIR,
  FOOTNOTE_DEF_RE,
  RAW_DOI_RE,
  canonical_identity,
  normalize_target_to_identity,
  parse_bib_entries,
)

ORIGIN_REF = "origin/main"
OUTPUT_PATH = Path("/tmp/citation-audit-vs-main.json")
TARGET_DIRS = ("content/notes", "content/tags")
FOOTNOTE_REF_RE = re.compile(r"\[\^([A-Za-z0-9_-]+)\]")
PANDOC_KEY_RE = re.compile(r"(?<![\w/])@([A-Za-z0-9_-]+)")
WIKILINK_ALIAS_RE = re.compile(r"\[\[([^\]|]+)\|([^\]]*?\b(?:19|20)\d{2}[a-z]?[^\]]*)\]\]")
PLAIN_YEAR_WIKI_RE = re.compile(r"\[\[([^\]|]*\b(?:19|20)\d{2}[a-z]?[^\]]*)\]\]")
URL_RE = re.compile(r"https?://[^\s)>]+")
IMAGE_EXTENSIONS = (".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".avif", ".mp4", ".mov")
AUTHOR_YEAR_RE = re.compile(
  r"^(?P<author>.+?)(?:\s+et al\.?)?\s+(?P<year>(?:19|20)\d{2}[a-z]?)$",
  re.IGNORECASE,
)


@dataclass(frozen=True)
class CitationToken:
  start: int
  end: int
  kind: str
  raw: str
  identity: str | None

  @property
  def resolved(self) -> bool:
    return bool(self.identity)


def git(*args: str) -> bytes:
  return subprocess.check_output(["git", *args], cwd=CONTENT_DIR.parent)


def git_show_text(ref: str, path: str) -> str:
  result = subprocess.run(
    ["git", "show", f"{ref}:{path}"],
    cwd=CONTENT_DIR.parent,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    check=True,
  )
  return result.stdout.decode("utf-8", "replace")


def git_show_optional_text(ref: str, path: str) -> str | None:
  result = subprocess.run(
    ["git", "show", f"{ref}:{path}"],
    cwd=CONTENT_DIR.parent,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
  )
  if result.returncode != 0:
    return None
  return result.stdout.decode("utf-8", "replace")


def git_paths(ref: str, prefix: str) -> set[str]:
  result = subprocess.run(
    ["git", "-c", "core.quotepath=off", "ls-tree", "-r", "-z", "--name-only", ref, prefix],
    cwd=CONTENT_DIR.parent,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    check=True,
  )
  return {entry.decode("utf-8", "replace") for entry in result.stdout.split(b"\x00") if entry}


def current_paths() -> list[str]:
  paths: list[str] = []
  for directory in TARGET_DIRS:
    base = CONTENT_DIR.parent / directory
    if not base.exists():
      continue
    for path in sorted(base.rglob("*.md")):
      paths.append(path.relative_to(CONTENT_DIR.parent).as_posix())
  return paths


def map_to_origin_main(current_path: str, main_paths: set[str]) -> str | None:
  if current_path in main_paths:
    return current_path

  if current_path.startswith("content/notes/"):
    name = current_path.removeprefix("content/notes/")
    for candidate in (f"content/{name}", f"content/MOCs/{name}"):
      if candidate in main_paths:
        return candidate

  if current_path.startswith("content/tags/"):
    slug = current_path.removeprefix("content/tags/")
    candidate = f"content/MOCs/{slug}"
    if candidate in main_paths:
      return candidate

  return None


def build_bib_identity_map(bib_text: str) -> dict[str, str]:
  mapping: dict[str, str] = {}
  for entry in parse_bib_entries(bib_text):
    if entry.identity:
      mapping[entry.key] = entry.identity
  return mapping


def slugify_ascii(value: str) -> str:
  normalized = unicodedata.normalize("NFKD", value)
  ascii_value = normalized.encode("ascii", "ignore").decode("ascii")
  return re.sub(r"[^a-z0-9]+", "", ascii_value.lower())


def build_author_year_map(bib_text: str) -> dict[tuple[str, str], list[str]]:
  mapping: dict[tuple[str, str], list[str]] = {}
  for entry in parse_bib_entries(bib_text):
    author = entry.fields.get("author", "")
    year = entry.fields.get("year", "")
    if not author or not year:
      continue
    first_author = author.split(" and ", 1)[0]
    surname = first_author.split(",", 1)[0].strip()
    if not surname:
      continue
    mapping.setdefault((slugify_ascii(surname), year), []).append(entry.identity)
  return mapping


def choose_tokens(candidates: list[CitationToken]) -> list[CitationToken]:
  priorities = {
    "wikilink": 0,
    "plain-year-wikilink": 1,
    "footnote-ref": 2,
    "pandoc": 3,
    "raw-doi": 4,
    "raw-url": 5,
  }
  chosen: list[CitationToken] = []
  for token in sorted(candidates, key=lambda item: (item.start, item.end, priorities[item.kind])):
    if chosen and token.start < chosen[-1].end:
      continue
    chosen.append(token)
  return chosen


def is_image_like_reference(raw: str) -> bool:
  lowered = raw.strip().lower()
  if lowered.startswith("pasted-image-") or lowered.startswith("pasted image "):
    return True
  target = lowered.split("|", 1)[0]
  return target.endswith(IMAGE_EXTENSIONS)


def footnote_identities(text: str) -> dict[str, str]:
  identities: dict[str, str] = {}
  for match in FOOTNOTE_DEF_RE.finditer(text):
    key = match.group("key")
    body = match.group("body").strip()
    doi_match = RAW_DOI_RE.search(body) or BARE_DOI_RE.search(body)
    url_match = URL_RE.search(body)
    if doi_match:
      identities[key] = canonical_identity(doi_match.group(1), "")
    elif url_match:
      identities[key] = canonical_identity("", url_match.group(0))
  return identities


def resolve_author_year(raw: str, author_year_map: dict[tuple[str, str], list[str]]) -> str | None:
  match = AUTHOR_YEAR_RE.match(raw.strip())
  if not match:
    return None
  surname_text = match.group("author").strip().split()[-1]
  year = match.group("year")[:4]
  identities = author_year_map.get((slugify_ascii(surname_text), year), [])
  identities = sorted({identity for identity in identities if identity})
  if len(identities) == 1:
    return identities[0]
  return None


def extract_tokens(
  text: str,
  bib_identities: dict[str, str],
  author_year_map: dict[tuple[str, str], list[str]],
) -> list[CitationToken]:
  content, _defs = split_content_and_defs(text)
  footnote_map = footnote_identities(text)
  candidates: list[CitationToken] = []

  for match in WIKILINK_ALIAS_RE.finditer(content):
    target = match.group(1).strip()
    if is_image_like_reference(target):
      continue
    identity = normalize_target_to_identity(target) or None
    candidates.append(CitationToken(match.start(), match.end(), "wikilink", target, identity))

  for match in PLAIN_YEAR_WIKI_RE.finditer(content):
    raw = match.group(1).strip()
    if is_image_like_reference(raw):
      continue
    candidates.append(
      CitationToken(
        match.start(),
        match.end(),
        "plain-year-wikilink",
        raw,
        resolve_author_year(raw, author_year_map),
      )
    )

  for match in FOOTNOTE_REF_RE.finditer(content):
    key = match.group(1)
    candidates.append(
      CitationToken(
        match.start(),
        match.end(),
        "footnote-ref",
        key,
        footnote_map.get(key) or bib_identities.get(key),
      )
    )

  for match in PANDOC_KEY_RE.finditer(content):
    key = match.group(1)
    candidates.append(CitationToken(match.start(), match.end(), "pandoc", key, bib_identities.get(key)))

  for match in RAW_DOI_RE.finditer(content):
    raw = match.group(1)
    candidates.append(CitationToken(match.start(), match.end(), "raw-doi", raw, canonical_identity(raw, "")))

  for match in URL_RE.finditer(content):
    url = match.group(0)
    if "doi.org/" in url.lower():
      continue
    candidates.append(CitationToken(match.start(), match.end(), "raw-url", url, canonical_identity("", url)))

  return choose_tokens(candidates)


def resolved_identities(tokens: list[CitationToken]) -> list[str]:
  return [token.identity for token in tokens if token.identity]


def unresolved_tokens(tokens: list[CitationToken]) -> list[dict[str, str]]:
  return [
    {"kind": token.kind, "raw": token.raw}
    for token in tokens
    if not token.identity
  ]


def main() -> None:
  main_paths = git_paths(ORIGIN_REF, "content")
  current_bib = build_bib_identity_map(BIB_PATH.read_text())
  origin_bib_text = git_show_optional_text(ORIGIN_REF, "bibliography.bib")
  main_bib = build_bib_identity_map(origin_bib_text) if origin_bib_text else current_bib
  author_year_map = build_author_year_map(BIB_PATH.read_text())

  report: list[dict[str, object]] = []
  mismatches = 0
  manual_review = 0

  for current_path in current_paths():
    origin_path = map_to_origin_main(current_path, main_paths)
    if not origin_path:
      continue

    current_text = (CONTENT_DIR.parent / current_path).read_text()
    origin_text = git_show_text(ORIGIN_REF, origin_path)

    current_tokens = extract_tokens(current_text, current_bib, author_year_map)
    origin_tokens = extract_tokens(origin_text, main_bib, author_year_map)
    current_ids = resolved_identities(current_tokens)
    origin_ids = resolved_identities(origin_tokens)
    current_unresolved = unresolved_tokens(current_tokens)
    origin_unresolved = unresolved_tokens(origin_tokens)

    if not current_ids and not origin_ids and not current_unresolved and not origin_unresolved:
      continue

    status = "ok"
    if current_ids != origin_ids:
      status = "mismatch"
      mismatches += 1
    elif current_unresolved or origin_unresolved:
      status = "review"
      manual_review += 1

    report.append(
      {
        "status": status,
        "current_path": current_path,
        "origin_path": origin_path,
        "current_identities": current_ids,
        "origin_identities": origin_ids,
        "current_unresolved": current_unresolved,
        "origin_unresolved": origin_unresolved,
      }
    )

  OUTPUT_PATH.write_text(json.dumps(report, indent=2))

  print(f"files checked: {len(report)}")
  print(f"mismatches: {mismatches}")
  print(f"manual review: {manual_review}")
  for entry in report:
    if entry["status"] == "ok":
      continue
    print(f"{entry['status'].upper()}: {entry['current_path']} <= {entry['origin_path']}")
    print(f"  main ids: {entry['origin_identities']}")
    print(f"  curr ids: {entry['current_identities']}")
    if entry["origin_unresolved"]:
      print(f"  main unresolved: {entry['origin_unresolved']}")
    if entry["current_unresolved"]:
      print(f"  current unresolved: {entry['current_unresolved']}")


if __name__ == "__main__":
  main()
