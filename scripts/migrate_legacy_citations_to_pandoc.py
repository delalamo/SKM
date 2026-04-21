#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from migrate_note_citations_to_bibliography import split_content_and_defs, split_frontmatter_and_body
from reconcile_bibliography import (
  BARE_DOI_RE,
  CONTENT_DIR,
  RAW_DOI_RE,
  canonical_doi,
  canonical_identity,
  normalize_target_to_identity,
)

DOI_TOKEN_PATTERN = r"10\.\d{4,9}/[^\s\]>*()]+(?:\([^)]+\)[^\s\]>*()]*)*"
PLACEHOLDER_RE = re.compile(r"<<CITE:([A-Za-z0-9_-]+)>>")
FOOTNOTE_REF_RE = re.compile(r"\[\^([A-Za-z0-9_-]+)\]")
WIKILINK_RE = re.compile(r"\[\[([^\]|]+)\|([^\]]*?\b(?:19|20)\d{2}[a-z]?[^\]]*)\]\]")
PAREN_RAW_DOI_RE = re.compile(rf"\(\s*(?:https?://)?doi\.org/({DOI_TOKEN_PATTERN})\s*\)", re.IGNORECASE)
PAREN_BARE_DOI_RE = re.compile(rf"\(\s*({DOI_TOKEN_PATTERN})\s*\)", re.IGNORECASE)
PURE_PARENS_PLACEHOLDER_RE = re.compile(
  r"\(\s*(<<CITE:[A-Za-z0-9_-]+>>(?:\s*(?:,|;|and|&)\s*<<CITE:[A-Za-z0-9_-]+>>)*?)\s*\)"
)
PLACEHOLDER_CLUSTER_RE = re.compile(
  r"<<CITE:[A-Za-z0-9_-]+>>(?:\s*(?:,|;|and|&)\s*<<CITE:[A-Za-z0-9_-]+>>)+"
)
AUTHOR_YEAR_ALIAS_RE = re.compile(r"^(?P<author>.+?)\s+(?P<year>(?:19|20)\d{2}[a-z]?)$")
PANDOC_CITEKEY_RE = re.compile(r"(?<![\w/])@([A-Za-z0-9_-]+)")
ADJACENT_CITATIONS_RE = re.compile(r"\[@([A-Za-z0-9_-]+)\]\s*\[@([A-Za-z0-9_-]+)\]")
ADJACENT_CITATION_GROUPS_RE = re.compile(
  r"(\[@[A-Za-z0-9_-]+(?:; @[A-Za-z0-9_-]+)*\])\s+(\[@[A-Za-z0-9_-]+(?:; @[A-Za-z0-9_-]+)*\])"
)
AUTHOR_YEAR_BRACKET_WITH_CITATION_RE = re.compile(
  r"\[[^\[\]]*?(?:19|20)\d{2}[a-z]?[^]]*\]\s*(\[@[A-Za-z0-9_-]+(?:; @[A-Za-z0-9_-]+)*\])"
)
DOUBLE_BRACKET_CITATION_RE = re.compile(r"\[\[(@[A-Za-z0-9_-]+)\]\]")
PURE_PAREN_CITATION_GROUP_RE = re.compile(r"\((\[@[A-Za-z0-9_-]+(?:; @[A-Za-z0-9_-]+)*\])\)")


@dataclass
class MigrationMaps:
  identity_to_key: dict[str, str]
  key_aliases: dict[str, str]
  footnote_key_to_key: dict[str, str]


def load_maps(path: Path) -> MigrationMaps:
  payload = json.loads(path.read_text())
  identity_to_key = payload["identity_to_key"]
  key_aliases = payload.get("key_aliases", {})

  footnote_targets: dict[str, set[str]] = defaultdict(set)
  for identity, target in payload.get("legacy_targets", {}).items():
    canonical_key = identity_to_key.get(identity)
    if not canonical_key:
      continue
    for footnote_key in target.get("footnote_keys", {}):
      footnote_targets[footnote_key].add(canonical_key)

  footnote_key_to_key = {
    footnote_key: next(iter(keys))
    for footnote_key, keys in footnote_targets.items()
    if len(keys) == 1
  }

  for citekey in identity_to_key.values():
    footnote_key_to_key.setdefault(citekey, citekey)

  for key, alias_target in key_aliases.items():
    if key not in footnote_key_to_key:
      footnote_key_to_key[key] = alias_target

  return MigrationMaps(
    identity_to_key=identity_to_key,
    key_aliases=key_aliases,
    footnote_key_to_key=footnote_key_to_key,
  )


