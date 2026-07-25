from __future__ import annotations

import importlib.util
import hashlib
import json
import sys
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path
from unittest.mock import patch


REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from scripts.paperbot.model import (  # noqa: E402
  DEFAULT_MIN_POSITIVE_COVERAGE,
  EMBEDDING_DIMENSION,
  MANUALLY_EXCLUDED_PMIDS,
  NEGATIVE_METADATA_SOURCE,
  NEGATIVE_QUOTAS,
  SEMANTIC_SCHOLAR_PROVIDER,
  SHARED_REFERENCE_REJECTION_THRESHOLD,
  LoadedModel,
  NegativePaper,
  StaleModelError,
  load_negative_corpus,
  negative_category_family,
  negative_selection_key,
  model_errors,
  refresh_model,
  score_embeddings,
  select_negative_corpus,
  validate_negative_corpus,
  validate_negative_metadata,
  check_model,
  _dependency_versions,
  _model_hash,
)
from scripts.paperbot.bibliography import embedding_input_hash  # noqa: E402
from scripts.paperbot.issue_negatives import (  # noqa: E402
  ISSUE_NEGATIVE_CORPUS,
  ISSUE_NEGATIVE_MANIFEST,
  ISSUE_NEGATIVE_MATRIX,
  IssueNegativeRecord,
)


HAS_NUMPY = importlib.util.find_spec("numpy") is not None
HAS_SKLEARN = importlib.util.find_spec("sklearn") is not None


def negative(paper_id: str, category: str, title: str = "Remote topic") -> NegativePaper:
  return NegativePaper(
    paper_id,
    title,
    "An unrelated scientific abstract.",
    category,
    2021,
    {
      "dataset": "pubmed-negatives-v1",
      "pmid": paper_id.removeprefix("pmid:"),
      "mesh_headings": [],
      "academic_graph": {
        "provider": "Semantic Scholar Academic Graph",
        "pmid": paper_id.removeprefix("pmid:"),
        "accepted": True,
        "resolved": True,
        "references_available": True,
        "reference_count": 1,
        "rejection_reason": None,
        "same_positive_work_count": 0,
        "direct_positive_work_count": 0,
        "shared_reference_count": 0,
        "max_shared_reference_count": 0,
        "shared_reference_rejection_threshold": 3,
      },
    },
  )


def valid_negative_metadata(count: int = 1) -> dict[str, object]:
  return {
    "dataset": "pubmed-negatives-v1",
    "source": NEGATIVE_METADATA_SOURCE,
    "count": count,
    "groups": NEGATIVE_QUOTAS,
    "manually_excluded_pmids": sorted(MANUALLY_EXCLUDED_PMIDS),
    "graph_filter_applied": True,
    "audited_bibliography_identity_hash": "a" * 64,
    "academic_graph": {
      "provider": SEMANTIC_SCHOLAR_PROVIDER,
      "rule": (
        "reject candidates sharing at least "
        f"{SHARED_REFERENCE_REJECTION_THRESHOLD} cited papers"
      ),
      "minimum_positive_reference_coverage": DEFAULT_MIN_POSITIVE_COVERAGE,
      "coverage": {
        "positive": {
          "works_total": 10,
          "works_resolved": 8,
          "works_with_references": 8,
          "paper_ids_resolved": 9,
          "paper_ids_with_references": 8,
          "resolution_fraction": 0.8,
          "reference_fraction": 0.8,
        },
        "negative": {
          "works_total": 2,
          "works_resolved": 1,
          "works_with_references": 1,
          "resolution_fraction": 0.5,
          "reference_fraction": 0.5,
        },
      },
      "accepted": 1,
      "rejected": 1,
      "rejection_counts": {"unresolved": 1},
    },
  }


