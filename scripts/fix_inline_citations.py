#!/usr/bin/env python3
"""
fix_inline_citations.py

Removes redundant inline author-year text that appears immediately before a
footnote marker, since the full citation is already in the footnote definition.

Before:  **Finding** (Smith et al 2022[^smith2022]).
After:   **Finding**[^smith2022].

Before:  (Baek et al 2023[^baek2023], Lee et al 2024[^lee2024])
After:   [^baek2023][^lee2024]

Before:  *Figure from Ferrari et al 2025[^ferrari2025]*
After:   *Figure from [^ferrari2025]*

Before:  (as judged by ProteinGym; Notin et al 2022[^notin2022])
After:   (as judged by ProteinGym; [^notin2022])

Also warns (step 4) about any un-migrated DOI-based citations that were never
converted to [^key] footnotes:

  [10.xxxx/yyy|Author Year]    — broken single-bracket (notes)
  [[10.xxxx/yyy|Author Year]]  — wikilink in a Figure caption (tag pages)

Run scripts/migrate_wikilink_citations.py to fix those automatically.

Usage:
    python3 scripts/fix_inline_citations.py [--dry-run] [file ...]
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from utils import REPO_ROOT

NOTES_DIR = REPO_ROOT / "content" / "notes"
TAGS_DIR  = REPO_ROOT / "content" / "tags"

FM_RE = re.compile(r'\A---\n.*?\n---\n', re.DOTALL)

# ---------------------------------------------------------------------------
# Step 1 — strip author-year text immediately before [^key]
#
# Matches patterns like:
#   Smith 2022            Lu et al 2024b
#   Smith & Jones 2022    del Alamo et al 2022a
#   de March et al 2024   Ouyang-Zhang et al 2025
# ---------------------------------------------------------------------------
_SURNAME = (
    r'(?:(?:de[lm]?|von|van|le|la)\s+)?'  # optional lowercase prefix (del, de, van …)
    r'[A-Z\xC0-\xD6\xD8-\xDE]'            # capital letter, including accented (À-Ö, Ø-Þ)
    r'[A-Za-z0-9\-\xC0-\xFF]+'            # rest of surname, including accented chars (À-ÿ)
)
_COAUTHOR = r'(?:\s+(?:et\s+al\.?|&\s+' + _SURNAME + r'))?'
AUTHOR_YEAR_RE = re.compile(
    r'(?:' + _SURNAME + _COAUTHOR + r')'
    r'\s+\d{4}[a-z]?'   # year, optional letter suffix
    r'(?=\[\^)'          # lookahead: immediately followed by [^
)


def strip_author_years(text: str) -> str:
    """Remove author-year strings immediately before footnote markers."""
    return AUTHOR_YEAR_RE.sub('', text)


# ---------------------------------------------------------------------------
# Step 2 — collapse ( [^key1] , [^key2] ) → [^key1][^key2]
#           when the parens contain ONLY footnote refs (plus whitespace/commas)
# ---------------------------------------------------------------------------
PARENS_FN_ONLY_RE = re.compile(
    r'\(\s*'
    r'(\[\^[\w]+\]'               # first [^key]
    r'(?:[,\s]*\[\^[\w]+\])*)'    # optional additional ,  [^key]
    r'\s*\)'
)


def collapse_paren_footnotes(text: str) -> str:
    """Replace (  [^a] , [^b]  ) with [^a][^b]."""
    def _replace(m: re.Match) -> str:
        refs = re.findall(r'\[\^\w+\]', m.group(1))
        return ''.join(refs)
    return PARENS_FN_ONLY_RE.sub(_replace, text)


# ---------------------------------------------------------------------------
# Step 3 — clean up any double-spaces left after stripping author-year text
#          inside parentheses, e.g. "(as judged by  [^notin2022])" → one space
# ---------------------------------------------------------------------------
DOUBLE_SPACE_RE = re.compile(r'  +')

# ---------------------------------------------------------------------------
# Step 4 — detect un-migrated DOI-based citation patterns and warn.
#
# These should never appear in a processed vault — if they do, run
# migrate_wikilink_citations.py first.
#
# Patterns detected (both use the encoded DOI form  10.xxxx__yyy):
#   [10.xxxx__yyy|Author Year]     single-bracket broken markup (notes)
#   [[10.xxxx__yyy|Author Year]]   wikilink in a Figure caption (tag pages)
# ---------------------------------------------------------------------------
UNMIGRATED_SINGLE_RE = re.compile(r'\[10\.[^\]|]+\|[^\]]+\](?!\])')
UNMIGRATED_DOUBLE_RE = re.compile(r'\[\[10\.[^\]|]+\|[^\]]+\]\]')


def find_unmigrated(text: str) -> list[tuple[int, str]]:
    """Return (line_number, line) pairs for any un-migrated DOI citations.

    Rules:
    * Single-bracket [10.xxx|Author Year] — always broken, always flag.
    * Double-bracket [[10.xxx|Author Year]] — flag ONLY in *Figure/Table/Image
      from …* caption lines, since body-text wikilinks in tag pages are intentional.
    """
    hits = []
    CAPTION_RE = re.compile(r'^\s*\*.*(?:Figure|Table|Image|Panel)\s+from', re.IGNORECASE)
    for lineno, line in enumerate(text.splitlines(), 1):
        # Skip footnote-definition lines
        if re.match(r'^\[\^\w+\]:', line):
            continue
        if UNMIGRATED_SINGLE_RE.search(line):
            hits.append((lineno, line.rstrip()))
        elif UNMIGRATED_DOUBLE_RE.search(line) and CAPTION_RE.match(line):
            hits.append((lineno, line.rstrip()))
    return hits


# ---------------------------------------------------------------------------
# Per-file processing
# ---------------------------------------------------------------------------

def process(path: Path, dry_run: bool) -> tuple[bool, list[tuple[int, str]]]:
    """
    Returns (was_modified, unmigrated_hits).
    unmigrated_hits is a list of (lineno, line) for any un-migrated DOI citations.
    """
    original = path.read_text('utf-8')

    # Step 4 — warn about un-migrated DOI citations before doing anything else
    unmigrated = find_unmigrated(original)

    # Split into frontmatter + body (footnote definitions are part of body)
    m = FM_RE.match(original)
    if m:
        fm, body = original[:m.end()], original[m.end():]
    else:
        fm, body = '', original

    # Split body into content lines and footnote-definition lines.
    # We only transform content lines — never touch [^key]: definition lines.
    content_lines = []
    fn_def_lines  = []
    in_fn_section = False

    for line in body.splitlines(keepends=True):
        if re.match(r'^\[\^\w+\]:', line):
            in_fn_section = True
        if in_fn_section:
            fn_def_lines.append(line)
        else:
            content_lines.append(line)

    content = ''.join(content_lines)

    content = strip_author_years(content)
    content = collapse_paren_footnotes(content)
    content = DOUBLE_SPACE_RE.sub(' ', content)

    updated = fm + content + ''.join(fn_def_lines)

    modified = (updated != original)
    if modified and not dry_run:
        path.write_text(updated, 'utf-8')
    return modified, unmigrated


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    args      = sys.argv[1:]
    dry_run   = '--dry-run' in args
    file_args = [a for a in args if not a.startswith('--')]

    if file_args:
        targets = [Path(p) for p in file_args]
    else:
        targets = sorted(NOTES_DIR.glob('*.md')) + sorted(TAGS_DIR.glob('*.md'))

    if dry_run:
        print('DRY RUN — no files will be modified\n')

    modified = 0
    warnings: list[str] = []

    for path in targets:
        changed, unmigrated = process(path, dry_run)
        if changed:
            modified += 1
            print(f'  ✓  {path.name}')
        if unmigrated:
            for lineno, line in unmigrated:
                warnings.append(f'  {path.name}:{lineno}: {line}')

    print(f'\n{"Would modify" if dry_run else "Modified"} {modified}/{len(targets)} file(s).')

    if warnings:
        print(
            f'\nWARNING: {len(warnings)} un-migrated DOI citation(s) found.\n'
            'Run  scripts/migrate_wikilink_citations.py  to convert them.\n'
        )
        for w in warnings:
            print(w)


if __name__ == '__main__':
    main()
