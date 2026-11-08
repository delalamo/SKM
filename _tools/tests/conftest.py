from __future__ import annotations

import shutil
import sys
from pathlib import Path

import pytest

TOOLS = Path(__file__).resolve().parents[1]
REPO = TOOLS.parent
FIXTURES = Path(__file__).resolve().parent / "fixtures"
sys.path.insert(0, str(TOOLS))


class FixtureVault:
  """A scratch copy of the fixture vault and its data directory."""

  def __init__(self, root: Path) -> None:
    self.root = root
    self.vault = root / "vault"
    self.data = root / "data"
    self.builds = root / "builds"
    self.bib = FIXTURES / "bibliography.bib"
    shutil.copytree(FIXTURES / "vault_ok", self.vault)
    shutil.copytree(FIXTURES / "data", self.data)
    shutil.copytree(FIXTURES / "builds", self.builds)

  def path(self, rel: str) -> Path:
    return self.vault / rel

  def read(self, rel: str) -> str:
    return self.path(rel).read_text(encoding="utf-8")

  def write(self, rel: str, text: str) -> None:
    self.path(rel).parent.mkdir(parents=True, exist_ok=True)
    self.path(rel).write_text(text, encoding="utf-8")

  def replace(self, rel: str, old: str, new: str) -> None:
    text = self.read(rel)
    assert text.count(old) == 1, f"{old!r} occurs {text.count(old)} times in {rel}"
    self.write(rel, text.replace(old, new))

  def load(self):
    from vaultlib.vault import Vault

    return Vault(self.vault, self.bib, self.data)


@pytest.fixture
def fixture_vault(tmp_path: Path) -> FixtureVault:
  return FixtureVault(tmp_path)


def katex_dir() -> str | None:
  candidate = REPO / "node_modules" / "katex"
  return str(candidate) if candidate.exists() and shutil.which("node") else None
