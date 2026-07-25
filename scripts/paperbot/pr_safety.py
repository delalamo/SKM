"""Trusted, testable policy for bibliography-model pull-request automation."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path, PurePosixPath
from typing import Iterable, Sequence


GENERATED_PATHS = frozenset(
  {
    "bibliography.bib",
    "paper_relevance/abstract_provenance.jsonl",
    "paper_relevance/positive_embeddings.npy",
    "paper_relevance/positive_manifest.jsonl",
    "paper_relevance/negative_embeddings.npy",
    "paper_relevance/negative_manifest.jsonl",
    "paper_relevance/issue_negatives.jsonl",
    "paper_relevance/issue_negative_embeddings.npy",
    "paper_relevance/issue_negative_manifest.jsonl",
    "paper_relevance/classifier.npz",
    "paper_relevance/model_manifest.json",
  }
)

GENERATED_MODEL_PATHS = frozenset(GENERATED_PATHS - {"bibliography.bib"})


@dataclass(frozen=True)
class SafetyDecision:
  auto_refresh: bool
  sensitive_change: bool


class UnexpectedGeneratedPaths(RuntimeError):
  def __init__(self, paths: Iterable[str]) -> None:
    self.paths = tuple(sorted(set(paths)))
    super().__init__("Paperbot generated unexpected paths: " + ", ".join(self.paths))


def normalize_repo_path(value: str) -> str:
  path = value.replace("\\", "/").removeprefix("./")
  normalized = PurePosixPath(path)
  if (
    not path
    or normalized.as_posix() == "."
    or normalized.is_absolute()
    or ".." in normalized.parts
  ):
    return ""
  return normalized.as_posix()


def is_sensitive_path(value: str) -> bool:
  path = normalize_repo_path(value)
  if not path:
    return True
  return (
    path.startswith("scripts/paperbot/")
    or path in {"paperbot.toml", "requirements-paperbot.lock"}
    or path.startswith(".github/workflows/")
    or path.startswith("paper_relevance/pubmed_negatives_v1")
    or path.startswith("paper_relevance/negatives_v1")
    or path.startswith("paper_relevance/semantic_scholar")
    or path in GENERATED_MODEL_PATHS
  )


def classify_paths(
  paths: Iterable[str], *, event_name: str, same_repository: bool
) -> SafetyDecision:
  sensitive = any(is_sensitive_path(path) for path in paths)
  return SafetyDecision(
    auto_refresh=(
      event_name == "pull_request" and same_repository and not sensitive
    ),
    sensitive_change=sensitive,
  )


def validate_generated_paths(paths: Iterable[str]) -> None:
  unexpected = [
    path
    for value in paths
    if (path := normalize_repo_path(value)) not in GENERATED_PATHS
  ]
  if unexpected:
    raise UnexpectedGeneratedPaths(unexpected)


def changed_paths(repo: Path, base: str, head: str) -> tuple[str, ...]:
  # Disabling rename detection reports both the deleted sensitive source and
  # the added destination, so a rename cannot hide generator/workflow changes.
  return _git_paths(
    repo, "diff", "--no-renames", "--name-only", "-z", f"{base}...{head}"
  )


def changed_worktree_paths(repo: Path) -> tuple[str, ...]:
  # Disabling rename detection gives every NUL-delimited record one status
  # prefix and one path, which avoids ambiguous parsing of adversarial names.
  output = _git(
    repo,
    "-c",
    "status.renames=false",
    "status",
    "--porcelain=v1",
    "-z",
    "--untracked-files=all",
  )
  paths: list[str] = []
  for record in output.split(b"\0"):
    if not record:
      continue
    if len(record) < 4 or record[2:3] != b" ":
      raise RuntimeError("git returned an invalid porcelain status record")
    paths.append(record[3:].decode("utf-8", errors="surrogateescape"))
  return tuple(paths)


def _git_paths(repo: Path, *arguments: str) -> tuple[str, ...]:
  output = _git(repo, *arguments)
  return tuple(
    value.decode("utf-8", errors="surrogateescape")
    for value in output.split(b"\0")
    if value
  )


def _git(repo: Path, *arguments: str) -> bytes:
  completed = subprocess.run(
    ["git", "-C", str(repo), *arguments],
    check=False,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
  )
  if completed.returncode:
    detail = completed.stderr.decode("utf-8", errors="replace").strip()
    raise RuntimeError(f"git {' '.join(arguments)} failed: {detail}")
  return completed.stdout


def _boolean(value: str) -> bool:
  normalized = value.strip().casefold()
  if normalized in {"1", "true", "yes"}:
    return True
  if normalized in {"0", "false", "no", ""}:
    return False
  raise argparse.ArgumentTypeError(f"invalid boolean: {value!r}")


def build_parser() -> argparse.ArgumentParser:
  parser = argparse.ArgumentParser(prog="paperbot-pr-safety")
  subparsers = parser.add_subparsers(dest="command", required=True)

  classify = subparsers.add_parser("classify")
  classify.add_argument("--repo", type=Path, required=True)
  classify.add_argument("--base", required=True)
  classify.add_argument("--head", required=True)
  classify.add_argument("--event-name", required=True)
  classify.add_argument("--same-repository", type=_boolean, required=True)
  classify.add_argument("--github-output", type=Path)

  validate = subparsers.add_parser("validate-generated")
  validate.add_argument("--repo", type=Path, required=True)
  return parser


def main(argv: Sequence[str] | None = None) -> int:
  args = build_parser().parse_args(argv)
  try:
    if args.command == "classify":
      paths = (
        changed_paths(args.repo, args.base, args.head)
        if args.event_name == "pull_request"
        else ()
      )
      decision = classify_paths(
        paths,
        event_name=args.event_name,
        same_repository=args.same_repository,
      )
      if args.github_output:
        with args.github_output.open("a", encoding="utf-8") as handle:
          handle.write(f"auto_refresh={str(decision.auto_refresh).lower()}\n")
          handle.write(
            f"sensitive_change={str(decision.sensitive_change).lower()}\n"
          )
      print(json.dumps({**asdict(decision), "changed_paths": list(paths)}, sort_keys=True))
      return 0

    paths = changed_worktree_paths(args.repo)
    validate_generated_paths(paths)
    print(json.dumps({"ok": True, "generated_paths": list(paths)}, sort_keys=True))
    return 0
  except UnexpectedGeneratedPaths as error:
    for path in error.paths:
      print(
        f"::error file={path}::Paperbot generated an unexpected path",
        file=sys.stderr,
      )
    return 1
  except (OSError, RuntimeError, ValueError) as error:
    print(f"paperbot PR safety: {error}", file=sys.stderr)
    return 1


if __name__ == "__main__":
  raise SystemExit(main())


__all__ = [
  "GENERATED_MODEL_PATHS",
  "GENERATED_PATHS",
  "SafetyDecision",
  "UnexpectedGeneratedPaths",
  "changed_paths",
  "changed_worktree_paths",
  "classify_paths",
  "is_sensitive_path",
  "main",
  "normalize_repo_path",
  "validate_generated_paths",
]
