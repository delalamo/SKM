from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path

import pytest
import yaml

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
    ".github/CODEOWNERS",
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


def test_sensitive_paperbot_paths_require_maintainer_code_ownership() -> None:
  codeowners = Path(".github/CODEOWNERS").read_text(encoding="utf-8")
  expected = {
    "/.github/CODEOWNERS",
    "/.github/workflows/paper-*.yml",
    "/paperbot.toml",
    "/requirements-paperbot.lock",
    "/scripts/paperbot/",
    "/paper_relevance/",
    "/tests/paperbot/",
  }
  rules = {
    line.split()[0]: tuple(line.split()[1:])
    for line in codeowners.splitlines()
    if line.strip() and not line.lstrip().startswith("#")
  }

  assert expected.issubset(rules)
  for path in expected:
    assert rules[path] == ("@delalamo",)


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
  assert "env -u PYTHONPATH python -P -c" in tests_job
  assert "import pytest,sys; sys.path.insert(0, \".\")" in tests_job
  assert "pytest.main([\"tests/paperbot\"])" in tests_job
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
  assert "  merge_group:" in trigger
  assert "Detect paperbot-relevant changes" in workflow
  for relevant_path in (
    ":(glob)tests/paperbot/**",
    ":(glob)**/.gitignore",
    ":(glob)**/.pytest.ini",
    ":(glob)**/.pytest.toml",
    ":(glob)**/conftest.py",
    ":(glob)**/pyproject.toml",
    ":(glob)**/pytest.ini",
    ":(glob)**/pytest.toml",
    ":(glob)**/setup.cfg",
    ":(glob)**/tox.ini",
    ":(glob)*.py",
    ":(glob)**/*.py",
    ":(glob)*.py[cod]",
    ":(glob)**/*.py[cod]",
    ":(glob)*.so",
    ":(glob)**/*.so",
    ":(glob)*.pyd",
    ":(glob)**/*.pyd",
    ":(glob)*.dylib",
    ":(glob)**/*.dylib",
    ".github/CODEOWNERS",
    "sitecustomize.py",
    "usercustomize.py",
  ):
    assert relevant_path in workflow
  assert 'case "$lock_status" in' in workflow
  assert 'case "$relevant_status" in' in workflow
  assert "name: Test paperbot without credentials" in workflow
  assert "if: always()" in workflow