class NegativeCorpusTests(unittest.TestCase):
  def test_dependency_versions_normalize_cpu_torch_build_tag(self) -> None:
    def fake_version(distribution: str) -> str:
      if distribution == "torch":
        return "2.13.0+cpu"
      raise LookupError(distribution)

    with patch("importlib.metadata.version", side_effect=fake_version):
      self.assertEqual(_dependency_versions(), {"python": "3.12", "torch": "2.13.0"})

  def test_category_families(self) -> None:
    self.assertEqual(negative_category_family("ecology"), "ecology")
    self.assertEqual(
      negative_category_family("genomics_transcriptomics"),
      "genomics_transcriptomics",
    )
    self.assertEqual(negative_category_family("astronomy"), "")

  def test_selection_is_hash_deterministic_and_filters_topics(self) -> None:
    candidates = [
      negative("pmid:3", "ecology", "Third"),
      negative("pmid:1", "ecology", "First"),
      negative("pmid:2", "ecology", "A protein design model"),
    ]
    selected = select_negative_corpus(candidates, {"ecology": 1})
    eligible = [candidates[0], candidates[1]]
    expected = min(eligible, key=lambda paper: (negative_selection_key(paper), paper.paper_id))
    self.assertEqual(selected, [expected])

  def test_validation_detects_wrong_quota_and_duplicate(self) -> None:
    paper = negative("pmid:1", "ecology")
    errors = validate_negative_corpus([paper, paper], quotas={"ecology": 1})
    self.assertTrue(any("duplicate negative identifier" in error for error in errors))
    self.assertTrue(any("expected 1" in error for error in errors))

  def test_validation_rejects_a_graph_audit_copied_from_another_paper(self) -> None:
    paper = negative("pmid:1", "ecology")
    paper.metadata["academic_graph"]["pmid"] = "2"  # type: ignore[index]
    errors = validate_negative_corpus([paper], quotas={"ecology": 1})
    self.assertTrue(any("bound to another paper" in error for error in errors))

  def test_load_bootstrap_record_shape(self) -> None:
    payload = {
      "dataset": "pubmed-negatives-v1",
      "paper_id": "pmid:12345",
      "pmid": "12345",
      "title": "Remote topic",
      "abstract": "An unrelated abstract.",
      "group": "ecology",
      "publication_date": "2021-01-01",
    }
    with tempfile.TemporaryDirectory() as directory:
      path = Path(directory) / "pubmed_negatives_v1.jsonl"
      path.write_text(json.dumps(payload) + "\n", encoding="utf-8")
      records = load_negative_corpus(path)
    self.assertEqual(records[0].paper_id, "pmid:12345")
    self.assertEqual(records[0].published_year, 2021)

  def test_negative_metadata_graph_summary_is_internally_consistent(self) -> None:
    with tempfile.TemporaryDirectory() as directory:
      path = Path(directory) / "pubmed_negatives_v1_metadata.json"
      path.write_text(json.dumps(valid_negative_metadata()) + "\n", encoding="utf-8")
      self.assertEqual(
        validate_negative_metadata(path, [negative("pmid:1", "ecology")]),
        [],
      )

  def test_negative_metadata_rejects_graph_provenance_drift(self) -> None:
    cases = {
      "graph filter": lambda value: value.update(graph_filter_applied=False),
      "bibliography audit hash": lambda value: value.update(
        audited_bibliography_identity_hash="not-a-hash"
      ),
      "provider": lambda value: value["academic_graph"].update(provider="other"),
      "rule threshold": lambda value: value["academic_graph"].update(
        rule="reject candidates sharing at least 999 cited papers"
      ),
      "coverage is inconsistent": lambda value: value["academic_graph"][
        "coverage"
      ]["positive"].update(reference_fraction=0.9),
      "rejection counts are inconsistent": lambda value: value[
        "academic_graph"
      ].update(rejection_counts={}),
      "candidate counts are inconsistent": lambda value: value[
        "academic_graph"
      ].update(accepted=2),
    }
    with tempfile.TemporaryDirectory() as directory:
      path = Path(directory) / "pubmed_negatives_v1_metadata.json"
      for expected, mutate in cases.items():
        with self.subTest(expected=expected):
          payload = valid_negative_metadata()
          mutate(payload)
          path.write_text(json.dumps(payload) + "\n", encoding="utf-8")
          errors = validate_negative_metadata(
            path, [negative("pmid:1", "ecology")]
          )
          self.assertTrue(any(expected in error for error in errors), errors)


