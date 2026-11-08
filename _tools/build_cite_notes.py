#!/usr/bin/env python3
"""Write the grey reference callouts beside every passage that cites references.

Each callout lists the full reference (as printed in the paper's reference
list) for every citation in its passage, links the cited paper's vault note
where there is one, and is titled ``References (N)``. Never edit them by hand
(spec section 7.4).
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from vaultlib import edit, markdown, paths  # noqa: E402
from vaultlib.vault import Vault  # noqa: E402

ARROW_LINK_RE = re.compile(r"→\s*\[\[([^\]|#]+)(?:\|[^\]]*)?\]\]")


def reference_texts(vault: Vault, note) -> dict[str, tuple[str, str]]:
  """Reference block ID -> (number, full text with a labelled vault link)."""
  prefix = (note.fm or {}).get("block_prefix", "")
  out = {}
  for block in note.blocks:
    if block.kind != "listitem" or not block.id or not block.id.startswith(f"{prefix}-ref-"):
      continue
    number = block.id.rsplit("-", 1)[-1]
    text = " ".join(line.strip() for line in block.lines)
    text = re.sub(r"^\d+[.)]\s+", "", text)
    text = markdown.BLOCK_ID_RE.sub("", text).strip()

    def label(match: re.Match) -> str:
      target = vault.resolve(match.group(1), note)
      entry = vault.bib.get(match.group(1))
      if target is None or entry is None:
        return match.group(0)
      return f"→ [[{match.group(1)}|{entry.short_label()}]]"

    out[block.id] = (number, ARROW_LINK_RE.sub(label, text))
  return out


def cited(prefix: str, text: str) -> list[str]:
  out: list[str] = []
  for link in markdown.find_links(text):
    if link.target == "" and link.block and link.block.startswith(f"{prefix}-ref-") and link.block not in out:
      out.append(link.block)
  return out


def callout_lines(refs: list[str], texts: dict[str, tuple[str, str]]) -> list[str]:
  lines = [f"> [!cite|margin llm]- References ({len(refs)})"]
  for ref in refs:
    number, text = texts.get(ref, (ref.rsplit("-", 1)[-1], "(reference not found)"))
    lines.append(f"> - [[#^{ref}|{number}]] {text}")
  return lines


def process(vault: Vault, note) -> bool:
  fm = note.fm or {}
  if fm.get("fulltext") == "stub":
    return False
  prefix = fm.get("block_prefix", "")
  texts = reference_texts(vault, note)
  lines = note.body.split("\n")
  edits: list[tuple[int, int, list[str]]] = []  # (start, end, replacement)
  for block in markdown.attach_callouts(note.blocks):
    if block.kind in ("callout", "marker", "blockid", "heading") or (block.id or "").startswith(f"{prefix}-ref-"):
      continue
    refs = cited(prefix, block.text)
    for existing in [c for c in block.callouts if c.callout.kind == "cite"]:
      end = existing.end + 1 if existing.end < len(lines) and not lines[existing.end].strip() else existing.end
      edits.append((existing.start, end, []))
    if refs:
      edits.append((block.start, block.start, callout_lines(refs, texts) + [""]))
  for start, end, replacement in sorted(edits, key=lambda e: (e[0], e[1]), reverse=True):
    lines[start:end] = replacement
  return edit.save(note, note.fm, "\n".join(lines))


def run(vault_dir: Path, bib_path: Path, data_dir: Path) -> int:
  vault = Vault(vault_dir, bib_path, data_dir)
  return sum(process(vault, note) for note in vault.kind("paper"))


def main(argv: list[str] | None = None) -> int:
  parser = argparse.ArgumentParser(description=__doc__)
  parser.add_argument("--vault", type=Path, default=paths.DEFAULT_VAULT)
  parser.add_argument("--bib", type=Path, default=paths.DEFAULT_BIB)
  parser.add_argument("--data", type=Path, default=paths.DEFAULT_DATA)
  args = parser.parse_args(argv)
  print(f"build_cite_notes: {run(args.vault, args.bib, args.data)} files changed")
  return 0


if __name__ == "__main__":
  sys.exit(main())