def test_workflow_wires_detection_and_required_gate_outputs_exactly() -> None:
  workflow = yaml.safe_load(
    Path(".github/workflows/paper-model-refresh.yml").read_text(
      encoding="utf-8"
    )
  )
  detect = workflow["jobs"]["detect_paperbot_changes"]
  assert detect["outputs"] == {
    "relevant": "${{ steps.changes.outputs.relevant }}",
    "lock_changed": "${{ steps.changes.outputs.lock_changed }}",
    "bibliography_changed": (
      "${{ steps.changes.outputs.bibliography_changed }}"
    ),
  }
  assert detect["env"] == {
    "BASE_SHA": (
      "${{ github.event.pull_request.base.sha || "
      "github.event.merge_group.base_sha || github.sha }}"
    ),
    "HEAD_SHA": (
      "${{ github.event.pull_request.head.sha || "
      "github.event.merge_group.head_sha || github.sha }}"
    ),
  }
  detect_checkout = next(
    step
    for step in detect["steps"]
    if step["name"] == "Check out candidate history"
  )
  expected_candidate_checkout = {
    "repository": (
      "${{ github.event.pull_request.head.repo.full_name || "
      "github.repository }}"
    ),
    "ref": "${{ github.event.pull_request.head.sha || github.sha }}",
    "path": "candidate",
    "persist-credentials": False,
  }
  for key, expected in expected_candidate_checkout.items():
    assert detect_checkout["with"][key] == expected
  assert detect_checkout["with"]["fetch-depth"] == 0

  selector = next(
    step
    for step in workflow["jobs"]["paperbot_tests"]["steps"]
    if step["name"] == "Select dependency source"
  )
  assert selector["env"]["LOCK_CHANGED"] == (
    "${{ needs.detect_paperbot_changes.outputs.lock_changed }}"
  )
  install = next(
    step
    for step in workflow["jobs"]["paperbot_tests"]["steps"]
    if step["name"] == "Install pinned dependencies"
  )
  assert install["run"] == (
    'python -m pip install --requirement '
    '"${{ steps.dependencies.outputs.lock }}"'
  )
  test_steps = workflow["jobs"]["paperbot_tests"]["steps"]
  assert test_steps.index(install) < next(
    index
    for index, step in enumerate(test_steps)
    if step["name"] == "Verify model with trusted code under selected dependencies"
  )
  verify_model = next(
    step
    for step in test_steps
    if step["name"] == "Verify model with trusted code under selected dependencies"
  )
  assert verify_model["if"] == (
    "steps.dependencies.outputs.bootstrap != 'true' && "
    "needs.detect_paperbot_changes.outputs.bibliography_changed != 'true'"
  )
  deferred_model = next(
    step
    for step in test_steps
    if step["name"] == "Defer model freshness to bibliography refresh"
  )
  assert deferred_model["if"] == (
    "steps.dependencies.outputs.bootstrap != 'true' && "
    "needs.detect_paperbot_changes.outputs.bibliography_changed == 'true'"
  )
  test_checkout = next(
    step
    for step in test_steps
    if step["name"] == "Check out candidate code"
  )
  assert test_checkout["with"] == expected_candidate_checkout

  gate = workflow["jobs"]["paperbot_test_gate"]
  assert gate["if"] == "always()"
  assert gate["needs"] == [
    "detect_paperbot_changes",
    "paperbot_tests",
    "refresh-or-verify",
  ]
  assert gate["steps"][0]["env"] == {
    "DETECT_RESULT": "${{ needs.detect_paperbot_changes.result }}",
    "RELEVANT": "${{ needs.detect_paperbot_changes.outputs.relevant }}",
    "TEST_RESULT": "${{ needs.paperbot_tests.result }}",
    "REFRESH_RESULT": "${{ needs.refresh-or-verify.result }}",
  }

  refresh_checkout = next(
    step
    for step in workflow["jobs"]["refresh-or-verify"]["steps"]
    if step["name"] == "Check out candidate bibliography"
  )
  for key, expected in expected_candidate_checkout.items():
    assert refresh_checkout["with"][key] == expected
  assert refresh_checkout["with"]["fetch-depth"] == 0


@pytest.mark.parametrize(
  ("event_name", "expected_lock_changed"),
  [
    ("workflow_dispatch", "true"),
    ("merge_group", "true"),
  ],
)
def test_non_pr_event_detection_is_fail_closed(
  tmp_path: Path,
  event_name: str,
  expected_lock_changed: str,
) -> None:
  workflow = yaml.safe_load(
    Path(".github/workflows/paper-model-refresh.yml").read_text(
      encoding="utf-8"
    )
  )
  step = next(
    step
    for step in workflow["jobs"]["detect_paperbot_changes"]["steps"]
    if step["name"] == "Detect relevant paths"
  )
  output = tmp_path / "github-output"
  completed = subprocess.run(
    ["bash", "-c", step["run"]],
    check=False,
    capture_output=True,
    text=True,
    env={
      **os.environ,
      "GITHUB_EVENT_NAME": event_name,
      "GITHUB_OUTPUT": str(output),
    },
  )

  assert completed.returncode == 0, completed.stderr
  values = output.read_text(encoding="utf-8")
  assert "relevant=true" in values
  assert f"lock_changed={expected_lock_changed}" in values
  assert "bibliography_changed=false" in values