def placeholder(key: str) -> str:
  return f"<<CITE:{key}>>"


def normalize_identity_from_body(body: str) -> str:
  doi_match = RAW_DOI_RE.search(body) or BARE_DOI_RE.search(body)
  if doi_match:
    return canonical_identity(doi_match.group(1), "")
  url_match = re.search(r"https?://[^\s)]+", body)
  if url_match:
    return canonical_identity("", url_match.group(0))
  return ""


def is_caption_like(line: str) -> bool:
  lowered = line.lower()
  return any(token in lowered for token in ("figure from", "table from", "ref ", "reference "))


def previous_nonspace_char(text: str, index: int) -> str:
  cursor = index - 1
  while cursor >= 0 and text[cursor].isspace():
    cursor -= 1
  return text[cursor] if cursor >= 0 else ""


def next_nonspace_char(text: str, index: int) -> str:
  cursor = index
  while cursor < len(text) and text[cursor].isspace():
    cursor += 1
  return text[cursor] if cursor < len(text) else ""


def author_text_from_alias(alias: str) -> str | None:
  match = AUTHOR_YEAR_ALIAS_RE.match(alias.strip())
  if not match:
    return None
  author_text = match.group("author").strip()
  author_text = re.sub(r"\bet al\b", "et al.", author_text)
  return author_text


def collapse_placeholders(text: str) -> str:
  def build_cluster(raw: str) -> str:
    keys: list[str] = []
    seen: set[str] = set()
    for key in PLACEHOLDER_RE.findall(raw):
      if key in seen:
        continue
      seen.add(key)
      keys.append(key)
    if not keys:
      return raw
    if len(keys) == 1:
      return f"[@{keys[0]}]"
    return "[" + "; ".join(f"@{key}" for key in keys) + "]"

  updated = PURE_PARENS_PLACEHOLDER_RE.sub(lambda match: build_cluster(match.group(1)), text)
  updated = PLACEHOLDER_CLUSTER_RE.sub(lambda match: build_cluster(match.group(0)), updated)
  return PLACEHOLDER_RE.sub(lambda match: f"[@{match.group(1)}]", updated)


def replace_alias_citations(text: str, key_aliases: dict[str, str]) -> str:
  def repl(match: re.Match[str]) -> str:
    key = match.group(1)
    return "@" + key_aliases.get(key, key)

  return PANDOC_CITEKEY_RE.sub(repl, text)


def merge_citation_groups(left: str, right: str) -> str:
  keys: list[str] = []
  seen: set[str] = set()
  for key in re.findall(r"@([A-Za-z0-9_-]+)", left + " " + right):
    if key in seen:
      continue
    seen.add(key)
    keys.append(key)
  return "[" + "; ".join(f"@{key}" for key in keys) + "]"


def normalize_inline_citations(text: str) -> str:
  updated = text
  while True:
    collapsed = ADJACENT_CITATIONS_RE.sub(r"[@\1; @\2]", updated)
    if collapsed == updated:
      break
    updated = collapsed

  while True:
    collapsed = ADJACENT_CITATION_GROUPS_RE.sub(
      lambda match: merge_citation_groups(match.group(1), match.group(2)),
      updated,
    )
    if collapsed == updated:
      break
    updated = collapsed

  updated = DOUBLE_BRACKET_CITATION_RE.sub(r"[\1]", updated)
  updated = AUTHOR_YEAR_BRACKET_WITH_CITATION_RE.sub(r"\1", updated)
  updated = PURE_PAREN_CITATION_GROUP_RE.sub(r"\1", updated)
  updated = re.sub(r"(?<=[A-Za-z0-9\]\)\*.,;:])\[@", " [@", updated)
  return updated


def replace_raw_dois(line: str, maps: MigrationMaps, failures: list[str], path: Path) -> str:
  def repl(match: re.Match[str]) -> str:
    raw = match.group(1)
    identity = canonical_identity(canonical_doi(raw), "")
    citekey = maps.identity_to_key.get(identity)
    if not citekey:
      failures.append(f"{path}: missing bibliography entry for DOI {raw}")
      return match.group(0)
    return placeholder(citekey)

  updated = PAREN_RAW_DOI_RE.sub(repl, line)
  updated = PAREN_BARE_DOI_RE.sub(repl, updated)
  updated = RAW_DOI_RE.sub(repl, updated)
  return BARE_DOI_RE.sub(repl, updated)


