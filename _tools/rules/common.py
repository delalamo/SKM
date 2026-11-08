"""Rules that apply to every note of the knowledge base (spec Appendix B)."""

from __future__ import annotations

import json
import re
import shutil
import subprocess
from pathlib import Path

from vaultlib import markdown, paths

from . import rule

ALLOWED_CALLOUTS = {"claim", "context", "eq", "cite", "status"}
ALLOWED_METADATA = {
  "margin", "llm", "human", "verified", "unverified",
  "supports", "qualifies", "contradicts", "cited", "related",
}
ATTACHMENT_EXT = re.compile(r"\.(png|jpe?g|gif|svg|webp|pdf)$", re.IGNORECASE)
DOLLAR_DIGIT_RE = re.compile(r"(?<![\\$])\$(?=\d)")
INLINE_CODE_RE = re.compile(r"`[^`]*`")
INLINE_MATH_RE = re.compile(r"(?<![\\$])\$(?!\$)((?:\\\$|[^$\n])+?)(?<!\\)\$(?!\d)")
PANDOC_RE = re.compile(r"\[[^\[\]\n]*?(?<![\w.])@[A-Za-z][A-Za-z0-9_:-]*[^\[\]\n]*\]")


def _kb(vault):
  return vault.kb_notes()


def _is_attachment(link) -> bool:
  return bool(ATTACHMENT_EXT.search(link.target))


@rule("FM-PARSE", "all", "Frontmatter is valid YAML")
def fm_parse(vault):
  for note in _kb(vault):
    if note.fm_error:
      yield note.rel, 1, f"frontmatter does not parse: {note.fm_error.splitlines()[0]}"


@rule("LINK-RESOLVE", "all", "Every link, embed and block reference resolves")
def link_resolve(vault):
  for note in _kb(vault):
    for link in note.links + note.fm_links:
      line = link.line + 1
      if _is_attachment(link):
        if vault.resolve_file(link.target) is None:
          yield note.rel, line, f"attachment not found: {link.target}"
        continue
      target = vault.resolve(link.target, note)
      if target is None:
        yield note.rel, line, f"unresolved link: {link.raw}"
        continue
      if link.block and link.block not in vault.block_ids.get(target.rel, {}):
        yield note.rel, line, f"no block ^{link.block} in {target.name}"
      elif link.heading:
        wanted = link.heading.lower()
        if wanted not in {heading.lower() for heading in vault.headings(target)}:
          yield note.rel, line, f"no heading '{link.heading}' in {target.name}"


@rule("LINK-LEGACY", "all", "Knowledge-base notes never link into the legacy zone")
def link_legacy(vault):
  for note in _kb(vault):
    for link in note.links + note.fm_links:
      if _is_attachment(link):
        found = vault.resolve_file(link.target)
        if found and found.split("/")[0] not in paths.KB_FOLDERS:
          yield note.rel, link.line + 1, f"attachment outside the knowledge base: {found}"
        continue
      target = vault.resolve(link.target, note)
      if target is not None and target.kind in ("legacy", "root"):
        yield note.rel, link.line + 1, f"link into legacy note {target.rel}"


@rule("NAME-DUP", "all", "No two notes share a name")
def name_dup(vault):
  for name, notes in sorted(vault.by_name.items()):
    if len(notes) > 1 and any(note.is_kb for note in notes):
      rels = ", ".join(sorted(note.rel for note in notes))
      for note in notes:
        if note.is_kb:
          yield note.rel, 1, f"note name '{note.name}' is not unique: {rels}"


@rule("BLOCKID-DUP", "all", "No duplicate block IDs within a note or across papers")
def blockid_dup(vault):
  owners: dict[str, str] = {}
  for note in _kb(vault):
    seen: set[str] = set()
    for block in note.blocks:
      if not block.id:
        continue
      if block.id in seen:
        yield note.rel, note.line_no(block.start), f"duplicate block ID ^{block.id}"
      seen.add(block.id)
      if note.kind == "paper":
        other = owners.setdefault(block.id, note.rel)
        if other != note.rel:
          yield note.rel, note.line_no(block.start), f"block ID ^{block.id} also used in {other}"


@rule("BLOCKLINK-LABEL", "all", "Block links carry readable labels")
def blocklink_label(vault):
  for note in _kb(vault):
    for link in note.links:
      if link.block and not link.embed and not (link.alias or "").strip():
        yield note.rel, link.line + 1, f"block link without a label: {link.raw}"


@rule("ATTACH-PLACE", "all", "Embedded attachments live in an attachments folder, paper figures named <citekey>-<name>")
def attach_place(vault):
  for note in _kb(vault):
    for link in note.links:
      if not (link.embed and _is_attachment(link)):
        continue
      found = vault.resolve_file(link.target)
      if found is None:
        continue
      parts = found.split("/")
      if len(parts) != 3 or parts[1] != paths.ATTACHMENTS or parts[0] not in paths.KB_FOLDERS:
        yield note.rel, link.line + 1, f"attachment {found} is not in <folder>/attachments/"
      elif note.kind == "paper" and not parts[2].startswith(note.name + "-"):
        yield note.rel, link.line + 1, f"paper figure {parts[2]} must be named {note.name}-<name>"