def test_pr_change_detection_propagates_git_failures(tmp_path: Path) -> None:
  workflow = yaml.safe_load(
    Path(".github/workflows/paper-model-refresh.yml").read_text(
      encoding="utf-8"
    )
  )
  step = next(
    step
    for step in workflow["jobs"]["detect_paperbot_changes"]["steps"]
    if step["name"] == "Detect relevant paths"
  )
  executable_dir = tmp_path / "bin"
  executable_dir.mkdir()
  fake_git = executable_dir / "git"
  fake_git.write_text(
    "#!/usr/bin/env bash\n"
    '[[ "$*" == *" fetch "* ]] && exit 0\n'
    "exit 128\n",
    encoding="utf-8",
  )
  fake_git.chmod(0o755)
  output = tmp_path / "github-output"
  completed = subprocess.run(
    ["bash", "-c", step["run"]],
    check=False,
    capture_output=True,
    text=True,
    env={
      **os.environ,
      "BASE_SHA": "a" * 40,
      "GITHUB_EVENT_NAME": "pull_request",
      "GITHUB_OUTPUT": str(output),
      "GITHUB_REPOSITORY": "delalamo/SKM",
      "HEAD_SHA": "b" * 40,
      "PATH": f"{executable_dir}{os.pathsep}{os.environ['PATH']}",
    },
  )

  assert completed.returncode == 128
  assert "Could not inspect changed Git object modes" in (
    completed.stdout + completed.stderr
  )


def test_pr_change_detection_reports_bibliography_changes(
  tmp_path: Path,
) -> None:
  workflow = yaml.safe_load(
    Path(".github/workflows/paper-model-refresh.yml").read_text(
      encoding="utf-8"
    )
  )
  step = next(
    step
    for step in workflow["jobs"]["detect_paperbot_changes"]["steps"]
    if step["name"] == "Detect relevant paths"
  )
  executable_dir = tmp_path / "bin"
  executable_dir.mkdir()
  fake_git = executable_dir / "git"
  fake_git.write_text(
    "#!/usr/bin/env bash\n"
    '[[ "$*" == *" fetch "* ]] && exit 0\n'
    '[[ "$*" == *" --raw "* ]] && exit 0\n'
    '[[ "$*" == *"-- requirements-paperbot.lock" ]] && exit 0\n'
    '[[ "$*" == *"-- bibliography.bib" ]] && exit 1\n'
    "exit 1\n",
    encoding="utf-8",
  )
  fake_git.chmod(0o755)
  output = tmp_path / "github-output"
  completed = subprocess.run(
    ["bash", "-c", step["run"]],
    check=False,
    capture_output=True,
    text=True,
    env={
      **os.environ,
      "BASE_SHA": "a" * 40,
      "GITHUB_EVENT_NAME": "pull_request",
      "GITHUB_OUTPUT": str(output),
      "GITHUB_REPOSITORY": "delalamo/SKM",
      "HEAD_SHA": "b" * 40,
      "PATH": f"{executable_dir}{os.pathsep}{os.environ['PATH']}",
    },
  )

  assert completed.returncode == 0, completed.stderr
  values = output.read_text(encoding="utf-8")
  assert "lock_changed=false" in values
  assert "bibliography_changed=true" in values
  assert "relevant=true" in values


