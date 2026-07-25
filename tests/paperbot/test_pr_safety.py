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


def test_non_bibliography_change_never_enters_auto_refresh() -> None:
  decision = classify_paths(
    ["paper_relevance/README.md"],
    event_name="pull_request",
    same_repository=True,
  )

  assert not decision.auto_refresh
  assert not decision.sensitive_change


def test_manual_dispatch_is_verify_only_even_for_bibliography() -> None:
  decision = classify_paths(
    ["bibliography.bib"],
    event_name="workflow_dispatch",
    same_repository=True,
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
    ".gitattributes",
    "paper_relevance/.gitattributes",
    ".lfsconfig",
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

  assert {
    "paper_relevance/issue_negatives.jsonl",
    "paper_relevance/issue_negative_embeddings.npy",
    "paper_relevance/issue_negative_manifest.jsonl",
  }.issubset(GENERATED_MODEL_PATHS)

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
  assert "steps.safety.outputs.auto_refresh == 'true'" in workflow
  assert "steps.safety.outputs.auto_refresh != 'true'" in workflow
  assert "cache: pip" not in workflow
  assert 'PAPERBOT_DISABLE_ARBITRARY_HTML: "1"' in workflow
  assert "-L \"$GITHUB_WORKSPACE/candidate/bibliography.bib\"" in workflow
  assert "issues: read" in workflow

  backfill = workflow.index("backfill-bibliography")
  sync = workflow.index("sync-issue-negatives")
  refresh = workflow.index("refresh-model")
  assert backfill < sync < refresh

  for path in (
    "paper_relevance/issue_negatives.jsonl",
    "paper_relevance/issue_negative_embeddings.npy",
    "paper_relevance/issue_negative_manifest.jsonl",
  ):
    assert path in workflow


def test_workflow_bootstrap_is_credential_free_and_read_only() -> None:
  workflow = Path(".github/workflows/paper-model-refresh.yml").read_text(
    encoding="utf-8"
  )

  tests_job, refresh_job = workflow.split("  refresh-or-verify:", maxsplit=1)
  assert "permissions:\n      contents: read" in tests_job
  assert "candidate/requirements-paperbot.lock" in tests_job
  assert "steps.dependencies.outputs.bootstrap == 'true'" in tests_job
  assert "tests/paperbot/test_no_remote_summarization.py" in tests_job
  assert "working-directory: candidate" in tests_job
  assert "run: python -m pytest tests/paperbot" in tests_job
  assert "check-model" in tests_job
  assert "secrets." not in tests_job
  assert "git push" not in tests_job

  assert "id: trusted" in refresh_job
  assert "if: steps.trusted.outputs.available == 'true'" in refresh_job
  assert "Initial paperbot bootstrap is validated by the credential-free test job" in (
    refresh_job
  )


def test_workflow_triggers_for_paperbot_test_changes() -> None:
  workflow = Path(".github/workflows/paper-model-refresh.yml").read_text(
    encoding="utf-8"
  )

  trigger = workflow.split("  workflow_dispatch:", maxsplit=1)[0]
  assert "    paths:" not in trigger
  assert "Detect paperbot-relevant changes" in workflow
  assert ":(glob)tests/paperbot/**" in workflow
  assert "name: Test paperbot without credentials" in workflow
  assert "if: always()" in workflow


def test_required_paperbot_gate_cannot_pass_after_detection_or_test_failure() -> None:
  workflow = Path(".github/workflows/paper-model-refresh.yml").read_text(
    encoding="utf-8"
  )
  gate = workflow.split("  paperbot_test_gate:", maxsplit=1)[1].split(
    "  refresh-or-verify:", maxsplit=1
  )[0]

  assert "needs: [detect_paperbot_changes, paperbot_tests]" in gate
  assert "DETECT_RESULT" in gate
  assert '"$DETECT_RESULT" != "success"' in gate
  assert '"$RELEVANT" == "true" && "$TEST_RESULT" != "success"' in gate
  assert '"$RELEVANT" != "true" && "$RELEVANT" != "false"' in gate


def test_workflow_scopes_tokens_to_their_required_steps() -> None:
  workflow = Path(".github/workflows/paper-model-refresh.yml").read_text(
    encoding="utf-8"
  )
  tests_job, refresh_job = workflow.split("  refresh-or-verify:", maxsplit=1)

  before_commit, commit_and_after = workflow.split(
    "      - name: Commit refreshed artifacts to trusted PR branch", maxsplit=1
  )
  assert "issues: read" not in tests_job
  assert "GITHUB_TOKEN:" not in tests_job
  assert "permissions:\n      contents: read\n      issues: read" in refresh_job
  assert "GITHUB_TOKEN: ${{ github.token }}" in before_commit
  assert workflow.count("GITHUB_TOKEN: ${{ github.token }}") == 1
  assert "MODEL_UPDATE_TOKEN" not in before_commit

  sync_step = before_commit.split(
    "      - name: Synchronize closed negative issues", maxsplit=1
  )[1].split("      - name: Refresh and verify model", maxsplit=1)[0]
  assert "steps.safety.outputs.auto_refresh == 'true'" in sync_step
  assert "GITHUB_TOKEN: ${{ github.token }}" in sync_step
  assert "MODEL_UPDATE_TOKEN" not in sync_step

  assert "MODEL_UPDATE_TOKEN: ${{ secrets.MODEL_UPDATE_TOKEN }}" in commit_and_after
  assert '--force-with-lease="refs/heads/$HEAD_REF:$HEAD_SHA"' in commit_and_after
  assert '"HEAD:refs/heads/$HEAD_REF"' in commit_and_after


def test_workflow_stages_exactly_the_generated_allowlist() -> None:
  workflow = Path(".github/workflows/paper-model-refresh.yml").read_text(
    encoding="utf-8"
  )
  stage_block = workflow.split(
    "          git -C candidate add -- \\", maxsplit=1
  )[1].split(
    "          if git -C candidate diff --cached --quiet;", maxsplit=1
  )[0]
  staged = {
    line.strip().removesuffix("\\").strip()
    for line in stage_block.splitlines()
    if line.strip()
  }

  assert staged == GENERATED_PATHS


def test_every_automatic_model_refresh_first_synchronizes_issue_feedback() -> None:
  workflow = Path(".github/workflows/paper-model-refresh.yml").read_text(
    encoding="utf-8"
  )
  backfill_step = workflow.split(
    "      - name: Backfill bibliography abstracts", maxsplit=1
  )[1].split("      - name: Synchronize closed negative issues", maxsplit=1)[0]
  sync_step = workflow.split(
    "      - name: Synchronize closed negative issues", maxsplit=1
  )[1].split("      - name: Refresh and verify model", maxsplit=1)[0]
  refresh_step = workflow.split(
    "      - name: Refresh and verify model", maxsplit=1
  )[1].split("      - name: Reject unexpected generated paths", maxsplit=1)[0]

  automatic_condition = "steps.safety.outputs.auto_refresh == 'true'"
  assert automatic_condition in backfill_step
  assert automatic_condition in sync_step
  assert automatic_condition in refresh_step
  assert "backfill-bibliography" in backfill_step
  assert "sync-issue-negatives" in sync_step
  assert "refresh-model" in refresh_step
