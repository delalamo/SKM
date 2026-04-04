#!/usr/bin/env python3
"""
generate_mocs.py

Scans content/notes/ for markdown files with hierarchical tags in their YAML
frontmatter (e.g. inverse-folding/training), then auto-generates a MOC page
for each top-level tag root at content/MOCs/<Title>.md.

Tag chips in the rendered site link directly to the appropriate MOC section
via a modified TagList.tsx — no backlink blocks are written to notes.

Usage:
    python3 generate_mocs.py

MOC files are overwritten on every run. Safe to run repeatedly (idempotent).
"""

import re
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from utils import REPO_ROOT

NOTES_DIR = REPO_ROOT / "content" / "notes"
MOCS_DIR  = REPO_ROOT / "content" / "MOCs"

# Maps subtag slugs to human-readable section titles (controls display order).
# Keep in sync with SUBTAG_ANCHORS in quartz/components/TagList.tsx.
SUBTAG_TITLES = {
    "training":    "Training",
    "execution":   "Execution",
    "antibodies":  "Antibodies",
    "datasets":    "Datasets",
    "misc":        "Miscellaneous",
}

# Maps tag roots to MOC page titles.
# Keep in sync with MOC_SLUGS in quartz/components/TagList.tsx.
MOC_TITLES = {
    "inverse-folding":  "Inverse Folding",
    "protein-folding":  "Protein Folding",
    "protein-design":   "Protein Design",
    "antibodies":       "Antibodies",
}


# ---------------------------------------------------------------------------
# Tag parsing
# ---------------------------------------------------------------------------

def parse_frontmatter_tags(filepath: Path) -> list[str]:
    """Return tags from a note's YAML frontmatter, or [] if none."""
    text = filepath.read_text(encoding="utf-8")
    fm_match = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if not fm_match:
        return []
    fm = fm_match.group(1)
    tags: list[str] = []
    block = re.search(r"^tags:\s*\n((?:[ \t]+-[ \t]+\S+\n?)+)", fm, re.MULTILINE)
    if block:
        for line in block.group(1).splitlines():
            t = line.strip().lstrip("- ").strip()
            if t:
                tags.append(t)
    else:
        inline = re.search(r"^tags:\s*(.+)$", fm, re.MULTILINE)
        if inline:
            tags = [t.strip() for t in inline.group(1).split(",") if t.strip()]
    return tags


def collect_notes_by_tag(notes_dir: Path) -> dict[str, dict[str, list[str]]]:
    """
    Returns:  { root_tag: { subtag: [note_title, ...] } }
    Notes with a root-only tag (no slash) are filed under subtag "".
    """
    result: dict[str, dict[str, list[str]]] = defaultdict(lambda: defaultdict(list))
    for md_file in sorted(notes_dir.glob("*.md")):
        title = md_file.stem
        for tag in parse_frontmatter_tags(md_file):
            root, subtag = tag.split("/", 1) if "/" in tag else (tag, "")
            result[root][subtag].append(title)
    return result


# ---------------------------------------------------------------------------
# Title helpers
# ---------------------------------------------------------------------------

def tag_root_to_title(root: str) -> str:
    return MOC_TITLES.get(root, root.replace("-", " ").title())


def subtag_to_section_title(subtag: str) -> str:
    return SUBTAG_TITLES.get(subtag, subtag.replace("-", " ").title())


# ---------------------------------------------------------------------------
# MOC generation
# ---------------------------------------------------------------------------

def generate_moc(root: str, subtag_map: dict[str, list[str]]) -> str:
    moc_title = tag_root_to_title(root)
    lines = [
        "---",
        f"title: {moc_title}",
        "tags:",
        f"  - {root}",
        "---",
        "",
        "> [!info] Auto-generated",
        f"> This page is generated automatically from notes tagged `{root}/*`.",
        "> Re-run `generate_mocs.py` after adding or re-tagging notes to update it.",
        "",
    ]
    known   = [s for s in SUBTAG_TITLES if s in subtag_map]
    unknown = sorted(s for s in subtag_map if s not in SUBTAG_TITLES and s != "")
    ordered = known + unknown + ([""] if "" in subtag_map else [])

    for subtag in ordered:
        section = subtag_to_section_title(subtag) if subtag else "General"
        lines += [f"## {section}", ""]
        for title in sorted(subtag_map[subtag]):
            lines.append(f"- [[{title}]]")
        lines.append("")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    MOCS_DIR.mkdir(parents=True, exist_ok=True)
    notes_by_tag = collect_notes_by_tag(NOTES_DIR)

    if not notes_by_tag:
        print("No tagged notes found in", NOTES_DIR)
        return

    for root, subtag_map in sorted(notes_by_tag.items()):
        moc_title = tag_root_to_title(root)
        moc_text  = generate_moc(root, subtag_map)
        out_path  = MOCS_DIR / f"{moc_title}.md"
        out_path.write_text(moc_text, encoding="utf-8")
        total = sum(len(v) for v in subtag_map.values())
        print(f"  {out_path.relative_to(Path(__file__).parent.parent)}  ({total} notes)")

    print("\nDone.")


if __name__ == "__main__":
    main()
