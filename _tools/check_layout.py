#!/usr/bin/env python3
"""Layout test: render paper notes with Quartz and the real CSS, then measure.

Builds a site from a vault (by default the test fixture vault) with Quartz,
opens every non-stub paper note in headless Chromium at several widths and
fails on margin notes overlapping text or each other, or horizontal scroll.
Screenshots at 1280 px go to the output directory for checking by eye.

  python3 _tools/check_layout.py                         # fixture vault
  python3 _tools/check_layout.py --site public           # an existing build of content/
  python3 _tools/check_layout.py --site public --papers guloglu2023 nowak2016
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))

from vaultlib import paths  # noqa: E402
from vaultlib.vault import Vault  # noqa: E402

FIXTURE = TOOLS / "tests" / "fixtures"


def paper_pages(vault_dir: Path, wanted: list[str] | None) -> list[str]:
  vault = Vault(vault_dir)
  pages = []
  for note in sorted(vault.kind("paper"), key=lambda n: n.name):
    if (note.fm or {}).get("fulltext") == "stub":
      continue
    if wanted and note.name not in wanted:
      continue
    pages.append(f"{paths.PAPERS}/{note.name}")
  return pages


def build_site(vault_dir: Path, work: Path) -> Path:
  content = work / "content"
  shutil.copytree(vault_dir, content)
  index = content / "index.md"
  if not index.exists():
    index.write_text("---\ntitle: Layout test\n---\nLayout test vault.\n", encoding="utf-8")
  site = work / "public"
  subprocess.run(["npx", "quartz", "build", "-d", str(content), "-o", str(site)], cwd=paths.REPO_ROOT, check=True)
  return site


def main(argv: list[str] | None = None) -> int:
  parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
  parser.add_argument("--vault", type=Path, default=FIXTURE / "vault_ok", help="vault to build (ignored with --site)")
  parser.add_argument("--site", type=Path, help="an existing Quartz build to check instead of building")
  parser.add_argument("--papers", nargs="*", help="citekeys to check (default: every non-stub paper)")
  parser.add_argument("--out", type=Path, default=paths.TOOLS_DIR / "node" / "out", help="screenshots and report")
  args = parser.parse_args(argv)

  vault_dir = paths.DEFAULT_VAULT if args.site else args.vault
  pages = paper_pages(vault_dir, args.papers)
  if not pages:
    print("no paper notes with text to check")
    return 0
  with tempfile.TemporaryDirectory() as tmp:
    site = args.site or build_site(args.vault, Path(tmp))
    script = TOOLS / "node" / "layout_check.mjs"
    result = subprocess.run(["node", str(script), str(site), str(args.out), *pages], check=False)
  return result.returncode


if __name__ == "__main__":
  sys.exit(main())
