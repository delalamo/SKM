#!/usr/bin/env python3
"""Add hover definitions for acronyms from Glossary/Acronyms.md.

The first use of each acronym in each block of Papers, Claims and Topics is
wrapped in ``<abbr title="definition">``. Generated sections, headings,
reference lines, footnote definitions and status or reference callouts are
skipped. Existing wrappers are removed first, so editing the acronym table
and re-running updates every note (spec section 7.5).
"""

from __future__ import annotations

import argparse
import html
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from vaultlib import edit, markdown, paths  # noqa: E402
from vaultlib.vault import Vault  # noqa: E402

ABBR_TAG_RE = re.compile(r'<abbr title="[^"]*">(.*?)</abbr>', re.DOTALL)
PROTECTED_RE = re.compile(
  r"!?\[\[[^\]]*\]\]"  # wikilinks and embeds
  r"|(?<!\\)\$\$.*?\$\$|(?<!\\)\$(?:\\\$|[^$\n])+?(?<!\\)\$"  # maths
  r"|`[^`]*`"  # inline code
  r"|<[^>]+>"  # HTML tags (not their text)
  r"|https?://\S+"  # URLs
  r"|\s\^[A-Za-z0-9][A-Za-z0-9_-]*\s*$"  # block IDs
)
SKIP_CALLOUTS = {"status", "cite"}


def wrap_line(line: str, acronyms: dict[str, str], seen: set[str], pattern: re.Pattern) -> str:
  out, cursor = [], 0
  for protected in PROTECTED_RE.finditer(line):
    out.append(_wrap_text(line[cursor:protected.start()], acronyms, seen, pattern))
    out.append(protected.group(0))
    cursor = protected.end()
  out.append(_wrap_text(line[cursor:], acronyms, seen, pattern))
  return "".join(out)


def _wrap_text(text: str, acronyms: dict[str, str], seen: set[str], pattern: re.Pattern) -> str:
  def repl(match: re.Match) -> str:
    word = match.group(0)
    if word in seen:
      return word
    seen.add(word)
    return f'<abbr title="{html.escape(acronyms[word], quote=True)}">{word}</abbr>'

  return pattern.sub(repl, text)


def process(vault: Vault, note, acronyms: dict[str, str], pattern: re.Pattern) -> bool:
  if note.kind == "paper" and (note.fm or {}).get("fulltext") == "stub":
    return False
  prefix = (note.fm or {}).get("block_prefix", "")
  lines = note.body.split("\n")
  for block in note.blocks:
    if block.generated or block.kind in ("heading", "math", "code", "marker", "blockid", "figure", "comment"):
      continue
    if block.kind == "callout" and block.callout.kind in SKIP_CALLOUTS:
      continue
    if (block.id or "").startswith(f"{prefix}-ref-") or block.lines[0].lstrip().startswith("[^"):
      continue
    seen: set[str] = set()
    first = block.start + (1 if block.kind == "callout" else 0)
    for index in range(first, block.end):
      line = ABBR_TAG_RE.sub(r"\1", lines[index])
      lines[index] = wrap_line(line, acronyms, seen, pattern) if acronyms else line
  return edit.save(note, note.fm, "\n".join(lines))


def run(vault_dir: Path, bib_path: Path, data_dir: Path) -> int:
  vault = Vault(vault_dir, bib_path, data_dir)
  acronyms = vault.acronyms
  words = sorted(acronyms, key=len, reverse=True)
  pattern = re.compile(r"(?<![\w-])(" + "|".join(re.escape(w) for w in words) + r")(?![\w-])") if words else re.compile(r"(?!x)x")
  changed = 0
  for note in vault.kb_notes():
    if note.kind in ("paper", "claim", "topic"):
      changed += process(vault, note, acronyms, pattern)
  return changed


def main(argv: list[str] | None = None) -> int:
  parser = argparse.ArgumentParser(description=__doc__)
  parser.add_argument("--vault", type=Path, default=paths.DEFAULT_VAULT)
  parser.add_argument("--bib", type=Path, default=paths.DEFAULT_BIB)
  parser.add_argument("--data", type=Path, default=paths.DEFAULT_DATA)
  args = parser.parse_args(argv)
  print(f"apply_abbr: {run(args.vault, args.bib, args.data)} files changed")
  return 0


if __name__ == "__main__":
  sys.exit(main())
