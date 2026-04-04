#!/usr/bin/env python3
"""
copy_images_to_assets.py

Scans all markdown notes under NOTES_DIR for Obsidian image embeds like:
    ![[image.png]]
    ![[image.png|400]]

For each referenced image:
  1. Looks it up in IMAGES_DIR
  2. Copies it to ASSETS_DIR (quartz/static/assets/) if not already there
  3. Rewrites the embed to standard markdown: ![](/assets/image-name.png)

Spaces in filenames are replaced with dashes in the destination filename and URL.

Configuration is read from a .env file in the same directory as this script,
or from environment variables directly.

.env keys (all optional — defaults are relative to the script location):
    IMAGES_DIR=/absolute/path/to/your/obsidian/Images
    ASSETS_DIR=/absolute/path/to/quartz/static/assets

Usage:
    python3 copy_images_to_assets.py [--dry-run] [--force]

Flags:
    --dry-run   Print what would happen without copying or editing files
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

from utils import REPO_ROOT

load_dotenv(REPO_ROOT / ".env")

# ── Paths ──────────────────────────────────────────────────────────────────────
NOTES_DIR  = REPO_ROOT / "content" / "notes"
ASSETS_DIR = Path(os.environ.get("ASSETS_DIR", str(REPO_ROOT / "static" / "assets")))

_DEFAULT_IMAGES_DIR = Path.home() / "Downloads" / "Images_copy"
IMAGES_DIR = Path(os.environ.get("IMAGES_DIR", str(_DEFAULT_IMAGES_DIR)))

# Obsidian image embed: ![[filename.ext]] or ![[filename.ext|width]]
EMBED_RE = re.compile(
    r'!\[\[([^\]|#]+?\.(png|jpg|jpeg|gif|webp|svg|PNG|JPG|JPEG|GIF|WEBP|SVG))(?:\|[^\]]+)?\]\]'
)

# ── Helpers ────────────────────────────────────────────────────────────────────
def build_image_index(images_dir: Path) -> dict:
    """
    Build a case-insensitive filename → Path index using os.listdir().
    """
    images_dir_str = str(images_dir)
    if not os.path.isdir(images_dir_str):
        print(f"[ERROR] Images directory not found: {images_dir_str}")
        print(f"        Check IMAGES_DIR in your .env or pass --images-dir")
        sys.exit(1)
    index = {}
    for name in os.listdir(images_dir_str):
        if name.startswith("."):
            continue
        full = os.path.join(images_dir_str, name)
        if os.path.isfile(full):
            index[name.lower()] = Path(full)
    return index

def resolve_image(filename: str, index: dict):
    return index.get(filename.lower())

def asset_name(filename: str) -> str:
    """Replace spaces with dashes for a clean, URL-safe asset filename."""
    return filename.replace(" ", "-")

# ── Main ───────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="Copy Obsidian image embeds into quartz/static/assets/ and rewrite note links."
    )
    parser.add_argument("--dry-run", action="store_true", help="Preview without copying or editing")
    parser.add_argument("--force",   action="store_true", help="Re-copy images already in assets/")
    args = parser.parse_args()

    ASSETS_DIR.mkdir(parents=True, exist_ok=True)

    image_index = build_image_index(IMAGES_DIR)
    print(f"Found {len(image_index)} images in {IMAGES_DIR}")

    md_files = list(NOTES_DIR.rglob("*.md"))
    print(f"Scanning {len(md_files)} notes in {NOTES_DIR}")
    print(f"Assets destination: {ASSETS_DIR}")
    if args.dry_run:
        print("DRY RUN — no files will be modified\n")

    copied  = 0
    skipped = 0
    missing = 0
    rewrote = 0
    not_found = set()

    for md_path in sorted(md_files):
        text = md_path.read_text(encoding="utf-8")
        matches = list(EMBED_RE.finditer(text))
        if not matches:
            continue

        new_text = text
        changed  = False

        for m in matches:
            filename   = m.group(1)
            full_embed = m.group(0)
            src_path   = resolve_image(filename, image_index)

            if src_path is None:
                if filename not in not_found:
                    print(f"  [MISSING] {filename}  (in {md_path.name})")
                    not_found.add(filename)
                missing += 1
                continue

            dest_filename = asset_name(src_path.name)
            dest_path     = ASSETS_DIR / dest_filename
            url           = f"/assets/{dest_filename}"
            md_image      = f"![]({url})"

            if not args.dry_run:
                if not args.force and dest_path.exists():
                    skipped += 1
                else:
                    shutil.copy2(str(src_path), str(dest_path))
                    print(f"  [COPY] {src_path.name}  →  static/assets/{dest_filename}")
                    copied += 1
            else:
                print(f"  [DRY RUN] {src_path.name}  →  static/assets/{dest_filename}  ({url})")
                copied += 1

            if full_embed in new_text:
                new_text = new_text.replace(full_embed, md_image, 1)
                changed  = True
                rewrote += 1

        if changed and not args.dry_run:
            md_path.write_text(new_text, encoding="utf-8")
            print(f"  [REWRITE] {md_path.name}")

    print()
    print("── Summary ───────────────────────────────────────────────")
    print(f"  Copied  : {copied}")
    print(f"  Skipped : {skipped}  (already in assets/, use --force to re-copy)")
    print(f"  Missing : {missing}  (embed found but source image not in IMAGES_DIR)")
    print(f"  Rewrote : {rewrote}  note embeds → /assets/ URLs")

if __name__ == "__main__":
    main()