@rule("CALLOUT-TYPE", "all", "Callout types and metadata words come from the allowed lists")
def callout_type(vault):
  for note in _kb(vault):
    for block in note.blocks:
      if block.kind != "callout":
        continue
      callout = block.callout
      line = note.line_no(block.start)
      if callout.kind not in ALLOWED_CALLOUTS:
        yield note.rel, line, f"callout type '{callout.kind}' is not allowed"
      for word in callout.metadata:
        if word not in ALLOWED_METADATA:
          yield note.rel, line, f"callout metadata word '{word}' is not allowed"


@rule("CALLOUT-BLANK", "all", "Callouts are separated from each other and from text by blank lines")
def callout_blank(vault):
  for note in _kb(vault):
    lines = note.body.split("\n")
    for block in note.blocks:
      if block.kind not in ("callout", "quote"):
        continue
      if any(markdown.CALLOUT_RE.match(line) for line in block.lines[1:]):
        yield note.rel, note.line_no(block.start), "two callouts with no blank line between them"
      if block.kind != "callout":
        continue
      if block.start > 0 and lines[block.start - 1].strip():
        yield note.rel, note.line_no(block.start), "callout not preceded by a blank line"
      if block.end < len(lines) and lines[block.end].strip():
        yield note.rel, note.line_no(block.end), "callout not followed by a blank line"


def _prose_lines(note):
  """(body line index, text) for lines outside math and code blocks."""
  skip: set[int] = set()
  for block in note.blocks:
    if block.kind in ("math", "code"):
      skip.update(range(block.start, block.end))
  for index, line in enumerate(note.body.split("\n")):
    if index not in skip:
      yield index, INLINE_CODE_RE.sub("", line)


@rule("DOLLAR-DIGIT", "all", "No unescaped $ before a digit (write \\$ for currency)")
def dollar_digit(vault):
  for note in _kb(vault):
    for index, line in _prose_lines(note):
      if DOLLAR_DIGIT_RE.search(line):
        yield note.rel, note.line_no(index), "unescaped $ before a digit"


@rule("TAG-BALANCE", "all", "<mark> and <abbr> tags are balanced; highlight classes are pm-claim or pm-context")
def tag_balance(vault):
  for note in _kb(vault):
    for block in note.blocks:
      text = block.text
      line = note.line_no(block.start)
      if len(re.findall(r"<mark\b", text)) != text.count("</mark>"):
        yield note.rel, line, "unbalanced <mark> tags"
      if len(re.findall(r"<abbr\b", text)) != text.count("</abbr>"):
        yield note.rel, line, "unbalanced <abbr> tags"
      for cls in markdown.mark_classes(text):
        if cls not in ("pm-claim", "pm-context"):
          yield note.rel, line, f"highlight class '{cls}' is not pm-claim or pm-context"


@rule("NO-PANDOC", "all", "Knowledge-base notes cite through links, never Pandoc [@key] citations")
def no_pandoc(vault):
  for note in _kb(vault):
    for index, line in _prose_lines(note):
      cleaned = markdown.WIKILINK_RE.sub("", line)
      if PANDOC_RE.search(cleaned):
        yield note.rel, note.line_no(index), "Pandoc citation; link the paper note instead"


def _equations(note):
  for block in note.blocks:
    if block.kind == "math":
      tex = block.text.strip()
      tex = tex[2:-2] if tex.endswith("$$") else tex[2:]
      yield block.start, tex, True
    elif block.kind in ("paragraph", "listitem", "table", "callout"):
      for offset, line in enumerate(block.lines):
        line = INLINE_CODE_RE.sub("", line)
        if block.kind == "callout":
          line = line.lstrip(">").lstrip()
        for match in INLINE_MATH_RE.finditer(line):
          yield block.start + offset, match.group(1), False


@rule("KATEX", "all", "Every equation parses in KaTeX", needs_katex=True)
def katex_parse(vault, katex_dir):
  node = shutil.which("node")
  script = Path(__file__).resolve().parents[1] / "node" / "katex_check.mjs"
  items, where = [], []
  for note in _kb(vault):
    for line, tex, display in _equations(note):
      items.append({"id": len(items), "tex": tex, "display": display})
      where.append((note.rel, note.line_no(line)))
  if not items:
    return
  if node is None:
    yield "-", 0, "node is not installed; cannot check equations"
    return
  result = subprocess.run(
    [node, str(script), katex_dir], input=json.dumps(items), capture_output=True, text=True, check=False
  )
  if result.returncode != 0:
    yield "-", 0, f"KaTeX check failed to run: {result.stderr.strip()[:200]}"
    return
  for failure in json.loads(result.stdout or "[]"):
    rel, line = where[failure["id"]]
    yield rel, line, f"equation does not parse in KaTeX: {failure['error']}"