@pytest.mark.parametrize(
  ("changed_path", "symlink_target"),
  [
    ("numpy", "scripts/paperbot"),
    ("scripts.pyc", None),
    ("scripts.cpython-312-x86_64-linux-gnu.so", None),
  ],
)
def test_pr_change_detection_treats_import_shadows_as_relevant(
  tmp_path: Path,
  changed_path: str,
  symlink_target: str | None,
) -> None:
  candidate = tmp_path / "candidate"
  candidate.mkdir()
  _git(candidate, "init")
  _git(candidate, "config", "user.name", "Paperbot Test")
  _git(candidate, "config", "user.email", "paperbot@example.invalid")
  (candidate / "README.md").write_text("base\n", encoding="utf-8")
  _git(candidate, "add", ".")
  _git(candidate, "commit", "-m", "base")
  base = _git(candidate, "rev-parse", "HEAD")
  changed = candidate / changed_path
  if symlink_target is None:
    changed.write_bytes(b"importable shadow fixture\n")
  else:
    changed.symlink_to(symlink_target)
  _git(candidate, "add", "-f", changed_path)
  _git(candidate, "commit", "-m", "importable package symlink")
  head = _git(candidate, "rev-parse", "HEAD")

  workflow = yaml.safe_load(
    Path(".github/workflows/paper-model-refresh.yml").read_text(
      encoding="utf-8"
    )
  )
  step = next(
    step
    for step in workflow["jobs"]["detect_paperbot_changes"]["steps"]
    if step["name"] == "Detect relevant paths"
  )
  executable_dir = tmp_path / "bin"
  executable_dir.mkdir()
  fake_git = executable_dir / "git"
  real_git = shutil.which("git")
  assert real_git is not None
  fake_git.write_text(
    "#!/usr/bin/env bash\n"
    'if [[ "$1" == "-C" && "$3" == "fetch" ]]; then exit 0; fi\n'
    f'exec "{real_git}" "$@"\n',
    encoding="utf-8",
  )
  fake_git.chmod(0o755)
  output = tmp_path / "github-output"
  completed = subprocess.run(
    ["bash", "-c", step["run"]],
    cwd=tmp_path,
    check=False,
    capture_output=True,
    text=True,
    env={
      **os.environ,
      "BASE_SHA": base,
      "GITHUB_EVENT_NAME": "pull_request",
      "GITHUB_OUTPUT": str(output),
      "GITHUB_REPOSITORY": "delalamo/SKM",
      "HEAD_SHA": head,
      "PATH": f"{executable_dir}{os.pathsep}{os.environ['PATH']}",
    },
  )

  assert completed.returncode == 0, completed.stderr
  values = output.read_text(encoding="utf-8")
  assert "lock_changed=false" in values
  assert "bibliography_changed=false" in values
  assert "relevant=true" in values


def test_symlink_detection_cannot_mask_a_later_git_failure(
  tmp_path: Path,
) -> None:
  workflow = yaml.safe_load(
    Path(".github/workflows/paper-model-refresh.yml").read_text(
      encoding="utf-8"
    )
  )
  step = next(
    step
    for step in workflow["jobs"]["detect_paperbot_changes"]["steps"]
    if step["name"] == "Detect relevant paths"
  )
  executable_dir = tmp_path / "bin"
  executable_dir.mkdir()
  fake_git = executable_dir / "git"
  fake_git.write_text(
    "#!/usr/bin/env bash\n"
    '[[ "$*" == *" fetch "* ]] && exit 0\n'
    'if [[ "$*" == *" --raw "* ]]; then\n'
    "  printf ':000000 120000 0000000 1111111 A\\tnumpy\\n'\n"
    "  exit 0\n"
    "fi\n"
    '[[ "$*" == *"bibliography.bib"* ]] && exit 128\n'
    '[[ "$*" == *"requirements-paperbot.lock"* ]] && exit 0\n'
    "exit 128\n",
    encoding="utf-8",
  )
  fake_git.chmod(0o755)
  completed = subprocess.run(
    ["bash", "-c", step["run"]],
    check=False,
    capture_output=True,
    text=True,
    env={
      **os.environ,
      "BASE_SHA": "a" * 40,
      "GITHUB_EVENT_NAME": "pull_request",
      "GITHUB_OUTPUT": str(tmp_path / "github-output"),
      "GITHUB_REPOSITORY": "delalamo/SKM",
      "HEAD_SHA": "b" * 40,
      "PATH": f"{executable_dir}{os.pathsep}{os.environ['PATH']}",
    },
  )

  assert completed.returncode == 128
  assert "Could not determine whether the bibliography changed" in (
    completed.stdout + completed.stderr
  )