def should_render_as_citation_only(text: str, start: int, end: int) -> bool:
  prev_char = previous_nonspace_char(text, start)
  next_char = next_nonspace_char(text, end)
  prefix = text[:start].rstrip().lower()

  if prev_char in "([;,":
    return True
  if next_char in "),.;]":
    return True
  if re.search(r"(?:^|\b)(by|from|per|via|see)\s+$", prefix[-24:]):
    return True
  return False


def replace_wikilinks(line: str, maps: MigrationMaps, failures: list[str], path: Path, citation_only: bool) -> str:
  result: list[str] = []
  cursor = 0
  for match in WIKILINK_RE.finditer(line):
    target, alias = match.group(1), match.group(2).strip()
    identity = normalize_target_to_identity(target)
    if not identity:
      continue
    citekey = maps.identity_to_key.get(identity)
    if not citekey:
      failures.append(f"{path}: missing bibliography entry for target {target}")
      continue

    result.append(line[cursor : match.start()])
    if citation_only or should_render_as_citation_only(line, match.start(), match.end()):
      result.append(placeholder(citekey))
    else:
      author_text = author_text_from_alias(alias)
      if author_text:
        result.append(f"{author_text} {placeholder(citekey)}")
      else:
        result.append(f"{alias} {placeholder(citekey)}")
    cursor = match.end()

  if cursor == 0:
    return line
  result.append(line[cursor:])
  return "".join(result)


def render_non_citation_defs(defs: list) -> str:
  if not defs:
    return ""
  return "\n".join("\n".join(defn.raw_lines) for defn in defs)


def process_file(path: Path, maps: MigrationMaps, dry_run: bool, failures: list[str]) -> bool:
  original = path.read_text()
  frontmatter, body = split_frontmatter_and_body(original)
  content, defs = split_content_and_defs(body)

  local_citation_defs: dict[str, str] = {}
  non_citation_defs = []
  local_defined_keys = {definition.key for definition in defs}

  for definition in defs:
    if definition.is_citation:
      identity = normalize_identity_from_body(definition.body)
      citekey = maps.identity_to_key.get(identity)
      if not citekey:
        citekey = maps.footnote_key_to_key.get(definition.key)
      if not citekey:
        failures.append(f"{path}: could not resolve footnote definition ^{definition.key}")
        continue
      local_citation_defs[definition.key] = citekey
    else:
      non_citation_defs.append(definition)

  def replace_footnotes(match: re.Match[str]) -> str:
    key = match.group(1)
    if key in local_citation_defs:
      return placeholder(local_citation_defs[key])
    if key not in local_defined_keys and key in maps.footnote_key_to_key:
      return placeholder(maps.footnote_key_to_key[key])
    return match.group(0)

  updated_content = FOOTNOTE_REF_RE.sub(replace_footnotes, content)
  updated_content = replace_alias_citations(updated_content, maps.key_aliases)

  rewritten_lines = []
  for line in updated_content.splitlines():
    citation_only = is_caption_like(line)
    line = replace_raw_dois(line, maps, failures, path)
    line = replace_wikilinks(line, maps, failures, path, citation_only)
    rewritten_lines.append(line)

  updated_content = "\n".join(rewritten_lines)
  updated_content = collapse_placeholders(updated_content)
  updated_content = normalize_inline_citations(updated_content)
  updated_content = re.sub(r"[ \t]{2,}", " ", updated_content)
  updated_content = updated_content.rstrip() + "\n"

  rendered_defs = render_non_citation_defs(non_citation_defs)
  final = frontmatter + updated_content
  if rendered_defs:
    final = final.rstrip() + "\n\n" + rendered_defs.rstrip() + "\n"

  if final == original:
    return False

  if not dry_run:
    path.write_text(final)
  return True


def main() -> None:
  parser = argparse.ArgumentParser()
  parser.add_argument(
    "--map",
    type=Path,
    default=Path("/tmp/reconcile-map.json"),
    help="Path to the JSON map emitted by reconcile_bibliography.py",
  )
  parser.add_argument("--dry-run", action="store_true")
  args = parser.parse_args()

  maps = load_maps(args.map)
  failures: list[str] = []
  changed = 0

  for path in sorted(CONTENT_DIR.rglob("*.md")):
    if process_file(path, maps, args.dry_run, failures):
      changed += 1

  print(f"changed files: {changed}")
  print(f"failures: {len(failures)}")
  if failures:
    for failure in failures[:200]:
      print(f"  {failure}")
    if len(failures) > 200:
      print(f"  ... {len(failures) - 200} more")
    raise SystemExit(1)


if __name__ == "__main__":
  main()
