from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.paperbot.backfill import backfill_bibliography
from scripts.paperbot.bibliography import load_bibliography
from scripts.paperbot.config import PaperbotConfig
from scripts.paperbot.enrichment import ResolvedAbstract


class _Resolver:
  def resolve(self, _fields: dict[str, str]) -> ResolvedAbstract:
    return ResolvedAbstract(
      "<p>A complete fetched abstract for this work.</p>",
      "fixture",
      "https://example.test/metadata",
      "CC-BY-4.0",
    )


class _FailingResolver:
  def resolve(self, _fields: dict[str, str]) -> ResolvedAbstract:
    raise AssertionError("a title-only exception must not trigger a provider lookup")


class BackfillTests(unittest.TestCase):
  def test_backfill_propagates_one_abstract_to_duplicate_aliases(self) -> None:
    with tempfile.TemporaryDirectory() as directory:
      root = Path(directory)
      bibliography = root / "bibliography.bib"
      bibliography.write_text(
        """@article{one2025,
  title = {A paper},
  author = {One, Ada},
  year = {2025},
  doi = {10.1234/example},
}

@misc{one2025preprint,
  title = {A paper},
  author = {One, Ada},
  year = {2025},
  doi = {10.1234/example},
}
""",
        encoding="utf-8",
      )
      artifacts = root / "artifacts"
      exceptions = artifacts / "exceptions.json"
      exceptions.parent.mkdir()
      exceptions.write_text("{}\n", encoding="utf-8")
      config = PaperbotConfig(
        bibliography_path=bibliography,
        artifact_dir=artifacts,
        abstract_exceptions_path=exceptions,
      )

      result = backfill_bibliography(config, resolver=_Resolver())

      self.assertEqual(result.canonical_works, 1)
      self.assertEqual(result.abstracts_added, 1)
      self.assertEqual(result.aliases_filled, 2)
      self.assertFalse(result.unresolved)
      self.assertTrue(all(entry.abstract for entry in load_bibliography(bibliography)))
      self.assertTrue((artifacts / "abstract_provenance.jsonl").exists())

  def test_dry_run_does_not_write(self) -> None:
    with tempfile.TemporaryDirectory() as directory:
      root = Path(directory)
      bibliography = root / "bibliography.bib"
      original = "@book{old1900, title={An old book}, author={Old, Ada}, year={1900}}\n"
      bibliography.write_text(original, encoding="utf-8")
      artifacts = root / "artifacts"
      artifacts.mkdir()
      exceptions = artifacts / "exceptions.json"
      exceptions.write_text('{"old1900":"No abstract was published."}\n', encoding="utf-8")
      config = PaperbotConfig(
        bibliography_path=bibliography,
        artifact_dir=artifacts,
        abstract_exceptions_path=exceptions,
      )

      result = backfill_bibliography(config, resolver=_FailingResolver(), dry_run=True)

      self.assertEqual(bibliography.read_text(encoding="utf-8"), original)
      self.assertFalse((artifacts / "abstract_provenance.jsonl").exists())
      self.assertFalse(result.unresolved)

  def test_existing_bibliography_license_is_recorded(self) -> None:
    with tempfile.TemporaryDirectory() as directory:
      root = Path(directory)
      bibliography = root / "bibliography.bib"
      bibliography.write_text(
        """@article{licensed2024,
  title = {A licensed paper},
  author = {Licensed, Ada},
  year = {2024},
  abstract = {An existing author abstract.},
  copyright = {https://creativecommons.org/licenses/by/4.0/},
}
""",
        encoding="utf-8",
      )
      artifacts = root / "artifacts"
      artifacts.mkdir()
      exceptions = artifacts / "exceptions.json"
      exceptions.write_text("{}\n", encoding="utf-8")
      config = PaperbotConfig(
        bibliography_path=bibliography,
        artifact_dir=artifacts,
        abstract_exceptions_path=exceptions,
      )

      backfill_bibliography(config, resolver=_FailingResolver())

      provenance = json.loads((artifacts / "abstract_provenance.jsonl").read_text())
      self.assertEqual(
        provenance["license"],
        "https://creativecommons.org/licenses/by/4.0/",
      )


if __name__ == "__main__":
  unittest.main()
