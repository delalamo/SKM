from __future__ import annotations

import hashlib
import json
import re
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


class _IdentityResolver:
  def __init__(self, text: str = "") -> None:
    self.calls = 0
    self.text = text

  def resolve(self, fields: dict[str, str]) -> ResolvedAbstract:
    self.calls += 1
    return ResolvedAbstract(
      self.text or f"Abstract resolved for {fields.get('doi', 'unknown')}.",
      "fixture",
      "",
      "unknown",
    )


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

  def test_backfill_rejects_duplicate_citation_keys_before_lookup(self) -> None:
    with tempfile.TemporaryDirectory() as directory:
      root = Path(directory)
      bibliography = root / "bibliography.bib"
      original = """@article{same,
  title = {First paper},
  author = {First, Ada},
  year = {2024},
  doi = {10.1000/first},
}

@article{SAME,
  title = {Second paper},
  author = {Second, Ada},
  year = {2024},
  doi = {10.1000/second},
}
"""
      bibliography.write_text(original, encoding="utf-8")
      artifacts = root / "artifacts"
      artifacts.mkdir()
      exceptions = artifacts / "exceptions.json"
      exceptions.write_text("{}\n", encoding="utf-8")
      resolver = _IdentityResolver()
      config = PaperbotConfig(
        bibliography_path=bibliography,
        artifact_dir=artifacts,
        abstract_exceptions_path=exceptions,
      )

      with self.assertRaisesRegex(ValueError, "Duplicate BibTeX citation keys"):
        backfill_bibliography(config, resolver=resolver)

      self.assertEqual(resolver.calls, 0)
      self.assertEqual(bibliography.read_text(encoding="utf-8"), original)

  def test_backfill_preserves_comments_directives_and_value_expressions(self) -> None:
    with tempfile.TemporaryDirectory() as directory:
      root = Path(directory)
      bibliography = root / "bibliography.bib"
      original = """% Keep this comment, including a fake @article{ignored} marker.
@string{venueName = "Journal of Examples"}
@preamble("Bibliography generated for " # venueName)

@article(macro2024,
  title = "A molecular " # "paper",
  author = {Macro, Ada},
  year = 2024,
  journal = venueName,
  note = {An unmatched parenthesis ) remains part of this field},
  doi = {10.1000/macro},
)

@article{existing2023,
  title = {An existing paper},
  author = {Existing, Ada},
  year = {2023},
  abstract = {Already complete.},
}
"""
      bibliography.write_text(original, encoding="utf-8")
      artifacts = root / "artifacts"
      artifacts.mkdir()
      exceptions = artifacts / "exceptions.json"
      exceptions.write_text("{}\n", encoding="utf-8")
      config = PaperbotConfig(
        bibliography_path=bibliography,
        artifact_dir=artifacts,
        abstract_exceptions_path=exceptions,
      )

      fetched = "A 50% result with unmatched {{ left and one } right brace."
      result = backfill_bibliography(
        config,
        resolver=_IdentityResolver(fetched),
      )
      updated = bibliography.read_text(encoding="utf-8")

      self.assertTrue(result.changed)
      self.assertIn(
        "% Keep this comment, including a fake @article{ignored} marker.",
        updated,
      )
      self.assertIn('@string{venueName = "Journal of Examples"}', updated)
      self.assertIn(
        '@preamble("Bibliography generated for " # venueName)',
        updated,
      )
      self.assertIn('title = "A molecular " # "paper",', updated)
      self.assertIn("journal = venueName,", updated)
      self.assertIn(
        "note = {An unmatched parenthesis ) remains part of this field},",
        updated,
      )
      self.assertIn(
        r"abstract = {A 50\% result with unmatched \{\{ left and one \} right brace.},",
        updated,
      )
      parsed = load_bibliography(bibliography)
      self.assertEqual(len(parsed), 2)
      entry = parsed[0]
      self.assertEqual(entry.fields["title"], "A molecular paper")
      self.assertEqual(entry.fields["doi"], "10.1000/macro")
      self.assertEqual(entry.abstract, fetched)
      self.assertEqual(parsed[1].abstract, "Already complete.")

  def test_backfill_places_separator_before_a_trailing_comment(self) -> None:
    with tempfile.TemporaryDirectory() as directory:
      root = Path(directory)
      bibliography = root / "bibliography.bib"
      bibliography.write_text(
        "@article{commented,\n"
        "  title = {A commented paper},\n"
        "  author = {Comment, Ada},\n"
        "  year = {2024},\n"
        "  doi = {10.1000/commented} % preserve this comment\n"
        "}\n",
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

      backfill_bibliography(
        config,
        resolver=_IdentityResolver("A fetched abstract."),
      )
      updated = bibliography.read_text(encoding="utf-8")

      self.assertIn(
        "doi = {10.1000/commented}, % preserve this comment",
        updated,
      )
      [entry] = load_bibliography(bibliography)
      self.assertEqual(entry.abstract, "A fetched abstract.")

  def test_backfill_protects_backslashes_immediately_before_braces(self) -> None:
    with tempfile.TemporaryDirectory() as directory:
      root = Path(directory)
      bibliography = root / "bibliography.bib"
      bibliography.write_text(
        "@article{slashes,\n"
        "  title = {A slash paper},\n"
        "  author = {Slash, Ada},\n"
        "  year = {2024},\n"
        "  doi = {10.1000/slashes},\n"
        "}\n",
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
      fetched = r"Literal \\{left, \\} right, and \\% percent sequences."

      backfill_bibliography(
        config,
        resolver=_IdentityResolver(fetched),
      )
      updated = bibliography.read_text(encoding="utf-8")

      self.assertIn(
        r"\textbackslash{}\textbackslash{}\{left",
        updated,
      )
      [entry] = load_bibliography(bibliography)
      self.assertEqual(entry.abstract, fetched)

  def test_backfill_replaces_empty_abstract_field_without_duplication(
    self,
  ) -> None:
    for empty_value in ("{}", '""', "{}, % preserve empty-field comment"):
      with self.subTest(empty_value=empty_value):
        with tempfile.TemporaryDirectory() as directory:
          root = Path(directory)
          bibliography = root / "bibliography.bib"
          bibliography.write_text(
            "@article{empty,\n"
            "  title = {An empty abstract paper},\n"
            "  author = {Empty, Ada},\n"
            "  year = {2024},\n"
              f"  abstract = {empty_value}"
              f"{'' if '%' in empty_value else ','}\n"
            "  doi = {10.1000/empty},\n"
            "}\n",
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

          backfill_bibliography(
            config,
            resolver=_IdentityResolver("A replacement abstract."),
          )
          updated = bibliography.read_text(encoding="utf-8")

          self.assertEqual(len(re.findall(r"(?i)\babstract\s*=", updated)), 1)
          if "%" in empty_value:
            self.assertIn("% preserve empty-field comment", updated)
          [entry] = load_bibliography(bibliography)
          self.assertEqual(entry.abstract, "A replacement abstract.")

  def test_backfill_ignores_braces_inside_field_comments(self) -> None:
    with tempfile.TemporaryDirectory() as directory:
      root = Path(directory)
      bibliography = root / "bibliography.bib"
      bibliography.write_text(
        "@article{comment-brace,\n"
        "  title = {A title % } is inside the comment\n"
        "    that continues here},\n"
        "  author = {Comment, Ada},\n"
        "  year = {2024},\n"
        "  abstract = {},\n"
        "  doi = {10.1000/comment-brace},\n"
        "}\n",
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

      result = backfill_bibliography(
        config,
        resolver=_IdentityResolver("A fetched abstract."),
      )
      updated = bibliography.read_text(encoding="utf-8")

      self.assertTrue(result.changed)
      self.assertEqual(result.unresolved, ())
      self.assertEqual(len(re.findall(r"(?i)\babstract\s*=", updated)), 1)
      self.assertIn("% } is inside the comment", updated)
      [entry] = load_bibliography(bibliography)
      self.assertEqual(entry.abstract, "A fetched abstract.")

  def test_backfill_rejects_markup_that_normalizes_to_an_empty_abstract(
    self,
  ) -> None:
    with tempfile.TemporaryDirectory() as directory:
      root = Path(directory)
      bibliography = root / "bibliography.bib"
      bibliography.write_text(
        "@article{empty-markup,\n"
        "  title = {An unresolved paper},\n"
        "  author = {Empty, Ada},\n"
        "  year = {2024},\n"
        "  doi = {10.1000/empty-markup},\n"
        "}\n",
        encoding="utf-8",
      )
      original = bibliography.read_text(encoding="utf-8")
      artifacts = root / "artifacts"
      artifacts.mkdir()
      exceptions = artifacts / "exceptions.json"
      exceptions.write_text("{}\n", encoding="utf-8")
      config = PaperbotConfig(
        bibliography_path=bibliography,
        artifact_dir=artifacts,
        abstract_exceptions_path=exceptions,
      )

      result = backfill_bibliography(
        config,
        resolver=_IdentityResolver("<p></p>"),
      )

      self.assertFalse(result.changed)
      self.assertEqual(result.abstracts_added, 0)
      self.assertEqual(result.aliases_filled, 0)
      self.assertEqual(result.unresolved, ("empty-markup",))
      self.assertEqual(bibliography.read_text(encoding="utf-8"), original)

  def test_backfill_preserves_provenance_when_canonical_id_changes(
    self,
  ) -> None:
    with tempfile.TemporaryDirectory() as directory:
      root = Path(directory)
      bibliography = root / "bibliography.bib"
      abstract = "The same abstract."
      bibliography.write_text(
        "@misc{preprint,\n"
        "  title = {A shared work},\n"
        "  author = {Shared, Ada},\n"
        "  year = {2023},\n"
        f"  abstract = {{{abstract}}},\n"
        "  doi = {10.21203/rs.3.rs-123/v1},\n"
        "}\n"
        "@article{published,\n"
        "  title = {A shared work},\n"
        "  author = {Shared, Ada},\n"
        "  year = {2024},\n"
        "  doi = {10.9999/published},\n"
        "}\n",
        encoding="utf-8",
      )
      artifacts = root / "artifacts"
      artifacts.mkdir()
      exceptions = artifacts / "exceptions.json"
      exceptions.write_text("{}\n", encoding="utf-8")
      old_retrieval = "2024-01-02T03:04:05+00:00"
      (artifacts / "abstract_provenance.jsonl").write_text(
        json.dumps(
          {
            "schema_version": 1,
            "work_id": "doi:10.21203/rs.3.rs-123/v1",
            "citekey": "preprint",
            "aliases": ["preprint"],
            "source": "crossref",
            "source_url": "https://example.test/old",
            "retrieved_at": old_retrieval,
            "text_sha256": hashlib.sha256(
              abstract.encode("utf-8")
            ).hexdigest(),
            "license": "source rights retained",
          },
          sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
      )
      config = PaperbotConfig(
        bibliography_path=bibliography,
        artifact_dir=artifacts,
        abstract_exceptions_path=exceptions,
      )

      result = backfill_bibliography(config)
      [provenance] = [
        json.loads(line)
        for line in (artifacts / "abstract_provenance.jsonl")
        .read_text(encoding="utf-8")
        .splitlines()
      ]

      self.assertEqual(result.unresolved, ())
      self.assertEqual(provenance["work_id"], "doi:10.9999/published")
      self.assertEqual(provenance["source"], "crossref")
      self.assertEqual(
        provenance["source_url"], "https://example.test/old"
      )
      self.assertEqual(provenance["retrieved_at"], old_retrieval)


if __name__ == "__main__":
  unittest.main()
