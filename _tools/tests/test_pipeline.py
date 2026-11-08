"""The pipeline is idempotent and regenerates every generated part of the vault."""

from __future__ import annotations

import re

import rules
import run_pipeline
from conftest import FIXTURES, katex_dir


def run(fx):
  return run_pipeline.run(fx.vault, fx.bib, fx.data, fx.builds, quiet=True)


def test_committed_fixture_is_pipeline_output(fixture_vault):
  assert run(fixture_vault) == []


def test_second_run_changes_nothing(fixture_vault):
  run(fixture_vault)
  assert run(fixture_vault) == []
  assert rules.run(fixture_vault.load(), katex=katex_dir()) == []


def test_generated_parts_are_restored(fixture_vault):
  fx = fixture_vault
  originals = {rel: fx.read(rel) for rel in (
    "Papers/alpha2020.md", "Papers/gamma2021.md", "Topics/Widget loops.md",
    "Claims/Widget loops are rigid.md", "Indexes/Claims index.md",
  )}
  # Strip reference callouts, hover definitions, topic lists, excerpts and kb lists.
  gamma = fx.read("Papers/gamma2021.md")
  gamma = re.sub(r"> \[!cite[^\n]*\n(> [^\n]*\n)*\n", "", gamma)
  gamma = re.sub(r'<abbr title="[^"]*">(.*?)</abbr>', r"\1", gamma)
  fx.write("Papers/gamma2021.md", gamma)
  fx.write("Topics/Widget loops.md", re.sub(r"(?s)(%% begin generated: claims %%\n).*?(%% end generated %%)", r"\1\2", originals["Topics/Widget loops.md"]))
  claim = originals["Claims/Widget loops are rigid.md"]
  claim = claim.replace('kb_supporting: ["[[alpha2020]]"]', "kb_supporting: []")
  claim = re.sub(r"(?s)%% begin generated: excerpts alpha2020 %%\n.*?%% end generated %%\n", "", claim)
  fx.write("Claims/Widget loops are rigid.md", claim)
  (fx.vault / "Indexes" / "Claims index.md").unlink()
  (fx.vault / "Papers" / "alpha2020.md").unlink()
  run(fx)
  for rel, text in originals.items():
    assert fx.read(rel) == text, rel


def test_real_vault_tools_run_without_knowledge_base_notes(tmp_path):
  """Before migration the real vault has only legacy notes: nothing is generated."""
  vault = tmp_path / "vault"
  (vault / "notes").mkdir(parents=True)
  (vault / "notes" / "A legacy claim.md").write_text("---\ntags: []\n---\nText [@x].\n")
  data = tmp_path / "data"
  data.mkdir()
  assert run_pipeline.run(vault, FIXTURES / "bibliography.bib", data, tmp_path / "builds", quiet=True) == []
