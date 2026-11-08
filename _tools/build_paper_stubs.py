#!/usr/bin/env python3
"""Create and refresh stub paper notes from the bibliography.

A stub is the bibliographic record of a paper whose text is not yet in the
vault (``fulltext: stub``): frontmatter plus a status banner. Each new paper
note gets a permanent short block-ID prefix (``gul23``) that keeps block IDs
unique across the vault.

  python3 _tools/build_paper_stubs.py --keys guloglu2023 nowak2016   # create
  python3 _tools/build_paper_stubs.py --all                          # create every missing stub
  python3 _tools/build_paper_stubs.py                                # refresh existing stubs only
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from vaultlib import bib as biblib  # noqa: E402
from vaultlib import edit, frontmatter, paths  # noqa: E402
from vaultlib.vault import Vault  # noqa: E402

STATUS_CHECKS = {"retraction_watch": "not run", "crossref_updates": "not run", "pubpeer": "not run"}


def _prefix_base(entry: biblib.Entry) -> str:
  authors = entry.authors
  family = biblib.fold(authors[0].family) if authors else biblib.fold(entry.key)
  letters = re.sub(r"[^a-z]", "", family)[:3]
  letters = (letters + "xx")[: max(2, len(letters))]
  year = re.sub(r"\D", "", entry.year)[-2:] or "00"
  return f"{letters}{year}"


def allocate_prefix(entry: biblib.Entry, taken: set[str]) -> str:
  base = _prefix_base(entry)
  for suffix in [""] + [chr(code) for code in range(ord("b"), ord("z") + 1)]:
    candidate = base + suffix
    if candidate not in taken:
      taken.add(candidate)
      return candidate
  raise RuntimeError(f"no free block prefix for {entry.key}")


def bib_fields(entry: biblib.Entry) -> dict:
  year = int(entry.year) if entry.year.isdigit() else entry.year
  return {
    "citekey": entry.key,
    "title": entry.title,
    "aliases": entry.aliases(),
    "authors": [author.display() for author in entry.authors],
    "year": year,
    "venue": entry.venue,
    "doi": entry.doi,
  }


def stub_body(entry: biblib.Entry) -> str:
  target = f"https://doi.org/{entry.doi}" if entry.doi else entry.fields.get("url", "")
  where = f" [Publisher's version]({target})." if target else ""
  return (
    "\n> [!status] About this note\n"
    f"> Bibliographic record only: the text of this paper is not yet in the vault.{where}\n"
  )


def stub_frontmatter(entry: biblib.Entry, prefix: str, existing: dict | None = None) -> dict:
  existing = existing or {}
  fm = dict(existing)
  fm.update(bib_fields(entry))
  fm.setdefault("license", "unknown")
  fm["fulltext"] = "stub"
  fm["block_prefix"] = existing.get("block_prefix", prefix)
  fm.setdefault("status_checks", dict(STATUS_CHECKS))
  fm.setdefault("topics", [])
  fm.setdefault("claims", [])
  fm["cssclasses"] = ["paper-margin"]
  fm["tags"] = ["paper"]
  return fm


def run(vault_dir: Path, bib_path: Path, data_dir: Path, keys: list[str] | None = None, create_all: bool = False) -> int:
  vault = Vault(vault_dir, bib_path, data_dir)
  entries = vault.bib
  taken = {str((note.fm or {}).get("block_prefix")) for note in vault.kind("paper")}
  changed = 0
  for note in vault.kind("paper"):
    fm = note.fm or {}
    if fm.get("fulltext") != "stub" or note.name not in entries:
      continue
    entry = entries[note.name]
    new_fm = stub_frontmatter(entry, fm.get("block_prefix", ""), fm)
    changed += edit.save(note, new_fm, stub_body(entry))
  wanted = sorted(entries) if create_all else sorted(keys or [])
  for key in wanted:
    if key not in entries:
      raise SystemExit(f"{key} is not in {bib_path}")
    path = vault_dir / paths.PAPERS / f"{key}.md"
    if path.exists():
      continue
    entry = entries[key]
    fm = stub_frontmatter(entry, allocate_prefix(entry, taken))
    changed += edit.write_if_changed(path, frontmatter.compose(fm, stub_body(entry), frontmatter.PAPER_ORDER))
  return changed


def main(argv: list[str] | None = None) -> int:
  parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
  parser.add_argument("--vault", type=Path, default=paths.DEFAULT_VAULT)
  parser.add_argument("--bib", type=Path, default=paths.DEFAULT_BIB)
  parser.add_argument("--data", type=Path, default=paths.DEFAULT_DATA)
  parser.add_argument("--keys", nargs="*", help="citekeys to create stubs for")
  parser.add_argument("--all", action="store_true", help="create a stub for every bibliography entry without a note")
  args = parser.parse_args(argv)
  changed = run(args.vault, args.bib, args.data, args.keys, args.all)
  print(f"build_paper_stubs: {changed} files changed")
  return 0


if __name__ == "__main__":
  sys.exit(main())
