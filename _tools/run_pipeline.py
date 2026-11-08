#!/usr/bin/env python3
"""Run every generator in order (spec section 11.2), then the validator.

  python3 _tools/run_pipeline.py                 # the real vault
  python3 _tools/run_pipeline.py --no-validate   # generators only

Order: refresh stubs -> per-paper builds -> reference callouts -> block-link
labels -> claim evidence -> indexes and topic lists -> hover definitions ->
validator. Every step is idempotent, so a second run changes nothing.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))

import alias_block_links  # noqa: E402
import apply_abbr  # noqa: E402
import build_cite_notes  # noqa: E402
import build_claim_evidence  # noqa: E402
import build_indexes  # noqa: E402
import build_paper_stubs  # noqa: E402
import validate_vault  # noqa: E402
from annolib import Note, _load_registry  # noqa: E402
from vaultlib import paths  # noqa: E402


class BuildContext:
  """What a per-paper build script needs: where the base text is and where to write."""

  def __init__(self, vault: Path, builds: Path, data: Path) -> None:
    self.vault = vault
    self.builds = builds
    self.registry = _load_registry(data)

  def load(self, citekey: str) -> Note:
    return Note.load(self.builds / "base" / f"{citekey}.md", self.registry)

  def write(self, note: Note, citekey: str) -> bool:
    return note.write(self.vault / paths.PAPERS / f"{citekey}.md")


def run_builds(vault: Path, builds: Path, data: Path) -> int:
  changed = 0
  if not builds.exists():
    return 0
  context = BuildContext(vault, builds, data)
  for script in sorted(builds.glob("build_*.py")):
    spec = importlib.util.spec_from_file_location(f"_build_{script.stem}", script)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    changed += bool(module.build(context))
  return changed


def snapshot(*roots: Path) -> dict[str, str]:
  """Content hash of every file under the given roots (to report net changes)."""
  out = {}
  for root in roots:
    if not root.exists():
      continue
    for path in sorted(root.rglob("*")):
      if path.is_file() and "__pycache__" not in path.parts:
        out[str(path)] = hashlib.sha256(path.read_bytes()).hexdigest()
  return out


def run(vault: Path, bib: Path, data: Path, builds: Path, quiet: bool = False) -> list[str]:
  """Run every generator; return the files whose content changed overall."""
  before = snapshot(vault, data)
  steps = [
    ("build_paper_stubs", lambda: build_paper_stubs.run(vault, bib, data)),
    ("builds", lambda: run_builds(vault, builds, data)),
    ("build_cite_notes", lambda: build_cite_notes.run(vault, bib, data)),
    ("alias_block_links", lambda: alias_block_links.run(vault, bib, data)),
    ("build_claim_evidence", lambda: build_claim_evidence.run(vault, bib, data)),
    ("build_indexes", lambda: build_indexes.run(vault, bib, data)),
    ("apply_abbr", lambda: apply_abbr.run(vault, bib, data)),
  ]
  for name, step in steps:
    writes = step()
    if not quiet:
      print(f"{name}: {writes} files written")
  after = snapshot(vault, data)
  changed = sorted(path for path in set(before) | set(after) if before.get(path) != after.get(path))
  if not quiet:
    print(f"pipeline: {len(changed)} files changed in total")
    for path in changed:
      print(f"  {path}")
  return changed


def main(argv: list[str] | None = None) -> int:
  parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
  parser.add_argument("--vault", type=Path, default=paths.DEFAULT_VAULT)
  parser.add_argument("--bib", type=Path, default=paths.DEFAULT_BIB)
  parser.add_argument("--data", type=Path, default=paths.DEFAULT_DATA)
  parser.add_argument("--builds", type=Path, default=paths.TOOLS_DIR / "builds")
  parser.add_argument("--katex", help="katex package path, passed to the validator")
  parser.add_argument("--no-validate", action="store_true")
  args = parser.parse_args(argv)
  run(args.vault, args.bib, args.data, args.builds)
  if args.no_validate:
    return 0
  extra = ["--katex", args.katex] if args.katex else []
  return validate_vault.main(["--vault", str(args.vault), "--bib", str(args.bib), "--data", str(args.data), *extra])


if __name__ == "__main__":
  sys.exit(main())
