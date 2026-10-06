from __future__ import annotations

import os
import subprocess
from pathlib import Path

import pytest
import yaml


WORKFLOW = Path(".github/workflows/paper-tests.yml")


def _workflow() -> dict:
  return yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))


def _git(repo: Path, *arguments: str) -> str:
  return subprocess.run(
    ["git", "-C", str(repo), *arguments],
    check=True, capture_output=True, text=True,
  ).stdout.strip()


@pytest.mark.parametrize(
  ("changed_path", "relevant"),
  [
    ("bibliography.bib", False),
    ("content/notes/example.md", False),
    ("scripts/paperbot/model.py", True),
    ("tests/paperbot/test_model.py", True),
    ("paper_relevance/classifier.npz", True),
    ("requirements-paperbot.lock", True),
    ("paperbot.toml", True),
    (".github/workflows/paper-tests.yml", True),
  ],
)
def test_change_detection_skips_bibliography_but_keeps_code_tests(
  tmp_path: Path, changed_path: str, relevant: bool,
) -> None:
  candidate = tmp_path / "candidate"
  candidate.mkdir()
  _git(candidate, "init")
  _git(candidate, "config", "user.name", "Paperbot Test")
  _git(candidate, "config", "user.email", "paperbot@example.invalid")
  _git(candidate, "commit", "--allow-empty", "-m", "base")
  base = _git(candidate, "rev-parse", "HEAD")
  changed = candidate / changed_path
  changed.parent.mkdir(parents=True, exist_ok=True)
  changed.write_text("changed\n", encoding="utf-8")
  _git(candidate, "add", ".")
  _git(candidate, "commit", "-m", "candidate")
  head = _git(candidate, "rev-parse", "HEAD")
  # Exercise the actual workflow shell against local Git history, including
  # its fetch step, without contacting GitHub.
  _git(candidate, "config", f"url.{candidate}.insteadOf", "https://github.com/example/repo.git")
  script = _workflow()["jobs"]["detect_paperbot_changes"]["steps"][-1]["run"]
  output = tmp_path / "outputs"
  subprocess.run(
    ["bash", "-c", script], cwd=tmp_path, check=True, capture_output=True,
    env={
      **os.environ,
      "GITHUB_EVENT_NAME": "pull_request",
      "GITHUB_REPOSITORY": "example/repo",
      "GITHUB_OUTPUT": str(output),
      "BASE_SHA": base,
      "HEAD_SHA": head,
    },
  )
  values = dict(line.split("=", 1) for line in output.read_text().splitlines())
  assert values["relevant"] == str(relevant).lower()
  assert values["lock_changed"] == str(changed_path == "requirements-paperbot.lock").lower()


@pytest.mark.parametrize(
  ("detection", "relevant", "tests", "succeeds"),
  [
    ("success", "false", "skipped", True),
    ("success", "true", "success", True),
    ("success", "true", "failure", False),
    ("success", "true", "skipped", False),
    ("failure", "false", "skipped", False),
    ("success", "", "skipped", False),
  ],
)
def test_required_gate_only_depends_on_relevant_unit_tests(
  detection: str, relevant: str, tests: str, succeeds: bool,
) -> None:
  gate = _workflow()["jobs"]["paperbot_test_gate"]
  result = subprocess.run(
    ["bash", "-c", gate["steps"][0]["run"]], capture_output=True,
    env={
      **os.environ, "DETECT_RESULT": detection,
      "RELEVANT": relevant, "TEST_RESULT": tests,
    },
  )
  assert (result.returncode == 0) == succeeds


def test_pr_workflow_does_not_check_or_publish_model_artifacts() -> None:
  workflow = _workflow()
  text = WORKFLOW.read_text(encoding="utf-8")
  for command in ("check-model", "refresh-model", "backfill-bibliography", "gh pr", "git push"):
    assert command not in text
  assert "secrets." not in text
  for job in workflow["jobs"].values():
    assert job["permissions"] == {"contents": "read"}
  assert workflow["jobs"]["paperbot_test_gate"]["name"] == "Test paperbot without credentials"
  assert not Path(".github/workflows/paper-model-refresh.yml").exists()


def test_sensitive_paperbot_paths_require_maintainer_code_ownership() -> None:
  rules = {
    line.split()[0]: tuple(line.split()[1:])
    for line in Path(".github/CODEOWNERS").read_text().splitlines()
    if line.strip() and not line.lstrip().startswith("#")
  }
  for path in (
    "/.github/CODEOWNERS", "/.github/workflows/paper-*.yml", "/paperbot.toml",
    "/requirements-paperbot.lock", "/scripts/paperbot/", "/paper_relevance/",
    "/tests/paperbot/",
  ):
    assert rules[path] == ("@delalamo",)