def test_changed_dependency_lock_is_tested_in_the_candidate_environment(
  tmp_path: Path,
) -> None:
  workspace = tmp_path / "workspace"
  trusted = workspace / "trusted"
  candidate = workspace / "candidate"
  (trusted / "scripts" / "paperbot").mkdir(parents=True)
  candidate.mkdir(parents=True)
  (trusted / "requirements-paperbot.lock").write_text(
    "trusted==1\n", encoding="utf-8"
  )
  (trusted / "scripts" / "paperbot" / "pr_safety.py").write_text(
    "# trusted\n", encoding="utf-8"
  )
  (candidate / "requirements-paperbot.lock").write_text(
    "candidate==2\n", encoding="utf-8"
  )
  workflow = yaml.safe_load(
    Path(".github/workflows/paper-model-refresh.yml").read_text(
      encoding="utf-8"
    )
  )
  step = next(
    step
    for step in workflow["jobs"]["paperbot_tests"]["steps"]
    if step["name"] == "Select dependency source"
  )

  for changed, expected_lock in (
    ("false", "trusted/requirements-paperbot.lock"),
    ("true", "candidate/requirements-paperbot.lock"),
  ):
    output = tmp_path / f"github-output-{changed}"
    completed = subprocess.run(
      ["bash", "-c", step["run"]],
      check=False,
      capture_output=True,
      text=True,
      env={
        **os.environ,
        "GITHUB_OUTPUT": str(output),
        "GITHUB_WORKSPACE": str(workspace),
        "LOCK_CHANGED": changed,
      },
    )
    assert completed.returncode == 0, completed.stderr
    values = output.read_text(encoding="utf-8")
    assert f"lock={expected_lock}" in values
    assert "bootstrap=false" in values


def test_candidate_dependencies_never_enter_the_credentialed_refresh_job() -> None:
  workflow = Path(".github/workflows/paper-model-refresh.yml").read_text(
    encoding="utf-8"
  )
  tests_job, refresh_job = workflow.split("  refresh-or-verify:", maxsplit=1)

  assert (
    "Verify model with trusted code under selected dependencies"
    in tests_job
  )
  assert 'working-directory: trusted' in tests_job
  assert '--repo-root "$GITHUB_WORKSPACE/candidate"' in tests_job
  assert "candidate/requirements-paperbot.lock" in tests_job

  assert "--requirement trusted/requirements-paperbot.lock" in refresh_job
  assert "--requirement candidate/requirements-paperbot.lock" not in refresh_job
  assert "steps.refresh_dependencies" not in refresh_job


def test_safe_path_prevents_candidate_pytest_module_shadowing(
  tmp_path: Path,
) -> None:
  candidate = tmp_path / "candidate"
  tests = candidate / "tests" / "paperbot"
  tests.mkdir(parents=True)
  scripts = candidate / "scripts"
  scripts.mkdir()
  (scripts / "__init__.py").write_text("", encoding="utf-8")
  (scripts / "sentinel.py").write_text("VALUE = 42\n", encoding="utf-8")
  (candidate / "pytest.py").write_text(
    "raise SystemExit(0)\n", encoding="utf-8"
  )
  (tests / "test_must_run.py").write_text(
    "from scripts.sentinel import VALUE\n\n"
    "def test_must_run():\n"
    "  assert VALUE == 42\n"
    "  assert False, 'the real pytest runner collected this test'\n",
    encoding="utf-8",
  )

  unsafe = subprocess.run(
    [os.sys.executable, "-m", "pytest", "tests/paperbot"],
    cwd=candidate,
    check=False,
    capture_output=True,
    text=True,
    env={**os.environ, "PYTHONPATH": str(candidate)},
  )
  safe = subprocess.run(
    [
      "env",
      "-u",
      "PYTHONPATH",
      os.sys.executable,
      "-P",
      "-c",
      (
        'import pytest,sys; sys.path.insert(0, "."); '
        'raise SystemExit(pytest.main(["tests/paperbot"]))'
      ),
    ],
    cwd=candidate,
    check=False,
    capture_output=True,
    text=True,
    env={**os.environ, "PYTHONPATH": str(candidate)},
  )

  assert unsafe.returncode == 0
  assert safe.returncode == 1
  assert "the real pytest runner collected this test" in (
    safe.stdout + safe.stderr
  )


