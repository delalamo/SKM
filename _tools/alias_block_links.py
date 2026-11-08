#!/usr/bin/env python3
"""Give every block link a readable label.

Links into a paper read ``Surname (Year), §section`` (the nearest heading
above the block, its number when the heading is numbered); links to other
notes read as the note name; unlabelled same-note links read ``§section``.
Existing labels on same-note links (such as citation numbers) are kept.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from vaultlib import edit, markdown, paths  # noqa: E402
from vaultlib.vault import Vault  # noqa: E402

NUMBERED_RE = re.compile(r"^((?:[A-Z]|\d+)(?:\.\d+)*)\.?\s")


def section_of(note, block_id: str) -> str:
  heading = ""
  for block in note.blocks:
    if block.kind == "heading":
      heading = block.heading
    if block.id == block_id:
      break
  heading = markdown.strip_markup(heading).strip()
  match = NUMBERED_RE.match(heading)
  return match.group(1) if match else heading


def label_for(vault: Vault, source, link) -> str | None:
  target = vault.resolve(link.target, source) if link.target else source
  if target is None:
    return None
  section = section_of(target, link.block)
  if link.target == "":
    if (link.alias or "").strip():
      return None
    return f"§{section}" if section else "this note"
  if target.kind == "paper":
    entry = vault.bib.get(target.name)
    who = entry.short_label() if entry else target.name
    return f"{who}, §{section}" if section else who
  return target.name


def process(vault: Vault, note) -> bool:
  lines = note.body.split("\n")
  changed = False
  for index, line in enumerate(lines):
    if "#^" not in line:
      continue
    in_table = line.lstrip("> ").startswith("|")

    def relabel(match: re.Match) -> str:
      if match.group(1):  # embeds need no label
        return match.group(0)
      target, subpath, alias = markdown.parse_link_inner(match.group(2))
      link = markdown.Link(False, target, subpath, alias, match.group(0), 0, 0, 0)
      if not link.block:
        return match.group(0)
      label = label_for(vault, note, link)
      if label is None:
        return match.group(0)
      return markdown.make_link(target, label, subpath, table=in_table)

    new = markdown.WIKILINK_RE.sub(relabel, line)
    if new != line:
      lines[index] = new
      changed = True
  if not changed:
    return False
  return edit.save(note, note.fm, "\n".join(lines))


def run(vault_dir: Path, bib_path: Path, data_dir: Path) -> int:
  vault = Vault(vault_dir, bib_path, data_dir)
  return sum(process(vault, note) for note in vault.kb_notes())


def main(argv: list[str] | None = None) -> int:
  parser = argparse.ArgumentParser(description=__doc__)
  parser.add_argument("--vault", type=Path, default=paths.DEFAULT_VAULT)
  parser.add_argument("--bib", type=Path, default=paths.DEFAULT_BIB)
  parser.add_argument("--data", type=Path, default=paths.DEFAULT_DATA)
  args = parser.parse_args(argv)
  print(f"alias_block_links: {run(args.vault, args.bib, args.data)} files changed")
  return 0


if __name__ == "__main__":
  sys.exit(main())
