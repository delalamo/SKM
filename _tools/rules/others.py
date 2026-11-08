"""Rules for topics, glossary, acronyms, concepts, datasets and indexes."""

from __future__ import annotations

import re

from vaultlib import markdown

from . import rule

RETIRED_TOPIC_SECTIONS = {"papers in the vault", "open questions"}
ACCESS_CLASSES = ("public", "licensed", "restricted", "by agreement", "unavailable")


@rule("TOPIC-FM", "topics", "Topic frontmatter: type topic, aliases list, tag topic")
def topic_fm(vault):
  for note in vault.kind("topic"):
    fm = note.fm or {}
    if fm.get("type") != "topic":
      yield note.rel, 1, "type must be topic"
    if not isinstance(fm.get("aliases"), list):
      yield note.rel, 1, "aliases must be a list"
    if "topic" not in (fm.get("tags") or []):
      yield note.rel, 1, "tags must include topic"


@rule("TOPIC-MARKERS", "topics", "Topic pages keep the generated claim-list markers and a Related topics section")
def topic_markers(vault):
  for note in vault.kind("topic"):
    if markdown.generated_section(note.body, "claims") is None:
      yield note.rel, 1, "missing '%% begin generated: claims %%' … '%% end generated %%'"
    if not any(b.kind == "heading" and b.level == 2 and b.heading == "Related topics" for b in note.blocks):
      yield note.rel, 1, "missing '## Related topics'"


@rule("TOPIC-RETIRED", "topics", "No 'Papers in the vault' or 'Open questions' sections")
def topic_retired(vault):
  for note in vault.kind("topic"):
    for block in note.blocks:
      if block.kind == "heading" and block.heading.strip().lower() in RETIRED_TOPIC_SECTIONS:
        yield note.rel, note.line_no(block.start), f"retired section '{block.heading}'"


@rule("GLOSSARY-PLAIN", "glossary", "A glossary note is one plain definition: no frontmatter, headings, lists, tables, quotes, equations, links, bold or HTML")
def glossary_plain(vault):
  for note in vault.kind("glossary"):
    if note.text.startswith("---\n"):
      yield note.rel, 1, "glossary notes have no frontmatter"
    if not note.body.strip():
      yield note.rel, 1, "definition is empty"
    for block in note.blocks:
      line = note.line_no(block.start)
      if block.kind != "paragraph":
        yield note.rel, line, f"glossary notes hold plain prose only (found {block.kind})"
        continue
      text = block.text
      if markdown.WIKILINK_RE.search(text) or re.search(r"\]\(", text):
        yield note.rel, line, "glossary notes contain no links"
      if "**" in text or "__" in text:
        yield note.rel, line, "glossary notes contain no bold text"
      if re.search(r"<[a-zA-Z/][^>]*>", text):
        yield note.rel, line, "glossary notes contain no HTML"
      if re.search(r"(?<!\\)\$", text):
        yield note.rel, line, "glossary notes contain no maths"


@rule("ACRONYMS-TABLE", "glossary", "Acronyms.md holds only its | Acronym | Definition | table")
def acronyms_table(vault):
  for note in vault.kind("acronyms"):
    blocks = note.blocks
    if note.text.startswith("---\n") or len(blocks) != 1 or blocks[0].kind != "table":
      yield note.rel, 1, "Acronyms.md must hold only the acronym table"
      continue
    rows = blocks[0].lines
    if not re.fullmatch(r"\|\s*Acronym\s*\|\s*Definition\s*\|", rows[0].strip()):
      yield note.rel, 1, "the table header must be | Acronym | Definition |"
    for offset, row in enumerate(rows[2:], start=2):
      cells = [cell.strip() for cell in row.strip().strip("|").split("|")]
      if len(cells) != 2 or not all(cells):
        yield note.rel, note.line_no(blocks[0].start + offset), "each row needs an acronym and a definition"


@rule("CONCEPT-FM", "concepts", "Concept frontmatter: type concept, aliases, introduced_by papers, topics, tag concept")
def concept_fm(vault):
  for note in vault.kind("concept"):
    fm = note.fm or {}
    if fm.get("type") != "concept":
      yield note.rel, 1, "type must be concept"
    for key in ("aliases", "introduced_by", "topics"):
      if not isinstance(fm.get(key), list):
        yield note.rel, 1, f"{key} must be a list"
    if "concept" not in (fm.get("tags") or []):
      yield note.rel, 1, "tags must include concept"
    for target in note.fm_link_targets("introduced_by"):
      found = vault.resolve(target, note)
      if found is not None and found.kind != "paper":
        yield note.rel, 1, f"introduced_by entry {target} is not a paper note"


@rule("DATASET-FM", "datasets", "Dataset frontmatter: type, provider, access class and URL")
def dataset_fm(vault):
  for note in vault.kind("dataset"):
    fm = note.fm or {}
    if fm.get("type") != "dataset":
      yield note.rel, 1, "type must be dataset"
    for key in ("provider", "url"):
      if not str(fm.get(key) or "").strip():
        yield note.rel, 1, f"missing {key}"
    if fm.get("access_class") not in ACCESS_CLASSES:
      yield note.rel, 1, f"access_class must be one of {', '.join(ACCESS_CLASSES)}"


@rule("INDEX-GENERATED", "indexes", "Index notes are generated only")
def index_generated(vault):
  for note in vault.kind("index"):
    lines = [line for line in note.body.split("\n") if line.strip()]
    if not lines or not markdown.GENERATED_BEGIN_RE.match(lines[0]) or not markdown.GENERATED_END_RE.match(lines[-1]):
      yield note.rel, 1, "index notes must consist of one generated section"
