from __future__ import annotations

import os
from pathlib import Path


REPO_ROOT = Path(
  os.getenv("PAPERBOT_POLICY_ROOT", Path(__file__).resolve().parents[2])
).resolve()
SCOPED_FILES = [
  *sorted((REPO_ROOT / "scripts" / "paperbot").glob("*.py")),
  REPO_ROOT / "requirements-paperbot.lock",
  REPO_ROOT / ".github" / "workflows" / "paper-discovery.yml",
  REPO_ROOT / ".github" / "workflows" / "paper-model-refresh.yml",
]
FORBIDDEN = (
  "open" + "ai",
  "chat" + "gpt",
  "open" + "ai_api_key",
)


def test_paperbot_has_no_remote_summarization_dependency() -> None:
  violations: list[str] = []
  for path in SCOPED_FILES:
    text = path.read_text(encoding="utf-8").casefold()
    for term in FORBIDDEN:
      if term in text:
        violations.append(f"{path.relative_to(REPO_ROOT)} contains {term}")
  assert not violations, "\n".join(violations)
