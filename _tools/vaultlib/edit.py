"""Small helpers shared by the generators: write only when content changes."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from . import frontmatter

ORDER_BY_KIND = {
  "paper": frontmatter.PAPER_ORDER,
  "claim": frontmatter.CLAIM_ORDER,
  "topic": frontmatter.TOPIC_ORDER,
  "concept": frontmatter.CONCEPT_ORDER,
  "dataset": frontmatter.DATASET_ORDER,
}


def write_if_changed(path: Path, text: str) -> bool:
  path = Path(path)
  if path.exists() and path.read_text(encoding="utf-8") == text:
    return False
  path.parent.mkdir(parents=True, exist_ok=True)
  path.write_text(text, encoding="utf-8")
  return True


def save(note, fm: dict[str, Any] | None, body: str) -> bool:
  """Write a note back with its frontmatter in the canonical key order."""
  text = frontmatter.compose(fm, body, ORDER_BY_KIND.get(note.kind, ()))
  changed = write_if_changed(note.path, text)
  if changed:
    note.text = text
    note.fm = fm
    note.body = body
    note.body_line0 = frontmatter.body_offset(text)
    for attr in ("blocks", "links", "fm_links"):
      note.__dict__.pop(attr, None)
  return changed


def link(target: str, alias: str | None = None) -> str:
  return f"[[{target}|{alias}]]" if alias else f"[[{target}]]"
