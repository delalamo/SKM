from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from scripts.paperbot.pr_safety import (
  GENERATED_MODEL_PATHS,
  GENERATED_PATHS,
  UnexpectedGeneratedPaths,
  changed_paths,
  changed_worktree_paths,
  classify_paths,
  validate_generated_paths,
)


def _git(repo: Path, *arguments: str) -> str:
  return subprocess.run(
    ["git", "-C", str(repo), *arguments],
    check=True,
    capture_output=True,
    text=True,
  ).stdout.strip()


def test_same_repository_bibliography_change_enables_auto_refresh() -> None:
  decision = classify_paths(
    ["bibliography.bib"], event_name="pull_request", same_repository=True
  )

  assert decision.auto_refresh
  assert not decision.sensitive_change


def test_fork_never_enters_the_credentialed_auto_refresh_path() -> None:
  decision = classify_paths(
    ["bibliography.bib"], event_name="pull_request", same_repository=False
  )

  assert not decision.auto_refresh
  assert not decision.sensitive_change


@pytest.mark.parametrize(
  "path",
  [
    "scripts/paperbot/model.py",
    "paperbot.toml",
    "requirements-paperbot.lock",
    ".github/workflows/paper-model-refresh.yml",
    "paper_relevance/pubmed_negatives_v1.jsonl",
    "paper_relevance/pubmed_negatives_v1_metadata.json",
    # Retain fail-closed handling for the retired corpus path.
    "paper_relevance/negatives_v1.jsonl",
    *sorted(GENERATED_MODEL_PATHS),
  ],
)
def test_sensitive_inputs_and_generated_artifacts_disable_auto_refresh(
  path: str,
) -> None:
  decision = classify_paths(
    ["bibliography.bib", path],
    event_name="pull_request",
    same_repository=True,
  )

  assert decision.sensitive_change
  assert not decision.auto_refresh


def test_generated_allowlist_fails_closed() -> None:
  validate_generated_paths(GENERATED_PATHS)

  with pytest.raises(UnexpectedGeneratedPaths) as caught:
    validate_generated_paths(["bibliography.bib", "content/unexpected.md"])

  assert caught.value.paths == ("content/unexpected.md",)


def test_git_path_readers_cover_pr_diff_and_worktree_allowlist(tmp_path: Path) -> None:
  repo = tmp_path / "repository"
  repo.mkdir()
  _git(repo, "init")
  _git(repo, "config", "user.name", "Paperbot Test")
  _git(repo, "config", "user.email", "paperbot@example.invalid")
  bibliography = repo / "bibliography.bib"
  bibliography.write_text("@article{one}\n", encoding="utf-8")
  _git(repo, "add", "bibliography.bib")
  _git(repo, "commit", "-m", "base")
  base = _git(repo, "rev-parse", "HEAD")

  bibliography.write_text("@article{two}\n", encoding="utf-8")
  _git(repo, "commit", "-am", "candidate")
  head = _git(repo, "rev-parse", "HEAD")
  assert changed_paths(repo, base, head) == ("bibliography.bib",)

  bibliography.write_text("@article{generated}\n", encoding="utf-8")
  assert changed_worktree_paths(repo) == ("bibliography.bib",)
  validate_generated_paths(changed_worktree_paths(repo))

  (repo / "unexpected.txt").write_text("not generated", encoding="utf-8")
  with pytest.raises(UnexpectedGeneratedPaths):
    validate_generated_paths(changed_worktree_paths(repo))


def test_sensitive_source_rename_cannot_bypass_auto_refresh_gate(
  tmp_path: Path,
) -> None:
  repo = tmp_path / "repository"
  (repo / "scripts" / "paperbot").mkdir(parents=True)
  _git(repo, "init")
  _git(repo, "config", "user.name", "Paperbot Test")
  _git(repo, "config", "user.email", "paperbot@example.invalid")
  model = repo / "scripts" / "paperbot" / "model.py"
  model.write_text("trusted = True\n", encoding="utf-8")
  _git(repo, "add", ".")
  _git(repo, "commit", "-m", "base")
  base = _git(repo, "rev-parse", "HEAD")

  (repo / "notes").mkdir()
  _git(repo, "mv", "scripts/paperbot/model.py", "notes/model.txt")
  _git(repo, "commit", "-m", "rename")
  head = _git(repo, "rev-parse", "HEAD")

  paths = changed_paths(repo, base, head)
  assert "scripts/paperbot/model.py" in paths
  assert "notes/model.txt" in paths
  decision = classify_paths(paths, event_name="pull_request", same_repository=True)
  assert decision.sensitive_change
  assert not decision.auto_refresh


def test_workflow_routes_push_and_validation_through_trusted_policy() -> None:
  workflow = Path(".github/workflows/paper-model-refresh.yml").read_text(
    encoding="utf-8"
  )

  assert "scripts.paperbot.pr_safety classify" in workflow
  assert "scripts.paperbot.pr_safety validate-generated" in workflow
  assert "case \"$path\"" not in workflow
  assert "if: steps.safety.outputs.auto_refresh == 'true'" in workflow
  assert "if: steps.safety.outputs.auto_refresh != 'true'" in workflow
  assert "cache: pip" not in workflow
  assert 'PAPERBOT_DISABLE_ARBITRARY_HTML: "1"' in workflow
  assert "-L \"$GITHUB_WORKSPACE/candidate/bibliography.bib\"" in workflow