def test_full_base_history_is_used_for_triple_dot_diffs() -> None:
  workflow = yaml.safe_load(
    Path(".github/workflows/paper-model-refresh.yml").read_text(
      encoding="utf-8"
    )
  )
  detect_script = next(
    step["run"]
    for step in workflow["jobs"]["detect_paperbot_changes"]["steps"]
    if step["name"] == "Detect relevant paths"
  )
  classify_script = next(
    step["run"]
    for step in workflow["jobs"]["refresh-or-verify"]["steps"]
    if step["name"] == "Classify the pull request"
  )
  for script in (detect_script, classify_script):
    assert "fetch --no-tags" in script
    assert "--depth" not in script
  assert '"$BASE_SHA...$HEAD_SHA"' in detect_script


def test_full_base_fetch_supports_a_diverged_pull_request(
  tmp_path: Path,
) -> None:
  upstream = tmp_path / "upstream.git"
  _git(tmp_path, "init", "--bare", str(upstream))

  maintainer = tmp_path / "maintainer"
  maintainer.mkdir()
  _git(maintainer, "init")
  _git(maintainer, "config", "user.name", "Paperbot Test")
  _git(maintainer, "config", "user.email", "paperbot@example.invalid")
  (maintainer / "README.md").write_text("base\n", encoding="utf-8")
  _git(maintainer, "add", ".")
  _git(maintainer, "commit", "-m", "base")
  _git(maintainer, "branch", "-M", "main")
  _git(maintainer, "remote", "add", "origin", str(upstream))
  _git(maintainer, "push", "-u", "origin", "main")

  candidate = tmp_path / "candidate"
  _git(
    tmp_path,
    "clone",
    "--branch",
    "main",
    str(upstream),
    str(candidate),
  )
  _git(candidate, "config", "user.name", "Paperbot Test")
  _git(candidate, "config", "user.email", "paperbot@example.invalid")
  _git(candidate, "checkout", "-b", "feature")
  (candidate / "scripts" / "paperbot").mkdir(parents=True)
  (candidate / "scripts" / "paperbot" / "model.py").write_text(
    "feature = True\n", encoding="utf-8"
  )
  _git(candidate, "add", ".")
  _git(candidate, "commit", "-m", "feature")
  head = _git(candidate, "rev-parse", "HEAD")

  (maintainer / "README.md").write_text("base advanced\n", encoding="utf-8")
  _git(maintainer, "commit", "-am", "advance main")
  base = _git(maintainer, "rev-parse", "HEAD")
  _git(maintainer, "push", "origin", "main")

  _git(candidate, "fetch", "--no-tags", str(upstream), base)
  completed = subprocess.run(
    [
      "git",
      "-C",
      str(candidate),
      "diff",
      "--quiet",
      "--no-renames",
      f"{base}...{head}",
      "--",
      "scripts/paperbot/model.py",
    ],
    check=False,
    capture_output=True,
    text=True,
  )

  assert completed.returncode == 1, completed.stderr


def test_dependency_source_rejects_invalid_change_detection(
  tmp_path: Path,
) -> None:
  workflow = yaml.safe_load(
    Path(".github/workflows/paper-model-refresh.yml").read_text(
      encoding="utf-8"
    )
  )
  step = next(
    step
    for step in workflow["jobs"]["paperbot_tests"]["steps"]
    if step["name"] == "Select dependency source"
  )
  completed = subprocess.run(
    ["bash", "-c", step["run"]],
    check=False,
    capture_output=True,
    text=True,
    env={
      **os.environ,
      "GITHUB_OUTPUT": str(tmp_path / "github-output"),
      "GITHUB_WORKSPACE": str(tmp_path),
      "LOCK_CHANGED": "",
    },
  )
  assert completed.returncode == 1


