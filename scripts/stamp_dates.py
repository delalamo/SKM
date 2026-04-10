#!/usr/bin/env python3
"""
stamp_dates.py

For each note in content/notes/, finds the corresponding source file in the
Obsidian vault and stamps its modification time as `created` and `modified`
fields in the note's YAML frontmatter.

This gives Quartz meaningful per-note timestamps (from actual Obsidian edits)
rather than the batch-conversion filesystem timestamps.

Usage:
    python3 scripts/stamp_dates.py [--dry-run]
"""

import argparse
import datetime
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from utils import REPO_ROOT

# ── Paths ──────────────────────────────────────────────────────────────────────
NOTES_DIR  = REPO_ROOT / "content" / "notes"
SOURCE_DIR = Path(os.environ.get(
    "OBSIDIAN_SOURCE",
    str(Path(__file__).parent.parent.parent / "Unfiltered" / "Sorted_notes" / "Public")
))

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
DATE_FIELD_RE  = re.compile(r"^(created|modified):\s*.+$", re.MULTILINE)


def to_iso(ts: float) -> str:
    """Unix timestamp → ISO-8601 string with second precision, local time."""
    dt = datetime.datetime.fromtimestamp(ts)
    return dt.strftime("%Y-%m-%dT%H:%M:%S")


def build_source_index(source_dir: Path) -> dict[str, Path]:
    """Map lowercased stem → source Path for every .md file under source_dir."""
    index: dict[str, Path] = {}
    for p in source_dir.rglob("*.md"):
        index[p.stem.lower()] = p
    return index


def stamp_note(note_path: Path, source_mtime: float, dry_run: bool) -> bool:
    """
    Add/replace `created` and `modified` in the note's YAML frontmatter.
    Returns True if the file was (or would be) changed.
    """
    text = note_path.read_text("utf-8")
    iso = to_iso(source_mtime)

    m = FRONTMATTER_RE.match(text)
    if not m:
        # No frontmatter — skip
        return False

    fm_body = m.group(1)
    after    = text[m.end():]

    # Remove existing created/modified lines
    new_fm = DATE_FIELD_RE.sub("", fm_body).rstrip("\n")

    # Append dates
    new_fm = new_fm + f"\ncreated: \"{iso}\"\nmodified: \"{iso}\""

    new_text = f"---\n{new_fm}\n---\n{after}"

    if new_text == text:
        return False

    if not dry_run:
        note_path.write_text(new_text, "utf-8")
    return True


def main():
    parser = argparse.ArgumentParser(description="Stamp source file mtimes into Quartz note frontmatter.")
    parser.add_argument("--dry-run", action="store_true", help="Preview without modifying files")
    args = parser.parse_args()

    if not SOURCE_DIR.is_dir():
        print(f"[ERROR] Source directory not found: {SOURCE_DIR}")
        print("        Set OBSIDIAN_SOURCE env var to the path of your Obsidian vault's public folder.")
        sys.exit(1)

    source_index = build_source_index(SOURCE_DIR)
    print(f"Indexed {len(source_index)} source files from {SOURCE_DIR}")

    notes = sorted(NOTES_DIR.glob("*.md"))
    print(f"Processing {len(notes)} notes in {NOTES_DIR}")
    if args.dry_run:
        print("DRY RUN — no files will be modified\n")

    stamped   = 0
    unchanged = 0
    no_match  = 0

    for note in notes:
        stem_lower = note.stem.lower()
        src = source_index.get(stem_lower)
        if src is None:
            no_match += 1
            continue

        src_mtime = src.stat().st_mtime
        changed = stamp_note(note, src_mtime, args.dry_run)
        if changed:
            stamped += 1
            if args.dry_run:
                print(f"  [DRY RUN] {note.name}  ←  {to_iso(src_mtime)}  ({src.name})")
        else:
            unchanged += 1

    print()
    print("── Summary ───────────────────────────────────────────────")
    print(f"  Stamped   : {stamped}")
    print(f"  Unchanged : {unchanged}  (already up to date)")
    print(f"  No match  : {no_match}  (no source file found)")

    if no_match:
        print("\nNote: 'No match' usually means the note was created manually")
        print("      (e.g. newly written notes, MOC-promoted notes).")


if __name__ == "__main__":
    main()
