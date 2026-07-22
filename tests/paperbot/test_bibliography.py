from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from scripts.paperbot.bibliography import (  # noqa: E402
  AbstractCompletenessError,
  BibliographyEntry,
  canonicalize_entries,
  load_title_only_exceptions,
  normalize_abstract,
  normalize_doi,
  parse_bibtex,
  render_bibtex,
  require_abstracts,
  semantic_bibliography_hash,
)
from scripts.reconcile_bibliography import (  # noqa: E402
  BibEntry as ReconcilerEntry,
  entry_from_metadata,
  metadata_from_csl,
  render_entry as render_reconciled_entry,
)


SAMPLE = r"""
@article{alpha2024,
  title = {{A} nested {Title}},
  author = {Alpha, Alice and Beta, Bob},
  year = {2024},
  abstract = {Background: useful. <i>Result</i>: strong.},
  doi = {https://doi.org/10.1000/Example.1},
  custom = {preserved},
}

@misc{alphaAlias,
  title = "A nested {Title}",
  author = "Alpha, Alice",
  year = 2024,
  doi = "10.1000/example.1",
}
"""


class BibtexTests(unittest.TestCase):
  def test_parse_and_render_preserve_abstract_and_unknown_fields(self) -> None:
    entries = parse_bibtex(SAMPLE)
    self.assertEqual(len(entries), 2)
    self.assertEqual(entries[0].fields["abstract"], "Background: useful. <i>Result</i>: strong.")
    self.assertEqual(entries[0].fields["custom"], "preserved")

    reparsed = parse_bibtex(render_bibtex(entries))
    self.assertEqual(reparsed[0].fields["abstract"], entries[0].fields["abstract"])
    self.assertEqual(reparsed[0].fields["custom"], "preserved")

  def test_quotes_inside_braced_abstract_do_not_unbalance_later_entries(self) -> None:
    source = '''
@article{quoted,
  title = {Quoted result},
  abstract = {The authors call this a "surprising result without a closing quote.},
}
@article{later,
  title = {Later entry},
  abstract = {Still parseable.},
}
'''
    entries = parse_bibtex(source)
    self.assertEqual([entry.key for entry in entries], ["quoted", "later"])
    self.assertIn('"surprising result', entries[0].abstract)

  def test_render_escapes_percent_without_changing_semantic_abstract(self) -> None:
    entry = BibliographyEntry(
      "article",
      "percent",
      {"title": "A 50% result", "abstract": r"Success was 50% with a pre-escaped 25\% baseline."},
    )
    rendered = render_bibtex([entry])
    self.assertIn(r"title = {A 50\% result}", rendered)
    self.assertIn(r"abstract = {Success was 50\% with a pre-escaped 25\% baseline.}", rendered)

    reparsed = parse_bibtex(rendered)[0]
    self.assertEqual(reparsed.abstract, "Success was 50% with a pre-escaped 25% baseline.")
    before = semantic_bibliography_hash(canonicalize_entries([entry]))
    after = semantic_bibliography_hash(canonicalize_entries([reparsed]))
    self.assertEqual(before, after)

  def test_normalize_abstract_removes_markup_and_explicit_trailer(self) -> None:
    value = "<jats:p>First&nbsp; result.</jats:p>  Second. Competing interests: None declared."
    self.assertEqual(normalize_abstract(value), "First result. Second.")

  def test_normalize_doi_strips_biorxiv_version(self) -> None:
    self.assertEqual(normalize_doi("https://doi.org/10.1101/2024.01.02.123456v3"), "10.1101/2024.01.02.123456")

  def test_canonicalize_merges_shared_identifier_once(self) -> None:
    works = canonicalize_entries(parse_bibtex(SAMPLE))
    self.assertEqual(len(works), 1)
    self.assertEqual(works[0].work_id, "doi:10.1000/example.1")
    self.assertEqual(works[0].aliases, ("alpha2024", "alphaAlias"))
    self.assertIn("Result", works[0].abstract)

  def test_title_fallback_does_not_merge_conflicting_dois(self) -> None:
    entries = [
      BibliographyEntry("article", "a", {"title": "Same", "author": "Smith, A", "year": "2020", "doi": "10.1/a", "abstract": "One"}),
      BibliographyEntry("article", "b", {"title": "Same", "author": "Smith, A", "year": "2020", "doi": "10.1/b", "abstract": "Two"}),
    ]
    self.assertEqual(len(canonicalize_entries(entries)), 2)

  def test_identifierless_alias_can_join_identified_work(self) -> None:
    entries = [
      BibliographyEntry("article", "a", {"title": "Same", "author": "Smith, A", "year": "2020", "doi": "10.1234/a", "abstract": "One"}),
      BibliographyEntry("article", "b", {"title": "Same", "author": "Smith, A", "year": "2020"}),
    ]
    works = canonicalize_entries(entries)
    self.assertEqual(len(works), 1)
    self.assertEqual(works[0].aliases, ("a", "b"))

  def test_preprint_and_version_of_record_are_one_work(self) -> None:
    entries = [
      BibliographyEntry("misc", "preprint", {"title": "Exact title", "author": "Smith, A", "year": "2022", "doi": "10.1101/2022.01.01.123456", "abstract": "One"}),
      BibliographyEntry("article", "published", {"title": "Exact title", "author": "Smith, A and Jones, B", "year": "2024", "doi": "10.1038/example", "abstract": "One"}),
    ]
    works = canonicalize_entries(entries)
    self.assertEqual(len(works), 1)
    self.assertEqual(works[0].work_id, "doi:10.1038/example")

  def test_abstract_exceptions_are_reasoned_and_affect_hash(self) -> None:
    work = canonicalize_entries([
      BibliographyEntry("book", "oldBook", {"title": "Old book", "author": "Smith, A", "year": "1900"})
    ])
    with self.assertRaises(AbstractCompletenessError):
      require_abstracts(work)
    require_abstracts(work, {"oldBook": "No abstract was published."})
    without_reason = semantic_bibliography_hash(work, {})
    with_reason = semantic_bibliography_hash(work, {"oldBook": "No abstract was published."})
    self.assertNotEqual(without_reason, with_reason)

  def test_exception_file_rejects_empty_reasons(self) -> None:
    with tempfile.TemporaryDirectory() as directory:
      path = Path(directory) / "exceptions.json"
      path.write_text(json.dumps({"oldBook": ""}), encoding="utf-8")
      with self.assertRaises(ValueError):
        load_title_only_exceptions(path)

  def test_structured_exception_file_is_supported(self) -> None:
    with tempfile.TemporaryDirectory() as directory:
      path = Path(directory) / "exceptions.json"
      path.write_text(
        json.dumps(
          {"schema_version": 1, "entries": {"old-book": "No abstract was published."}}
        ),
        encoding="utf-8",
      )
      self.assertEqual(
        load_title_only_exceptions(path),
        {"old-book": "No abstract was published."},
      )

  def test_reconciler_fetches_and_renders_csl_abstract(self) -> None:
    metadata = metadata_from_csl(
      {
        "type": "article-journal",
        "title": "A title",
        "author": [{"family": "Smith", "given": "A"}],
        "issued": {"date-parts": [[2024]]},
        "abstract": "<jats:p>A fetched abstract.</jats:p>",
        "DOI": "10.1234/example",
      },
      "https://doi.org/10.1234/example",
    )
    rendered = render_reconciled_entry(entry_from_metadata("smith2024", metadata))
    self.assertIn("abstract = {A fetched abstract.}", rendered)

  def test_reconciler_render_preserves_existing_abstract_field(self) -> None:
    rendered = render_reconciled_entry(
      ReconcilerEntry("article", "existing", {"title": "Title", "abstract": "Original abstract."})
    )
    self.assertIn("abstract = {Original abstract.}", rendered)

  def test_reconciler_escapes_raw_and_preescaped_percent_idempotently(self) -> None:
    raw = ReconcilerEntry("article", "raw", {"abstract": "A 50% result."})
    escaped = ReconcilerEntry("article", "escaped", {"abstract": r"A 50\% result."})
    self.assertIn(r"abstract = {A 50\% result.}", render_reconciled_entry(raw))
    self.assertIn(r"abstract = {A 50\% result.}", render_reconciled_entry(escaped))


if __name__ == "__main__":
  unittest.main()