def test_required_paperbot_gate_cannot_pass_after_required_job_failure() -> None:
  workflow = Path(".github/workflows/paper-model-refresh.yml").read_text(
    encoding="utf-8"
  )
  gate = workflow.split("  paperbot_test_gate:", maxsplit=1)[1].split(
    "  refresh-or-verify:", maxsplit=1
  )[0]

  assert (
    "needs: [detect_paperbot_changes, paperbot_tests, refresh-or-verify]"
    in gate
  )
  assert "DETECT_RESULT" in gate
  assert '"$DETECT_RESULT" != "success"' in gate
  assert '"$RELEVANT" == "true" && "$TEST_RESULT" != "success"' in gate
  assert '"$RELEVANT" == "true" && "$REFRESH_RESULT" != "success"' in gate
  assert '"$RELEVANT" != "true" && "$RELEVANT" != "false"' in gate


@pytest.mark.parametrize(
  ("environment", "expected"),
  [
    (
      {
        "DETECT_RESULT": "success",
        "RELEVANT": "false",
        "TEST_RESULT": "skipped",
        "REFRESH_RESULT": "skipped",
      },
      0,
    ),
    (
      {
        "DETECT_RESULT": "success",
        "RELEVANT": "true",
        "TEST_RESULT": "success",
        "REFRESH_RESULT": "success",
      },
      0,
    ),
    (
      {
        "DETECT_RESULT": "success",
        "RELEVANT": "true",
        "TEST_RESULT": "failure",
        "REFRESH_RESULT": "success",
      },
      1,
    ),
    (
      {
        "DETECT_RESULT": "success",
        "RELEVANT": "true",
        "TEST_RESULT": "success",
        "REFRESH_RESULT": "failure",
      },
      1,
    ),
    (
      {
        "DETECT_RESULT": "failure",
        "RELEVANT": "",
        "TEST_RESULT": "skipped",
        "REFRESH_RESULT": "skipped",
      },
      1,
    ),
  ],
)
def test_required_gate_shell_logic(
  environment: dict[str, str],
  expected: int,
) -> None:
  workflow = yaml.safe_load(
    Path(".github/workflows/paper-model-refresh.yml").read_text(
      encoding="utf-8"
    )
  )
  script = workflow["jobs"]["paperbot_test_gate"]["steps"][0]["run"]

  completed = subprocess.run(
    ["bash", "-c", script],
    check=False,
    capture_output=True,
    text=True,
    env={**os.environ, **environment},
  )

  assert completed.returncode == expected


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
  assert (
    commit_and_after.index("git -C candidate diff --cached --quiet")
    < commit_and_after.index('[[ -z "$MODEL_UPDATE_TOKEN" ]]')
  )


def test_noop_refresh_does_not_require_model_update_token(
  tmp_path: Path,
) -> None:
  candidate = tmp_path / "candidate"
  candidate.mkdir()
  _git(candidate, "init")
  _git(candidate, "config", "user.name", "Paperbot Test")
  _git(candidate, "config", "user.email", "paperbot@example.invalid")
  for relative in GENERATED_PATHS:
    path = candidate / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(b"fixture\n")
  _git(candidate, "add", ".")
  _git(candidate, "commit", "-m", "current artifacts")

  workflow = yaml.safe_load(
    Path(".github/workflows/paper-model-refresh.yml").read_text(
      encoding="utf-8"
    )
  )
  step = next(
    step
    for step in workflow["jobs"]["refresh-or-verify"]["steps"]
    if step["name"] == "Commit refreshed artifacts to trusted PR branch"
  )
  completed = subprocess.run(
    ["bash", "-c", step["run"]],
    cwd=tmp_path,
    check=False,
    capture_output=True,
    text=True,
    env={
      **os.environ,
      "HEAD_REF": "feature",
      "HEAD_REPOSITORY": "delalamo/SKM",
      "HEAD_SHA": _git(candidate, "rev-parse", "HEAD"),
      "MODEL_UPDATE_TOKEN": "",
    },
  )

  assert completed.returncode == 0, completed.stderr
  assert "already current" in completed.stdout


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
