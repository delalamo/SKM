"""Annotation library for per-paper build scripts (spec section 7.6).

A build script loads the pristine ingest output of one paper, applies exact
corrections and adds the margin layer in code, then renders the paper note:

  note = Note.load(BASE / "alpha2020.md")
  note.sub("alp20-p003", "teh", "the")            # exact correction, once
  note.name("five recurring shapes", "alp20-shapes")  # semantic block ID
  note.claim("alp20-shapes", "C-0001", "Most short widget loops fall into five recurring shapes.", "supports")
  note.context("alp20-p003", "Scope", "The survey covers crystal structures only.", "loops from crystal structures")
  note.eq("alp20-eq1", "Symbols", "$k$ is the number of shapes.")
  note.write(VAULT / "Papers" / "alpha2020.md")

Claims are referred to by ID; their current titles come from
``_tools/data/claim_ids.json`` when the note is rendered, so renaming or
merging a claim never touches a build script.
"""

from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from vaultlib import frontmatter, markdown, paths  # noqa: E402

RELATION_TITLES = {
  "supports": "Supports",
  "qualifies": "Qualifies",
  "contradicts": "Contradicts",
  "cited": "Cited, not tested here",
  "related": "Related",
}


class AnnotationError(ValueError):
  pass


@dataclass
class _Margin:
  kind: str  # claim | context | eq
  title: str
  body: list[str]
  span: str | None
  meta: list[str]


@dataclass
class _Chunk:
  text: str  # raw lines of one block (with its ID), no trailing newline
  id: str | None
  kind: str
  blank_before: bool = True  # was the block separated from the previous one by a blank line
  margins: list[_Margin] = field(default_factory=list)


class Note:
  def __init__(self, text: str, registry: dict | None = None) -> None:
    self.fm, body = frontmatter.parse(text)
    self.fm = self.fm or {}
    self.registry = registry if registry is not None else _load_registry()
    self.chunks: list[_Chunk] = []
    lines = body.split("\n")
    previous_end = None
    for block in markdown.segment(body):
      end = block.end
      if block.id_line is not None:
        end = block.id_line + 1
      chunk_text = "\n".join(lines[block.start : end]).strip("\n")
      blank = previous_end is None or block.start > previous_end
      self.chunks.append(_Chunk(chunk_text, block.id, block.kind, blank))
      previous_end = end

  @classmethod
  def load(cls, path: Path | str, registry: dict | None = None) -> "Note":
    return cls(Path(path).read_text(encoding="utf-8"), registry)

  # -- lookups -------------------------------------------------------------

  def _chunk(self, block_id: str) -> _Chunk:
    found = [chunk for chunk in self.chunks if chunk.id == block_id]
    if len(found) != 1:
      raise AnnotationError(f"block ^{block_id} found {len(found)} times")
    return found[0]

  def ids(self) -> list[str]:
    return [chunk.id for chunk in self.chunks if chunk.id]

  # -- corrections and names -------------------------------------------------

  def sub(self, block_id: str, old: str, new: str) -> None:
    """Exact correction inside one block; ``old`` must occur exactly once."""
    chunk = self._chunk(block_id)
    count = chunk.text.count(old)
    if count != 1:
      raise AnnotationError(f"^{block_id}: {old!r} occurs {count} times")
    chunk.text = chunk.text.replace(old, new)

  def name(self, snippet: str, new_id: str) -> None:
    """Give the block containing ``snippet`` (exactly one) the ID ``new_id``."""
    found = [chunk for chunk in self.chunks if snippet in chunk.text and chunk.kind != "heading"]
    if len(found) != 1:
      raise AnnotationError(f"snippet {snippet!r} found in {len(found)} blocks")
    if new_id in self.ids():
      raise AnnotationError(f"block ID ^{new_id} already exists")
    chunk = found[0]
    if chunk.id is None:
      raise AnnotationError(f"block with {snippet!r} has no ID to rename")
    old_id = chunk.id
    chunk.text = re.sub(rf"\^{re.escape(old_id)}(\s*)$", f"^{new_id}\\1", chunk.text)
    chunk.id = new_id
    for other in self.chunks:
      other.text = other.text.replace(f"#^{old_id}|", f"#^{new_id}|").replace(f"#^{old_id}]]", f"#^{new_id}]]")

  # -- margin notes ----------------------------------------------------------

  def _check_span(self, chunk: _Chunk, span: str) -> None:
    if "[[" in span or "]]" in span:
      raise AnnotationError(f"highlight may not include a wikilink: {span!r}")
    count = chunk.text.count(span)
    if count != 1:
      raise AnnotationError(f"^{chunk.id}: highlight {span!r} occurs {count} times")

  def claim(
    self, block_id: str, claim: str, span: str, rel: str,
    title: str | None = None, note: str | None = None, author: str = "llm",
  ) -> None:
    if rel not in RELATION_TITLES:
      raise AnnotationError(f"unknown relation {rel!r}")
    chunk = self._chunk(block_id)
    self._check_span(chunk, span)
    claim_title = self._claim_title(claim)
    body = [f"- [[{claim_title}]]"]
    if note:
      body += ["", note]
    chunk.margins.append(_Margin("claim", title or RELATION_TITLES[rel], body, span, [author, rel]))

  def context(self, block_id: str, title: str, body: str, span: str, author: str = "llm") -> None:
    chunk = self._chunk(block_id)
    self._check_span(chunk, span)
    chunk.margins.append(_Margin("context", title, body.split("\n"), span, [author]))

  def eq(self, block_id: str, title: str, body: str, author: str = "llm") -> None:
    chunk = self._chunk(block_id)
    if chunk.kind != "math":
      raise AnnotationError(f"^{block_id} is not a display equation")
    chunk.margins.append(_Margin("eq", title, body.split("\n"), None, [author]))

  def _claim_title(self, claim: str) -> str:
    if re.fullmatch(r"C-\d{4}", claim):
      entry = self.registry.get(claim)
      if entry is None:
        raise AnnotationError(f"claim {claim} is not in claim_ids.json")
      if entry.get("merged_into"):
        return self._claim_title(entry["merged_into"])
      return entry["title"]
    return claim

  # -- rendering -------------------------------------------------------------

  def render(self) -> str:
    out: list[str] = []
    for chunk in self.chunks:
      text = chunk.text
      ordered = [m for m in chunk.margins if m.kind == "eq"]
      spanned = sorted((m for m in chunk.margins if m.span), key=lambda m: text.index(m.span))
      for margin in spanned:
        cls = "pm-claim" if margin.kind == "claim" else "pm-context"
        text = text.replace(margin.span, f'<mark class="{cls}">{margin.span}</mark>', 1)
      separator = "\n\n" if (chunk.blank_before or chunk.margins) else "\n"
      for margin in ordered + spanned:
        meta = "|" + " ".join(["margin", *margin.meta])
        lines = [f"> [!{margin.kind}{meta}] {margin.title}"]
        lines += [f"> {line}".rstrip() if line else ">" for line in margin.body]
        out.append("\n\n" + "\n".join(lines))
      out.append(separator + text)
    body = "".join(out).lstrip("\n") + "\n"
    return frontmatter.compose(self.fm, "\n" + body, frontmatter.PAPER_ORDER)

  def write(self, path: Path | str) -> bool:
    path = Path(path)
    text = self.render()
    if path.exists() and path.read_text(encoding="utf-8") == text:
      return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return True


def _load_registry(data_dir: Path | None = None) -> dict:
  path = (data_dir or paths.DEFAULT_DATA) / "claim_ids.json"
  if not path.exists():
    return {}
  return json.loads(path.read_text(encoding="utf-8"))
