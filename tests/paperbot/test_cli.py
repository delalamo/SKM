from __future__ import annotations

import json
import sys
from pathlib import Path
from types import ModuleType
from typing import Any
from unittest.mock import Mock

import pytest

from scripts.paperbot.cli import build_parser, main
from scripts.paperbot.model import LoadedModel


def test_sync_issue_negatives_command_is_registered() -> None:
  args = build_parser().parse_args(["sync-issue-negatives"])

  assert args.command == "sync-issue-negatives"


def test_sync_issue_negatives_passes_the_builtin_token(
  monkeypatch: pytest.MonkeyPatch,
  capsys: pytest.CaptureFixture[str],
) -> None:
  calls: list[tuple[Any, str]] = []
  collector = ModuleType("scripts.paperbot.issue_negatives")

  def sync_issue_negatives(config: Any, *, github_token: str) -> dict[str, Any]:
    calls.append((config, github_token))
    return {"active_count": 3, "ok": True}

  collector.sync_issue_negatives = sync_issue_negatives  # type: ignore[attr-defined]
  monkeypatch.setitem(sys.modules, collector.__name__, collector)
  monkeypatch.setenv("GITHUB_TOKEN", "read-only-token")

  assert main(["--repo-root", str(Path.cwd()), "sync-issue-negatives"]) == 0
  assert len(calls) == 1
  assert calls[0][0].repository == "delalamo/SKM"
  assert calls[0][1] == "read-only-token"
  assert json.loads(capsys.readouterr().out) == {"active_count": 3, "ok": True}


def test_sync_issue_negatives_requires_a_token(
  monkeypatch: pytest.MonkeyPatch,
) -> None:
  monkeypatch.delenv("GITHUB_TOKEN", raising=False)

  with pytest.raises(SystemExit) as caught:
    main(["--repo-root", str(Path.cwd()), "sync-issue-negatives"])

  assert caught.value.code == 2


def test_repo_root_requires_its_own_config(
  tmp_path: Path,
  capsys: pytest.CaptureFixture[str],
) -> None:
  assert main(["--repo-root", str(tmp_path), "check-model"]) == 1
  assert "regular, non-symlink file" in capsys.readouterr().err


def test_project_sync_uses_the_saved_model_without_requiring_fresh_training(
  monkeypatch: pytest.MonkeyPatch,
) -> None:
  saved_model = LoadedModel(None, 0, "trained-model")
  monkeypatch.setattr("scripts.paperbot.cli.load_model", lambda _: saved_model)
  monkeypatch.setattr(
    "scripts.paperbot.cli.check_model",
    Mock(side_effect=AssertionError("training corpus freshness is not required")),
  )
  sync = Mock(return_value=2)
  monkeypatch.setattr("scripts.paperbot.cli.sync_project_queue", sync)
  monkeypatch.setenv("PROJECTS_TOKEN", "project-token")

  assert main(["daily", "--sync-project", "queue.json"]) == 0
  assert sync.call_args.kwargs["expected_model_hash"] == "trained-model"
  assert sync.call_args.kwargs["projects_token"] == "project-token"
