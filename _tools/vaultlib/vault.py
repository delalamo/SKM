"""Load a vault into memory: notes, blocks, links and how they resolve."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from functools import cached_property
from pathlib import Path
from typing import Any

from . import bib as biblib
from . import frontmatter, markdown, paths

NOTE_KIND_BY_FOLDER = {
  paths.PAPERS: "paper",
  paths.CLAIMS: "claim",
  paths.TOPICS: "topic",
  paths.CONCEPTS: "concept",
  paths.GLOSSARY: "glossary",
  paths.DATASETS: "dataset",
  paths.INDEXES: "index",
  paths.TEMPLATES: "template",
}


@dataclass
class Note:
  path: Path
  rel: str  # posix path relative to the vault root, with .md
  text: str
  fm: dict[str, Any] | None = None
  fm_error: str | None = None
  body: str = ""
  body_line0: int = 0  # 0-based file line where the body starts

  @property
  def name(self) -> str:
    return Path(self.rel).stem

  @property
  def folder(self) -> str:
    parts = self.rel.split("/")
    return parts[0] if len(parts) > 1 else ""

  @property
  def kind(self) -> str:
    if self.folder in paths.LEGACY_FOLDERS:
      return "legacy"
    if self.folder == paths.GLOSSARY and self.name == "Acronyms":
      return "acronyms"
    if self.folder == paths.PAPERS and self.rel.count("/") > 1:
      return "other"
    return NOTE_KIND_BY_FOLDER.get(self.folder, "root" if not self.folder else "other")

  @property
  def is_kb(self) -> bool:
    return self.kind not in ("legacy", "root", "other", "template")

  @cached_property
  def blocks(self) -> list[markdown.Block]:
    return markdown.segment(self.body)

  @cached_property
  def links(self) -> list[markdown.Link]:
    return markdown.find_links(self.body, self.body_line0)

  @cached_property
  def fm_links(self) -> list[markdown.Link]:
    if self.body_line0 == 0:
      return []
    head = "\n".join(self.text.split("\n")[: self.body_line0])
    return markdown.find_links(head, 0)

  def line_no(self, body_line: int) -> int:
    """1-based file line number for a 0-based body line."""
    return self.body_line0 + body_line + 1

  def fm_list(self, key: str) -> list:
    value = (self.fm or {}).get(key)
    if value is None:
      return []
    return value if isinstance(value, list) else [value]

  def fm_link_targets(self, key: str) -> list[str]:
    """Targets of wikilinks stored as strings in a frontmatter list."""
    out = []
    for item in self.fm_list(key):
      if isinstance(item, str):
        found = markdown.find_links(item)
        out.append(found[0].target if found else item)
    return out


def link_target(value: Any) -> str:
  if isinstance(value, str):
    found = markdown.find_links(value)
    return found[0].target if found else value
  return str(value)


class Vault:
  def __init__(self, root: Path, bib_path: Path | None = None, data_dir: Path | None = None) -> None:
    self.root = Path(root)
    self.bib_path = Path(bib_path) if bib_path else paths.DEFAULT_BIB
    self.data_dir = Path(data_dir) if data_dir else paths.DEFAULT_DATA
    self.notes: dict[str, Note] = {}
    self.files: dict[str, list[str]] = {}  # lowercased file name -> rel paths
    for path in sorted(self.root.rglob("*")):
      rel = path.relative_to(self.root).as_posix()
      if any(part.startswith(".") for part in rel.split("/")) or not path.is_file():
        continue
      if path.suffix == ".md":
        self.notes[rel] = self._load(path, rel)
      else:
        self.files.setdefault(path.name.lower(), []).append(rel)
    self.by_name: dict[str, list[Note]] = {}
    for note in self.notes.values():
      self.by_name.setdefault(note.name.lower(), []).append(note)

  @staticmethod
  def _load(path: Path, rel: str) -> Note:
    text = path.read_text(encoding="utf-8")
    note = Note(path=path, rel=rel, text=text)
    try:
      note.fm, note.body = frontmatter.parse(text)
    except Exception as exc:  # malformed YAML is reported by a rule
      note.fm_error = str(exc)
      _, note.body = frontmatter.split(text)
    note.body_line0 = frontmatter.body_offset(text)
    return note

  # -- lookups -------------------------------------------------------------

  def kind(self, kind: str) -> list[Note]:
    return [note for note in self.notes.values() if note.kind == kind]

  def kb_notes(self) -> list[Note]:
    return [note for note in self.notes.values() if note.is_kb]

  def resolve(self, target: str, source: Note | None = None) -> Note | None:
    if target == "":
      return source
    key = target.lower()
    if key.endswith(".md"):
      key = key[:-3]
    if "/" in key:
      for rel, note in self.notes.items():
        stem = rel[:-3].lower()
        if stem == key or stem.endswith("/" + key):
          return note
      return None
    found = self.by_name.get(key, [])
    return found[0] if len(found) == 1 else (found[0] if found else None)

  def resolve_file(self, target: str) -> str | None:
    name = target.rsplit("/", 1)[-1].lower()
    found = self.files.get(name)
    return found[0] if found else None

  def note(self, folder: str, name: str) -> Note | None:
    return self.notes.get(f"{folder}/{name}.md")

  @cached_property
  def bib(self) -> dict[str, biblib.Entry]:
    if self.bib_path.exists():
      return biblib.load(self.bib_path)
    return {}

  @cached_property
  def block_ids(self) -> dict[str, dict[str, markdown.Block]]:
    out: dict[str, dict[str, markdown.Block]] = {}
    for note in self.notes.values():
      ids: dict[str, markdown.Block] = {}
      for block in note.blocks:
        if block.id and block.id not in ids:
          ids[block.id] = block
      out[note.rel] = ids
    return out

  def headings(self, note: Note) -> set[str]:
    return {block.heading for block in note.blocks if block.kind == "heading"}

  # -- data files ------------------------------------------------------------

  def data_lines(self, name: str) -> list[str]:
    path = self.data_dir / name
    if not path.exists():
      return []
    lines = []
    for line in path.read_text(encoding="utf-8").splitlines():
      line = line.split("#", 1)[0].strip()
      if line:
        lines.append(line)
    return lines

  @cached_property
  def claim_registry(self) -> dict[str, dict]:
    path = self.data_dir / "claim_ids.json"
    if not path.exists():
      return {}
    return json.loads(path.read_text(encoding="utf-8"))

  @cached_property
  def acronyms(self) -> dict[str, str]:
    note = self.note(paths.GLOSSARY, "Acronyms")
    out: dict[str, str] = {}
    if note is None:
      return out
    for line in note.body.splitlines():
      cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
      if len(cells) == 2 and cells[0] and not re.fullmatch(r":?-+:?", cells[0]) and cells[0] != "Acronym":
        out[cells[0]] = cells[1]
    return out

  @cached_property
  def author_surnames(self) -> set[str]:
    names = biblib.surnames(self.bib)
    for note in self.kind("paper"):
      for author in note.fm_list("authors"):
        if isinstance(author, str):
          for author_obj in biblib.parse_authors(author):
            names.add(author_obj.family)
    return names

  def topic_names(self, topic: Note) -> list[str]:
    names = [topic.name]
    names += [alias for alias in topic.fm_list("aliases") if isinstance(alias, str)]
    return names

  def paper_state(self, paper: Note) -> str:
    """Derived annotation state: stub, ingested or annotated."""
    fm = paper.fm or {}
    if fm.get("fulltext") == "stub":
      return "stub"
    provenance = fm.get("annotation_provenance") or {}
    if isinstance(provenance, dict) and provenance.get("generated"):
      return "annotated"
    return "ingested"
