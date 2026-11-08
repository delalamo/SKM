#!/usr/bin/env python3
"""Check that every URL the site has ever published still resolves.

Each line of the URL list is a page path relative to the site root, without
``.html`` (``notes/Some-claim``). A path resolves when the built site has
``<path>.html`` or ``<path>/index.html``; Quartz writes alias redirects the
same way, so a moved note keeps its old URL through ``redirect_from``.

  python3 _tools/check_legacy_urls.py public/ _tools/data/legacy_urls.txt
  python3 _tools/check_legacy_urls.py public/ _tools/data/legacy_urls.txt --write
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

SKIP = {"404"}


def published_paths(site: Path) -> list[str]:
  paths = set()
  for html in site.rglob("*.html"):
    rel = html.relative_to(site).as_posix()[: -len(".html")]
    if rel.endswith("/index"):
      rel = rel[: -len("/index")]
    elif rel == "index":
      rel = ""
    if rel in SKIP or rel.startswith("static/"):
      continue
    paths.add(rel)
  return sorted(paths)


def resolves(site: Path, path: str) -> bool:
  if path == "":
    return (site / "index.html").exists()
  return (site / f"{path}.html").exists() or (site / path / "index.html").exists()


def main(argv: list[str] | None = None) -> int:
  parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
  parser.add_argument("site", type=Path, help="built site directory (Quartz public/)")
  parser.add_argument("urls", type=Path, help="list of legacy page paths")
  parser.add_argument("--write", action="store_true", help="snapshot the site's pages into the list")
  args = parser.parse_args(argv)

  if args.write:
    paths = published_paths(args.site)
    args.urls.parent.mkdir(parents=True, exist_ok=True)
    args.urls.write_text("".join(f"{path}\n" for path in paths), encoding="utf-8")
    print(f"wrote {len(paths)} paths to {args.urls}")
    return 0

  wanted = [line.rstrip("\n") for line in args.urls.read_text(encoding="utf-8").splitlines()]
  missing = [path for path in wanted if not resolves(args.site, path)]
  for path in missing:
    print(f"missing: /{path}")
  print(f"{len(wanted) - len(missing)} of {len(wanted)} legacy URLs resolve")
  return 1 if missing else 0


if __name__ == "__main__":
  sys.exit(main())
