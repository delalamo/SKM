#!/usr/bin/env python3
"""
format_notes.py — Prepares Obsidian notes for Quartz publishing. Two jobs:

  1. Converts [[10.xxx__yyy|Author Year]] citation wikilinks to markdown footnotes,
     fetching full citation metadata from the CrossRef API via doi.org content negotiation.
  2. (--refresh-citations) Re-fetches bare fallback footnote definitions of the form
       [^key]: Author Year. https://doi.org/DOI
     and replaces them with full citations. Use this when notes were previously
     processed without network access (e.g. in a sandbox).

Run manually when porting or adding notes. Idempotent: re-running a fully processed
note produces no changes.

Usage:
    python3 format_notes.py                            # convert DOI wikilinks in all notes
    python3 format_notes.py content/notes/foo.md       # single file
    python3 format_notes.py --refresh-citations        # upgrade bare fallback citations
    python3 format_notes.py --refresh-citations content/notes/foo.md
"""

import re
import sys
import json
import time
import urllib.request
import urllib.parse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from utils import REPO_ROOT

NOTES_DIR = REPO_ROOT / "content" / "notes"

# DOI citation wikilinks: [[10.1038__s41467-024-45621-4|Ding et al 2024]]
CITE_RE = re.compile(r'\[\[(10\.[^|\]]+)\|([^\]]+)\]\]')

# YAML frontmatter block at file start
FM_RE = re.compile(r'^---\r?\n(.*?)\r?\n---\r?\n?', re.DOTALL)


# ---------------------------------------------------------------------------
# DOI / citation helpers
# ---------------------------------------------------------------------------

def doi_from_target(target: str) -> str:
    """'10.1038__s41467-024-45621-4'  →  '10.1038/s41467-024-45621-4'"""
    return target.replace('__', '/')


def footnote_key(display: str, used: set[str]) -> str:
    """'Smith et al 2022'  →  'smith2022' (deduplicated with 'b', 'c', …)"""
    tokens = display.strip().split()
    name = re.sub(r'[^a-zA-Z]', '', tokens[0]).lower()
    year = next((t[:4] for t in reversed(tokens) if re.fullmatch(r'\d{4}[a-z]?', t)), '')
    base = f"{name}{year}"
    key, suffix = base, ord('b')
    while key in used:
        key = base + chr(suffix)
        suffix += 1
    return key


def fetch_csl_json(doi: str) -> dict | None:
    """
    Fetch CSL-JSON metadata from doi.org content negotiation.
    Falls back to CrossRef REST API if doi.org does not return parseable JSON.
    """
    # Primary: doi.org content negotiation
    url = f"https://doi.org/{urllib.parse.quote(doi, safe='/')}"
    req = urllib.request.Request(url, headers={
        "Accept": "application/vnd.citationstyles.csl+json",
        "User-Agent": "QuartzKnowledgeBase/1.0 (mailto:user@example.com)",
    })
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read())
    except Exception:
        pass

    # Fallback: CrossRef REST API
    url2 = f"https://api.crossref.org/works/{urllib.parse.quote(doi, safe='/')}"
    req2 = urllib.request.Request(url2, headers={
        "User-Agent": "QuartzKnowledgeBase/1.0 (mailto:user@example.com)"
    })
    try:
        with urllib.request.urlopen(req2, timeout=15) as resp:
            msg = json.loads(resp.read()).get("message", {})
            # CrossRef returns slightly different field names; normalise key ones
            if "issued" not in msg and "published-print" in msg:
                msg["issued"] = msg["published-print"]
            return msg
    except Exception as e:
        print(f"    ⚠  could not fetch {doi}: {e}")
        return None


def format_citation(csl: dict, doi: str) -> str:
    """Render a CSL-JSON (or CrossRef message) dict as a plain-text citation."""
    authors = csl.get("author", [])
    if not authors:
        author_str = "Unknown"
    elif len(authors) == 1:
        author_str = authors[0].get("family", "Unknown")
    elif len(authors) == 2:
        author_str = (
            f"{authors[0].get('family', '?')} & {authors[1].get('family', '?')}"
        )
    else:
        author_str = f"{authors[0].get('family', 'Unknown')} et al."

    year = ""
    for field in ("issued", "published", "published-print", "published-online", "created"):
        dp = csl.get(field, {}).get("date-parts", [[]])[0]
        if dp:
            year = str(dp[0])
            break

    title = re.sub(r'<[^>]+>', '', csl.get("title", "Untitled"))
    # CrossRef sometimes returns title as a list
    if isinstance(title, list):
        title = title[0] if title else "Untitled"
    # Collapse any embedded newlines / extra whitespace into a single space
    title = re.sub(r'\s+', ' ', title).strip()

    container = csl.get("container-title", "")
    if isinstance(container, list):
        container = container[0] if container else ""
    container = re.sub(r'\s+', ' ', container).strip()

    parts = [author_str]
    if year:
        parts.append(f"({year})")
    parts.append(f'"{title}."')
    if container:
        parts.append(f"*{container}*.")
    parts.append(f"https://doi.org/{doi}")
    return " ".join(parts)


# ---------------------------------------------------------------------------
# Frontmatter helpers
# ---------------------------------------------------------------------------