@unittest.skipUnless(HAS_NUMPY and HAS_SKLEARN, "numpy and scikit-learn are not installed")
class ArtifactTests(unittest.TestCase):
  class FakeEncoder:
    def embed(self, documents):
      import numpy as np

      rows = []
      for title, abstract in documents:
        seed = sum((index + 1) * ord(char) for index, char in enumerate(title + abstract))
        row = np.zeros(EMBEDDING_DIMENSION, dtype=np.float32)
        row[seed % EMBEDDING_DIMENSION] = 1.0
        rows.append(row)
      return np.asarray(rows, dtype=np.float32)

  def setUp(self) -> None:
    self.temporary = tempfile.TemporaryDirectory()
    self.root = Path(self.temporary.name)
    self.bib = self.root / "bibliography.bib"
    self.artifacts = self.root / "artifacts"
    self.artifacts.mkdir()
    self.negatives = self.artifacts / "pubmed_negatives_v1.jsonl"
    self.bib.write_text(
      "@article{positive,\n title={A useful paper},\n author={Smith, A},\n year={2024},\n abstract={Useful biology result.},\n doi={10.1234/useful}\n}\n",
      encoding="utf-8",
    )
    self.negatives.write_text(
      json.dumps({
        "paper_id": "pmid:12345",
        "pmid": "12345",
        "title": "Remote stars",
        "abstract": "An unrelated astronomy result.",
        "group": "ecology",
        "publication_date": "2021-01-01",
      }) + "\n",
      encoding="utf-8",
    )

  def tearDown(self) -> None:
    self.temporary.cleanup()

  def issue_negative(
    self,
    *,
    work_id: str,
    title: str,
    abstract: str,
    issue_number: int = 101,
    aliases: tuple[str, ...] = (),
  ) -> IssueNegativeRecord:
    normalized_aliases = tuple(sorted({work_id, *aliases}))
    return IssueNegativeRecord(
      schema_version=1,
      work_id=work_id,
      aliases=normalized_aliases,
      issue_numbers=(issue_number,),
      issue_urls=(f"https://github.com/delalamo/SKM/issues/{issue_number}",),
      selected_issue_number=issue_number,
      title=title,
      abstract=abstract,
      input_hash=embedding_input_hash(title, abstract),
      metadata_hash=hashlib.sha256(
        f"{work_id}:{issue_number}".encode("utf-8")
      ).hexdigest(),
      active=True,
    )

  def write_issue_negatives(
    self, *records: IssueNegativeRecord
  ) -> None:
    path = self.artifacts / ISSUE_NEGATIVE_CORPUS
    path.write_text(
      "".join(
        json.dumps(record.to_dict(), sort_keys=True) + "\n"
        for record in sorted(records, key=lambda item: item.work_id)
      ),
      encoding="utf-8",
    )

  def test_refresh_check_and_stale_detection(self) -> None:
    manifest = refresh_model(
      self.bib,
      self.artifacts,
      encoder=self.FakeEncoder(),
      strict_negative_quotas=False,
    )
    self.assertEqual(manifest["positive_count"], 1)
    self.assertEqual(check_model(self.bib, self.artifacts, strict_negative_quotas=False)["model_hash"], manifest["model_hash"])

    self.bib.write_text(self.bib.read_text(encoding="utf-8").replace("Useful biology result.", "Changed result."), encoding="utf-8")
    with self.assertRaises(StaleModelError):
      check_model(self.bib, self.artifacts, strict_negative_quotas=False)

  def test_active_issue_negative_extends_the_effective_negative_class(self) -> None:
    self.write_issue_negatives(self.issue_negative(
      work_id="doi:10.9999/irrelevant",
      title="An irrelevant clinical report",
      abstract="This report concerns an unrelated therapeutic intervention.",
    ))

    manifest = refresh_model(
      self.bib,
      self.artifacts,
      encoder=self.FakeEncoder(),
      strict_negative_quotas=False,
    )

    self.assertEqual(manifest["negative_count"], 1)
    self.assertEqual(manifest["issue_negative_count"], 1)
    self.assertEqual(manifest["effective_negative_count"], 2)
    rows = [
      json.loads(line)
      for line in (self.artifacts / ISSUE_NEGATIVE_MANIFEST)
      .read_text(encoding="utf-8")
      .splitlines()
    ]
    self.assertEqual(len(rows), 1)
    self.assertTrue(rows[0]["active"])
    check_model(self.bib, self.artifacts, strict_negative_quotas=False)

  def test_duplicate_issue_provenance_does_not_change_model_version(self) -> None:
    feedback = self.issue_negative(
      work_id="doi:10.9999/irrelevant",
      title="An irrelevant clinical report",
      abstract="This report concerns an unrelated therapeutic intervention.",
    )
    self.write_issue_negatives(feedback)
    original = refresh_model(
      self.bib,
      self.artifacts,
      encoder=self.FakeEncoder(),
      strict_negative_quotas=False,
    )

    self.write_issue_negatives(
      replace(
        feedback,
        issue_numbers=(101, 102),
        issue_urls=(
          "https://github.com/delalamo/SKM/issues/101",
          "https://github.com/delalamo/SKM/issues/102",
        ),
      )
    )
    updated = refresh_model(
      self.bib,
      self.artifacts,
      encoder=self.FakeEncoder(),
      strict_negative_quotas=False,
    )

    self.assertNotEqual(
      original["issue_negative_snapshot_hash"],
      updated["issue_negative_snapshot_hash"],
    )
    self.assertNotEqual(
      original["issue_negative_corpus_hash"],
      updated["issue_negative_corpus_hash"],
    )
    self.assertEqual(
      original["issue_negative_training_hash"],
      updated["issue_negative_training_hash"],
    )
    self.assertEqual(original["model_hash"], updated["model_hash"])
    check_model(self.bib, self.artifacts, strict_negative_quotas=False)

  def test_fit_omits_issue_negative_that_is_in_the_bibliography(self) -> None:
    # The collector should normally mark this omission. The model repeats the
    # identity check so a stale or incorrectly marked snapshot cannot give a
    # bibliography paper negative weight.
    self.write_issue_negatives(self.issue_negative(
      work_id="doi:10.1234/useful",
      title="A stale issue copy of the useful paper",
      abstract="Stale issue text that must not enter the negative class.",
    ))

    manifest = refresh_model(
      self.bib,
      self.artifacts,
      encoder=self.FakeEncoder(),
      strict_negative_quotas=False,
    )

    self.assertEqual(manifest["issue_negative_count"], 0)
    self.assertEqual(manifest["effective_negative_count"], 1)
    self.assertEqual(
      manifest["issue_negative_bibliography_overlap_count"], 1
    )
    self.assertEqual(
      manifest["issue_negative_omission_counts"],
      {"bibliography_overlap": 1},
    )
    check_model(self.bib, self.artifacts, strict_negative_quotas=False)

  def test_fit_omits_issue_negative_already_in_the_fixed_corpus(self) -> None:
    self.write_issue_negatives(self.issue_negative(
      work_id="pmid:12345",
      title="A duplicate fixed negative",
      abstract="Different text cannot bypass the stable PMID identity.",
    ))

    manifest = refresh_model(
      self.bib,
      self.artifacts,
      encoder=self.FakeEncoder(),
      strict_negative_quotas=False,
    )

    self.assertEqual(manifest["issue_negative_count"], 0)
    self.assertEqual(manifest["effective_negative_count"], 1)
    self.assertEqual(manifest["issue_negative_fixed_overlap_count"], 1)
    check_model(self.bib, self.artifacts, strict_negative_quotas=False)

  def test_check_model_accepts_legacy_artifacts_as_empty_feedback(self) -> None:
    import numpy as np

    refresh_model(
      self.bib,
      self.artifacts,
      encoder=self.FakeEncoder(),
      strict_negative_quotas=False,
    )
    manifest_path = self.artifacts / "model_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    with np.load(self.artifacts / "classifier.npz", allow_pickle=False) as model:
      coefficients = np.asarray(model["coef"], dtype=np.float64)
      intercept = float(np.asarray(model["intercept"])[0])
    for field in list(manifest):
      if field.startswith("issue_negative_"):
        manifest.pop(field)
    manifest.pop("effective_negative_count")
    manifest["model_hash"] = _model_hash(
      coefficients,
      intercept,
      manifest["bibliography_hash"],
      manifest["negative_corpus_file_hash"],
      manifest["negative_metadata_file_hash"],
    )
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    for filename in (
      ISSUE_NEGATIVE_CORPUS,
      ISSUE_NEGATIVE_MATRIX,
      ISSUE_NEGATIVE_MANIFEST,
    ):
      (self.artifacts / filename).unlink()

    checked = check_model(
      self.bib, self.artifacts, strict_negative_quotas=False
    )
    self.assertEqual(checked["model_hash"], manifest["model_hash"])

  def test_check_detects_issue_negative_artifact_tampering(self) -> None:
    import numpy as np

    self.write_issue_negatives(self.issue_negative(
      work_id="doi:10.9999/irrelevant",
      title="An irrelevant clinical report",
      abstract="This report concerns an unrelated therapeutic intervention.",
    ))
    refresh_model(
      self.bib,
      self.artifacts,
      encoder=self.FakeEncoder(),
      strict_negative_quotas=False,
    )
    matrix_path = self.artifacts / ISSUE_NEGATIVE_MATRIX
    matrix = np.load(matrix_path, allow_pickle=False)
    matrix[0, 0] += 0.25
    np.save(matrix_path, matrix, allow_pickle=False)

    errors = model_errors(
      self.bib, self.artifacts, strict_negative_quotas=False
    )
    self.assertTrue(
      any("issue_negative_matrix_hash" in error for error in errors),
      errors,
    )

  def test_positive_row_is_stable_when_abstract_changes(self) -> None:
    refresh_model(self.bib, self.artifacts, encoder=self.FakeEncoder(), strict_negative_quotas=False)
    original = [json.loads(line) for line in (self.artifacts / "positive_manifest.jsonl").read_text().splitlines()]
    self.bib.write_text(self.bib.read_text().replace("Useful biology result.", "A different useful result."))
    refresh_model(self.bib, self.artifacts, encoder=self.FakeEncoder(), strict_negative_quotas=False)
    updated = [json.loads(line) for line in (self.artifacts / "positive_manifest.jsonl").read_text().splitlines()]
    self.assertEqual(original[0]["row"], updated[0]["row"])
    self.assertNotEqual(original[0]["input_hash"], updated[0]["input_hash"])

  def test_check_detects_provenance_drift(self) -> None:
    work_id = "doi:10.1234/useful"
    provenance = {
      work_id: {
        "source": "crossref",
        "source_url": "https://api.crossref.org/works/10.1234/useful",
        "retrieved_at": "2026-01-02T00:00:00+00:00",
        "license": "unknown",
      }
    }
    refresh_model(
      self.bib,
      self.artifacts,
      encoder=self.FakeEncoder(),
      abstract_provenance=provenance,
      strict_negative_quotas=False,
    )
    manifest_row = json.loads((self.artifacts / "positive_manifest.jsonl").read_text().strip())
    provenance_row = {
      "schema_version": 1,
      "work_id": work_id,
      "citekey": "positive",
      "aliases": ["positive"],
      "source": "crossref",
      "source_url": "https://api.crossref.org/works/10.1234/useful",
      "retrieved_at": "2026-01-02T00:00:00+00:00",
      "text_sha256": manifest_row["abstract_hash"],
      "license": "unknown",
    }
    provenance_path = self.artifacts / "abstract_provenance.jsonl"
    provenance_path.write_text(json.dumps(provenance_row) + "\n")
    check_model(self.bib, self.artifacts, strict_negative_quotas=False)

    provenance_row["license"] = "changed"
    provenance_path.write_text(json.dumps(provenance_row) + "\n")
    with self.assertRaises(StaleModelError):
      check_model(self.bib, self.artifacts, strict_negative_quotas=False)

  def test_check_detects_recorded_dependency_drift(self) -> None:
    refresh_model(
      self.bib,
      self.artifacts,
      encoder=self.FakeEncoder(),
      strict_negative_quotas=False,
    )
    manifest_path = self.artifacts / "model_manifest.json"
    manifest = json.loads(manifest_path.read_text())
    dependency = next(iter(manifest["dependencies"]))
    manifest["dependencies"][dependency] = "unexpected-version"
    manifest_path.write_text(json.dumps(manifest))
    with self.assertRaises(StaleModelError):
      check_model(self.bib, self.artifacts, strict_negative_quotas=False)

  def test_check_requires_the_complete_runtime_dependency_mapping(self) -> None:
    refresh_model(
      self.bib,
      self.artifacts,
      encoder=self.FakeEncoder(),
      strict_negative_quotas=False,
    )
    manifest_path = self.artifacts / "model_manifest.json"
    manifest = json.loads(manifest_path.read_text())
    manifest["dependencies"].pop(next(iter(manifest["dependencies"])))
    manifest_path.write_text(json.dumps(manifest))
    errors = model_errors(
      self.bib, self.artifacts, strict_negative_quotas=False
    )
    self.assertTrue(any("exactly match the runtime" in error for error in errors))

  def test_check_validates_static_negative_manifest_fields(self) -> None:
    refresh_model(
      self.bib,
      self.artifacts,
      encoder=self.FakeEncoder(),
      strict_negative_quotas=False,
    )
    manifest_path = self.artifacts / "model_manifest.json"
    original = json.loads(manifest_path.read_text())
    for field in (
      "negative_corpus",
      "negative_dataset",
      "negative_source",
      "negative_graph_provider",
      "negative_metadata",
    ):
      with self.subTest(field=field):
        changed = json.loads(json.dumps(original))
        changed[field] = "unexpected"
        manifest_path.write_text(json.dumps(changed))
        errors = model_errors(
          self.bib, self.artifacts, strict_negative_quotas=False
        )
        self.assertTrue(any(field in error for error in errors), errors)
    manifest_path.write_text(json.dumps(original))

  def test_check_compares_recorded_training_metadata_to_refit(self) -> None:
    refresh_model(
      self.bib,
      self.artifacts,
      encoder=self.FakeEncoder(),
      strict_negative_quotas=False,
    )
    manifest_path = self.artifacts / "model_manifest.json"
    manifest = json.loads(manifest_path.read_text())
    manifest["training"]["iterations"] += 1
    manifest_path.write_text(json.dumps(manifest))
    errors = model_errors(
      self.bib, self.artifacts, strict_negative_quotas=False
    )
    self.assertTrue(any("training metadata" in error for error in errors))

  def test_full_negative_metadata_is_frozen(self) -> None:
    refresh_model(
      self.bib,
      self.artifacts,
      encoder=self.FakeEncoder(),
      strict_negative_quotas=False,
    )
    payload = json.loads(self.negatives.read_text())
    payload["authors"] = ["Metadata-only change"]
    self.negatives.write_text(json.dumps(payload) + "\n")

    with self.assertRaises(StaleModelError):
      check_model(self.bib, self.artifacts, strict_negative_quotas=False)
    with self.assertRaisesRegex(ValueError, "frozen negative JSONL corpus changed"):
      refresh_model(
        self.bib,
        self.artifacts,
        encoder=self.FakeEncoder(),
        strict_negative_quotas=False,
      )

  def test_negative_selection_metadata_is_frozen(self) -> None:
    metadata = self.artifacts / "pubmed_negatives_v1_metadata.json"
    metadata.write_text('{"dataset":"test"}\n', encoding="utf-8")
    refresh_model(
      self.bib,
      self.artifacts,
      encoder=self.FakeEncoder(),
      strict_negative_quotas=False,
    )
    metadata.write_text('{"dataset":"changed"}\n', encoding="utf-8")
    with self.assertRaises(StaleModelError):
      check_model(self.bib, self.artifacts, strict_negative_quotas=False)
    with self.assertRaisesRegex(ValueError, "selection metadata changed"):
      refresh_model(
        self.bib,
        self.artifacts,
        encoder=self.FakeEncoder(),
        strict_negative_quotas=False,
      )
    refresh_model(
      self.bib,
      self.artifacts,
      encoder=self.FakeEncoder(),
      strict_negative_quotas=False,
      allow_negative_change=True,
    )

  def test_check_independently_refits_stored_classifier(self) -> None:
    import numpy as np

    refresh_model(
      self.bib,
      self.artifacts,
      encoder=self.FakeEncoder(),
      strict_negative_quotas=False,
    )
    classifier_path = self.artifacts / "classifier.npz"
    with np.load(classifier_path, allow_pickle=False) as stored:
      coefficients = stored["coef"].copy()
      intercept = stored["intercept"].copy()
      classes = stored["classes"].copy()
    coefficients[0] += 0.25
    np.savez(
      classifier_path,
      coef=coefficients,
      intercept=intercept,
      classes=classes,
    )

    errors = model_errors(
      self.bib,
      self.artifacts,
      strict_negative_quotas=False,
    )
    self.assertTrue(any("deterministic refit" in error for error in errors))

  def test_refresh_refuses_to_reuse_corrupt_embedding_matrix(self) -> None:
    import numpy as np

    refresh_model(
      self.bib,
      self.artifacts,
      encoder=self.FakeEncoder(),
      strict_negative_quotas=False,
    )
    matrix_path = self.artifacts / "positive_embeddings.npy"
    matrix = np.load(matrix_path, allow_pickle=False)
    matrix[0, 0] += 0.25
    np.save(matrix_path, matrix, allow_pickle=False)

    with self.assertRaisesRegex(ValueError, "Refusing to reuse corrupt positive"):
      refresh_model(
        self.bib,
        self.artifacts,
        encoder=self.FakeEncoder(),
        strict_negative_quotas=False,
      )

  def test_refresh_reembeds_when_manifest_hash_provenance_is_incomplete(self) -> None:
    refresh_model(
      self.bib,
      self.artifacts,
      encoder=self.FakeEncoder(),
      strict_negative_quotas=False,
    )
    manifest_path = self.artifacts / "model_manifest.json"
    manifest = json.loads(manifest_path.read_text())
    manifest.pop("positive_matrix_hash")
    manifest_path.write_text(json.dumps(manifest))

    encoder = self.FakeEncoder()
    with patch.object(encoder, "embed", wraps=encoder.embed) as embed:
      refresh_model(
        self.bib,
        self.artifacts,
        encoder=encoder,
        strict_negative_quotas=False,
      )
    self.assertEqual(sum(len(call.args[0]) for call in embed.call_args_list), 2)

  def test_refresh_reembeds_when_embedding_specification_is_incompatible(self) -> None:
    refresh_model(
      self.bib,
      self.artifacts,
      encoder=self.FakeEncoder(),
      strict_negative_quotas=False,
    )
    manifest_path = self.artifacts / "model_manifest.json"
    manifest = json.loads(manifest_path.read_text())
    manifest["embedding"]["pooling"] = "different_pooling"
    manifest_path.write_text(json.dumps(manifest))

    encoder = self.FakeEncoder()
    with patch.object(encoder, "embed", wraps=encoder.embed) as embed:
      refreshed = refresh_model(
        self.bib,
        self.artifacts,
        encoder=encoder,
        strict_negative_quotas=False,
      )
    self.assertEqual(sum(len(call.args[0]) for call in embed.call_args_list), 2)
    self.assertEqual(refreshed["embedding"]["pooling"], "first_token_l2_normalized")

  def test_refresh_rejects_positive_negative_identity_or_title_overlap(self) -> None:
    original_bibliography = self.bib.read_text()
    cases = {
      "identifier": original_bibliography.replace(
        " doi={10.1234/useful}",
        " doi={10.1234/useful},\n pmid={12345}",
      ),
      "title": original_bibliography.replace("A useful paper", "Remote stars"),
    }
    for expected, bibliography in cases.items():
      with self.subTest(expected=expected):
        self.bib.write_text(bibliography)
        with self.assertRaisesRegex(ValueError, f"overlaps.*{expected}"):
          refresh_model(
            self.bib,
            self.artifacts,
            encoder=self.FakeEncoder(),
            strict_negative_quotas=False,
          )
        self.bib.write_text(original_bibliography)

  def test_check_detects_when_a_negative_later_becomes_positive(self) -> None:
    refresh_model(
      self.bib,
      self.artifacts,
      encoder=self.FakeEncoder(),
      strict_negative_quotas=False,
    )
    self.bib.write_text(
      self.bib.read_text().replace("A useful paper", "Remote stars")
    )
    errors = model_errors(
      self.bib, self.artifacts, strict_negative_quotas=False
    )
    self.assertTrue(any("overlaps the positive bibliography" in error for error in errors))

  def test_scores_use_positive_class_sigmoid(self) -> None:
    import numpy as np

    coefficients = np.zeros(EMBEDDING_DIMENSION)
    coefficients[0] = 2.0
    model = LoadedModel(coefficients, -1.0, "test")
    rows = np.zeros((2, EMBEDDING_DIMENSION))
    rows[1, 0] = 1.0
    scores = score_embeddings(rows, model)
    self.assertLess(scores[0], 0.5)
    self.assertGreater(scores[1], 0.5)


if __name__ == "__main__":
  unittest.main()
