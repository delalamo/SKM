#!/usr/bin/env python3
from __future__ import annotations

"""
Fail when tracked repository files contain duplicate content.

Rules:
  - Non-markdown files are compared byte-for-byte.
  - Markdown files are compared after normalizing line endings and removing
    auto-stamped `created` / `modified` fields from top-level YAML frontmatter.

This catches accidental duplicate asset uploads as well as copied notes that
only differ by timestamp metadata.
"""

from collections import defaultdict
from dataclasses import dataclass
import hashlib
from pathlib import Path
import re
import subprocess
import sys

sys.path.insert(0, str(Path(__file__).parent))
from utils import REPO_ROOT

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---(\n|$)", re.DOTALL)
STAMP_RE = re.compile(r"^(created|modified):\s*.*$")


@dataclass(frozen=True)
class FileRecord:
    path: Path
    exact_hash: str
    comparison_hash: str


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def tracked_files(root: Path) -> list[Path]:
    try:
        proc = subprocess.run(
            ["git", "ls-files", "-z"],
            cwd=root,
            check=True,
            capture_output=True,
        )
    except FileNotFoundError as exc:
        raise RuntimeError("git is required to enumerate tracked files") from exc
    except subprocess.CalledProcessError as exc:
        raise RuntimeError("failed to enumerate tracked files with git ls-files") from exc

    files: list[Path] = []
    for raw_path in proc.stdout.split(b"\0"):
        if not raw_path:
            continue
        rel = Path(raw_path.decode("utf-8"))
        full = root / rel
        if full.is_file():
            files.append(full)
    return files


def normalize_markdown(raw: bytes) -> bytes:
    text = raw.decode("utf-8")
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    match = FRONTMATTER_RE.match(text)
    if match:
        frontmatter_lines = match.group(1).split("\n")
        filtered_lines = [line for line in frontmatter_lines if not STAMP_RE.match(line)]
        cleaned_frontmatter = "\n".join(filtered_lines)
        text = f"---\n{cleaned_frontmatter}\n---{match.group(2)}{text[match.end():]}"

    return (text.rstrip() + "\n").encode("utf-8")


def comparison_bytes(path: Path, raw: bytes) -> bytes:
    if path.suffix.lower() == ".md":
        return normalize_markdown(raw)
    return raw


def find_duplicate_groups(root: Path) -> list[tuple[list[FileRecord], bool]]:
    by_hash: dict[str, list[FileRecord]] = defaultdict(list)

    for path in tracked_files(root):
        raw = path.read_bytes()
        rel = path.relative_to(root)
        exact_hash = sha256(raw)
        comparison_hash = sha256(comparison_bytes(path, raw))
        by_hash[comparison_hash].append(
            FileRecord(path=rel, exact_hash=exact_hash, comparison_hash=comparison_hash)
        )

    groups: list[tuple[list[FileRecord], bool]] = []
    for records in by_hash.values():
        if len(records) < 2:
            continue
        ordered = sorted(records, key=lambda record: record.path.as_posix())
        exact_duplicate = len({record.exact_hash for record in ordered}) == 1
        groups.append((ordered, exact_duplicate))

    groups.sort(key=lambda group: group[0][0].path.as_posix())
    return groups


def main() -> int:
    groups = find_duplicate_groups(REPO_ROOT)
    if not groups:
        print("No duplicate tracked files found.")
        return 0

    print("Duplicate tracked files found:")
    for records, exact_duplicate in groups:
        reason = "exact content" if exact_duplicate else "markdown content ignoring created/modified"
        print(f"\n- {reason}")
        for record in records:
            print(f"  - {record.path.as_posix()}")

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