def strip_tags_from_frontmatter(fm_body: str) -> tuple[str, list[str]]:
    """
    Remove the 'tags:' field from a YAML frontmatter body string.
    Returns (cleaned_frontmatter_body, [tag, tag, ...]).
    """
    tags: list[str] = []
    result: list[str] = []
    lines = fm_body.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        # Block form:   tags:\n  - foo\n  - bar
        if re.match(r'^tags:\s*$', line):
            i += 1
            while i < len(lines) and re.match(r'^\s+-\s+\S', lines[i]):
                tags.append(lines[i].strip().lstrip('- ').strip())
                i += 1
            continue
        # Inline form:  tags: foo, bar
        m = re.match(r'^tags:\s+(.+)$', line)
        if m:
            for t in m.group(1).split(','):
                t = t.strip()
                if t:
                    tags.append(t)
            i += 1
            continue
        result.append(line)
        i += 1
    return '\n'.join(result), tags


# ---------------------------------------------------------------------------
# Per-file processing
# ---------------------------------------------------------------------------

def process_note(path: Path) -> bool:
    """Transform a single note in-place. Returns True if modified."""
    original = path.read_text(encoding='utf-8')
    text = original
    tags: list[str] = []

    # ── 1. Tags stay in frontmatter — leave them alone ─────────────────────
    # (generate_mocs.py reads them; they render invisibly in Quartz unless
    # a Tags component is explicitly added to the layout)

    # ── 2. Convert DOI wikilinks to footnotes ──────────────────────────────
    doi_to_display: dict[str, str] = {}
    doi_to_key:     dict[str, str] = {}
    used_keys: set[str] = set()

    for m in CITE_RE.finditer(text):
        doi = doi_from_target(m.group(1))
        display = m.group(2)
        if doi not in doi_to_display:
            doi_to_display[doi] = display
            key = footnote_key(display, used_keys)
            used_keys.add(key)
            doi_to_key[doi] = key

    if doi_to_display:
        # Replace inline occurrences — emit only the footnote marker, not the
        # display text, since the full citation is in the footnote definition.
        def replacer(m: re.Match) -> str:
            doi = doi_from_target(m.group(1))
            return f"[^{doi_to_key[doi]}]"

        text = CITE_RE.sub(replacer, text)

        # Fetch citations and append footnote definitions at the bottom.
        # Do NOT add a "## References" heading — Quartz automatically renders
        # footnote definitions ([^key]: ...) as a styled "References" section.
        print(f"  Fetching {len(doi_to_display)} citation(s)…")
        ref_lines = [""]
        for doi, display in doi_to_display.items():
            key = doi_to_key[doi]
            print(f"    {doi} … ", end='', flush=True)
            csl = fetch_csl_json(doi)
            time.sleep(0.3)   # polite rate-limiting
            if csl:
                citation = format_citation(csl, doi)
                print("✓")
            else:
                citation = f"{display}. https://doi.org/{doi}"
                print("fallback")
            ref_lines.append(f"[^{key}]: {citation}")

        text = text.rstrip('\n') + '\n' + '\n'.join(ref_lines) + '\n'

    # ── 3. Tags stay in frontmatter — no inline hashtags written ──────────
    # generate_mocs.py reads tags from frontmatter and adds a visible backlink
    # to the appropriate MOC section, which is cleaner than rendered hashtags.

    # ── Write if changed ──────────────────────────────────────────────────
    if text == original:
        return False
    path.write_text(text, encoding='utf-8')
    return True


# ---------------------------------------------------------------------------
# Refresh fallback citations
# ---------------------------------------------------------------------------

# Matches bare fallback footnote lines: [^key]: Some Text. https://doi.org/DOI
# Full citations always contain a quoted title (") or italicised journal (*),
# so we only target lines that have neither.
FALLBACK_FN_RE = re.compile(
    r'^\[\^(\w+)\]: (?![^"*\n]*[*"])(.+?)\. (https://doi\.org/(.+))\s*$',
    re.MULTILINE,
)

def refresh_citations(path: Path) -> bool:
    """
    Find bare fallback footnote definitions in a note and replace them with
    full citations fetched from doi.org / CrossRef. Returns True if modified.
    """
    original = path.read_text(encoding='utf-8')
    text = original

    matches = list(FALLBACK_FN_RE.finditer(text))
    if not matches:
        return False

    print(f"  Found {len(matches)} bare citation(s) to refresh…")
    for m in matches:
        key        = m.group(1)
        doi        = m.group(4).strip()
        old_line   = m.group(0)

        print(f"    [{key}] {doi} … ", end='', flush=True)
        csl = fetch_csl_json(doi)
        time.sleep(0.3)

        if csl:
            citation = format_citation(csl, doi)
            new_line = f"[^{key}]: {citation}"
            print("✓")
        else:
            print("fallback (could not fetch)")
            continue  # leave the existing bare line unchanged

        text = text.replace(old_line, new_line, 1)

    if text == original:
        return False
    path.write_text(text, encoding='utf-8')
    return True


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    args = sys.argv[1:]
    refresh_mode = '--refresh-citations' in args
    file_args = [a for a in args if not a.startswith('--')]

    if file_args:
        targets = [Path(p) for p in file_args]
    else:
        targets = sorted(NOTES_DIR.glob('*.md'))

    action = refresh_citations if refresh_mode else process_note
    mode_label = "Refreshing citations" if refresh_mode else "Processing notes"
    print(f"{mode_label} ({len(targets)} file(s))…\n")

    modified = 0
    for path in targets:
        print(f"→ {path.name}")
        try:
            changed = action(path)
        except Exception as e:
            print(f"  ✗ error: {e}")
            continue
        if changed:
            modified += 1
            print("  ✓ updated")
        else:
            print("  — no changes")

    print(f"\nDone. {modified}/{len(targets)} file(s) updated.")


if __name__ == "__main__":
    main()
