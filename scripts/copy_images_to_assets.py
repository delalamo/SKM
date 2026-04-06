#!/usr/bin/env python3
"""
copy_images_to_assets.py

Scans all markdown files under content/notes/ and content/MOCs/ for
already-converted image references like:
    ![](/assets/image-name.png)

For each referenced image:
  1. Looks up the source file in IMAGES_DIR (matching hyphens back to spaces,
     case-insensitively)
  2. Copies it to ASSETS_DIR (quartz/content/assets/) if not already there

Notes are NOT rewritten — they are already in standard markdown format.

Configuration is read from a .env file at the repo root, or from environment
variables directly.

.env keys (all optional — defaults shown):
    R2_IMAGES_DIR=/absolute/path/to/your/obsidian/Images
    ASSETS_DIR=/absolute/path/to/quartz/content/assets

Usage:
    python3 copy_images_to_assets.py [--dry-run] [--force]

Flags:
    --dry-run   Print what would happen without copying files
    --force     Re-copy images already present in assets/
"""

import argparse
import os
import re
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from utils import REPO_ROOT

# ── .env loader ────────────────────────────────────────────────────────────────
def load_dotenv(path: Path):
    if not path.exists():
        return
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            os.environ.setdefault(key.strip(), value.strip())

load_dotenv(REPO_ROOT / ".env")

# ── Paths ──────────────────────────────────────────────────────────────────────
CONTENT_DIR = REPO_ROOT / "content"
ASSETS_DIR  = Path(os.environ.get("ASSETS_DIR", str(CONTENT_DIR / "assets")))

_DEFAULT_IMAGES_DIR = Path.home() / "Downloads" / "Images_copy"
IMAGES_DIR = Path(os.environ.get("R2_IMAGES_DIR", str(_DEFAULT_IMAGES_DIR)))

# Standard markdown image: ![anything](/assets/filename.ext)
# Use a possessive-style match on the extension to correctly handle filenames
# that contain literal parentheses, e.g. Mean-p-(All-Taxa).png
ASSET_RE = re.compile(
    r'!\[[^\]]*\]\(/assets/(.+?\.(png|jpg|jpeg|gif|webp|svg|PNG|JPG|JPEG|GIF|WEBP|SVG))\)'
)

# ── Helpers ────────────────────────────────────────────────────────────────────
def build_image_index(images_dir: Path) -> dict:
    """
    Build an index keyed by normalised filename (lowercased, spaces→hyphens)
    so we can look up source files from the hyphenated asset names.
    """
    if not images_dir.is_dir():
        print(f"[ERROR] Images directory not found: {images_dir}")
        print(f"        Set R2_IMAGES_DIR in your .env or as an env variable.")
        sys.exit(1)
    index = {}
    for p in images_dir.iterdir():
        if p.is_file() and not p.name.startswith("."):
            normalised = p.name.lower().replace(" ", "-")
            index[normalised] = p
    return index

def resolve_image(asset_filename: str, index: dict) -> Path | None:
    """Look up a /assets/foo-bar.png reference in the source index."""
    return index.get(asset_filename.lower())

# ── Main ───────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="Copy referenced images into quartz/content/assets/."
    )
    parser.add_argument("--dry-run", action="store_true", help="Preview without copying")
    parser.add_argument("--force",   action="store_true", help="Re-copy images already in assets/")
    args = parser.parse_args()

    ASSETS_DIR.mkdir(parents=True, exist_ok=True)

    image_index = build_image_index(IMAGES_DIR)
    print(f"Found {len(image_index)} images in {IMAGES_DIR}")

    # Scan both notes and MOCs
    scan_dirs = [CONTENT_DIR / "notes", CONTENT_DIR / "MOCs"]
    md_files  = []
    for d in scan_dirs:
        if d.is_dir():
            md_files.extend(d.rglob("*.md"))

    print(f"Scanning {len(md_files)} markdown files")
    print(f"Assets destination: {ASSETS_DIR}")
    if args.dry_run:
        print("DRY RUN — no files will be copied\n")

    copied    = 0
    skipped   = 0
    missing   = 0
    not_found = set()

    for md_path in sorted(md_files):
        text    = md_path.read_text(encoding="utf-8")
        matches = list(ASSET_RE.finditer(text))
        if not matches:
            continue

        for m in matches:
            asset_filename = m.group(1)   # e.g. "Pasted-image-20231029.png"
            src_path       = resolve_image(asset_filename, image_index)
            dest_path      = ASSETS_DIR / asset_filename

            if src_path is None:
                if asset_filename not in not_found:
                    print(f"  [MISSING] {asset_filename}  (referenced in {md_path.name})")
                    not_found.add(asset_filename)
                missing += 1
                continue

            if dest_path.exists() and not args.force:
                skipped += 1
                continue

            if not args.dry_run:
                shutil.copy2(src_path, dest_path)
                print(f"  [COPY] {src_path.name}  →  content/assets/{asset_filename}")
            else:
                print(f"  [DRY RUN] {src_path.name}  →  content/assets/{asset_filename}")
            copied += 1

    print()
    print("── Summary ───────────────────────────────────────────────")
    print(f"  Copied  : {copied}")
    print(f"  Skipped : {skipped}  (already in assets/, use --force to re-copy)")
    print(f"  Missing : {missing}  (referenced but source image not found in IMAGES_DIR)")

if __name__ == "__main__":
    main()
