from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from typing import Mapping

from scripts.paperbot.bibliography import CanonicalWork
from scripts.paperbot.citation_graph import (
  GraphCoverageError,
  SemanticScholarClient,
  audit_negative_graph_distance,
  positive_identifiers_from_works,
  semantic_scholar_identifier,
)


class FakeGraphRequest:
  def __init__(
    self,
    resolutions: Mapping[str, str | None],
    references: Mapping[str, list[str] | None],
  ):
    self.resolutions = dict(resolutions)
    self.references = dict(references)
    self.calls: list[tuple[str, ...]] = []

  def __call__(
    self,
    method: str,
    url: str,
    headers: Mapping[str, str],
    payload: Mapping[str, object],
  ) -> object:
    del method, headers
    identifiers = tuple(payload["ids"])  # type: ignore[arg-type]
    self.calls.append(identifiers)
    if "references.paperId" not in url:
      return [
        {"paperId": self.resolutions[value]}
        if self.resolutions.get(value)
        else None
        for value in identifiers
      ]
    response: list[object] = []
    for paper_id in identifiers:
      references = self.references.get(paper_id)
      if paper_id not in self.references:
        response.append(None)
      elif references is None:
        # A resolved graph node whose reference list is not available is
        # intentionally different from an available empty reference list.
        response.append({"paperId": paper_id})
      else:
        response.append(
          {
            "paperId": paper_id,
            "references": [{"paperId": value} for value in references],
          }
        )
    return response


def client(request: FakeGraphRequest, **kwargs: object) -> SemanticScholarClient:
  return SemanticScholarClient(
    request=request,
    min_interval=0,
    **kwargs,  # type: ignore[arg-type]
  )


class CitationGraphTests(unittest.TestCase):
  def test_identifier_conversion_and_positive_work_mapping(self) -> None:
    self.assertEqual(
      semantic_scholar_identifier("doi:https://doi.org/10.1000/Example"),
      "DOI:10.1000/example",
    )
    self.assertEqual(semantic_scholar_identifier("pmid:00123"), "PMID:00123")
    self.assertEqual(
      semantic_scholar_identifier("arxiv:2501.12345v2"), "ARXIV:2501.12345"
    )
    self.assertEqual(semantic_scholar_identifier("fallback:abc"), "")

    work = CanonicalWork(
      work_id="doi:10.1000/example",
      citekey="example2025",
      aliases=("example2025",),
      identifiers=(
        "pmid:123",
        "doi:10.1000/Example",
        "arxiv:2501.12345v2",
        "fallback:ignored",
      ),
      entry_type="article",
      fields={"title": "Example"},
    )
    self.assertEqual(
      positive_identifiers_from_works([work]),
      {
        "doi:10.1000/example": (
          "ARXIV:2501.12345",
          "DOI:10.1000/example",
          "PMID:123",
        )
      },
    )

  def test_rejects_direct_edges_and_substantive_bibliographic_coupling(self) -> None:
    resolutions = {
      "DOI:10.1/positive": "POSITIVE-1",
      "PMID:900": "POSITIVE-2",
      "PMID:1": "NEGATIVE-FAR",
      "PMID:2": "NEGATIVE-CITES-POSITIVE",
      "PMID:3": "NEGATIVE-CITED-BY-POSITIVE",
      "PMID:4": "NEGATIVE-SHARED",
      "PMID:5": None,
      "PMID:6": "NEGATIVE-NO-REFERENCES",
      "PMID:7": "NEGATIVE-INCIDENTAL-SHARED",
      "PMID:8": "POSITIVE-2",
    }
    references = {
      "POSITIVE-1": [
        "COMMON-REFERENCE-1",
        "COMMON-REFERENCE-2",
        "COMMON-REFERENCE-3",
        "NEGATIVE-CITED-BY-POSITIVE",
      ],
      "POSITIVE-2": ["POSITIVE-ONLY-REFERENCE"],
      "NEGATIVE-FAR": ["DISTANT-REFERENCE"],
      "NEGATIVE-CITES-POSITIVE": ["POSITIVE-1"],
      "NEGATIVE-CITED-BY-POSITIVE": ["OTHER-REFERENCE"],
      "NEGATIVE-SHARED": [
        "COMMON-REFERENCE-1",
        "COMMON-REFERENCE-2",
        "COMMON-REFERENCE-3",
      ],
      "NEGATIVE-NO-REFERENCES": None,
      "NEGATIVE-INCIDENTAL-SHARED": ["COMMON-REFERENCE-1"],
    }
    transport = FakeGraphRequest(resolutions, references)
    graph = audit_negative_graph_distance(
      {
        "positive:one": ("DOI:10.1/positive",),
        "positive:two": ("PMID:900",),
      },
      {
        "far": "1",
        "cites-positive": "2",
        "cited-by-positive": "3",
        "shared": "4",
        "unresolved": "5",
        "unavailable": "6",
        "incidental-shared": "7",
        "same-work": "8",
      },
      client=client(transport, batch_size=2),
      min_positive_coverage=1.0,
    )

    self.assertEqual(graph.accepted_ids, ("far", "incidental-shared"))
    self.assertEqual(
      {key: value.rejection_reason for key, value in graph.records.items()},
      {
        "cited-by-positive": "direct_citation",
        "cites-positive": "direct_citation",
        "far": None,
        "incidental-shared": None,
        "shared": "shared_reference",
        "same-work": "same_work",
        "unavailable": "references_unavailable",
        "unresolved": "unresolved",
      },
    )
    self.assertEqual(
      graph.records["cited-by-positive"].direct_positive_work_ids,
      ("positive:one",),
    )
    self.assertEqual(
      graph.records["shared"].shared_reference_ids,
      ("COMMON-REFERENCE-1", "COMMON-REFERENCE-2", "COMMON-REFERENCE-3"),
    )
    self.assertEqual(graph.records["shared"].max_shared_reference_count, 3)
    self.assertEqual(
      graph.records["incidental-shared"].max_shared_reference_count,
      1,
    )
    self.assertTrue(all(len(call) <= 2 for call in transport.calls))
    metadata = graph.metadata()
    self.assertEqual(metadata["accepted"], 2)
    self.assertEqual(
      metadata["rejection_counts"],
      {
        "direct_citation": 2,
        "references_unavailable": 1,
        "same_work": 1,
        "shared_reference": 1,
        "unresolved": 1,
      },
    )
    self.assertEqual(
      graph.records["same-work"].same_positive_work_ids,
      ("positive:two",),
    )

  def test_empty_reference_list_fails_closed(self) -> None:
    transport = FakeGraphRequest(
      {"PMID:90": "POSITIVE", "PMID:10": "NEGATIVE"},
      {"POSITIVE": ["POSITIVE-REFERENCE"], "NEGATIVE": []},
    )
    graph = audit_negative_graph_distance(
      {"positive": ("PMID:90",)},
      {"negative": "10"},
      client=client(transport),
      min_positive_coverage=1.0,
    )
    self.assertEqual(graph.accepted_ids, ())
    self.assertFalse(graph.records["negative"].references_available)
    self.assertEqual(graph.records["negative"].reference_count, 0)
    self.assertEqual(
      graph.records["negative"].rejection_reason,
      "references_unavailable",
    )

  def test_positive_coverage_floor_records_resolution_and_references_separately(self) -> None:
    transport = FakeGraphRequest(
      {
        "PMID:90": "POSITIVE-COVERED",
        "PMID:91": "POSITIVE-NO-REFERENCES",
        "PMID:92": None,
        "PMID:10": "NEGATIVE",
      },
      {
        "POSITIVE-COVERED": ["POSITIVE-REFERENCE"],
        "POSITIVE-NO-REFERENCES": None,
        "NEGATIVE": ["NEGATIVE-REFERENCE"],
      },
    )
    with self.assertRaises(GraphCoverageError) as context:
      audit_negative_graph_distance(
        {
          "covered": ("PMID:90",),
          "no-references": ("PMID:91",),
          "unresolved": ("PMID:92",),
        },
        {"negative": "10"},
        client=client(transport),
        min_positive_coverage=0.90,
      )
    coverage = context.exception.coverage
    self.assertEqual(coverage.positive_work_total, 3)
    self.assertEqual(coverage.positive_work_resolved, 2)
    self.assertEqual(coverage.positive_work_with_references, 1)
    self.assertAlmostEqual(coverage.positive_resolution_coverage, 2 / 3)
    self.assertAlmostEqual(coverage.positive_reference_coverage, 1 / 3)

  def test_caller_selected_cache_resumes_without_network_requests(self) -> None:
    with tempfile.TemporaryDirectory() as directory:
      cache_path = Path(directory) / "semantic-scholar.json"
      first_transport = FakeGraphRequest(
        {"PMID:90": "POSITIVE", "PMID:10": "NEGATIVE"},
        {"POSITIVE": ["POSITIVE-REFERENCE"], "NEGATIVE": ["NEGATIVE-REFERENCE"]},
      )
      first = audit_negative_graph_distance(
        {"positive": ("PMID:90",)},
        {"negative": "10"},
        client=client(first_transport, cache_path=cache_path),
        min_positive_coverage=1.0,
      )
      self.assertTrue(cache_path.exists())
      self.assertGreater(len(first_transport.calls), 0)

      second_transport = FakeGraphRequest({}, {})
      second = audit_negative_graph_distance(
        {"positive": ("PMID:90",)},
        {"negative": "10"},
        client=client(second_transport, cache_path=cache_path),
        min_positive_coverage=1.0,
      )
      self.assertEqual(second_transport.calls, [])
      self.assertEqual(first.metadata(), second.metadata())
      self.assertEqual([path.name for path in Path(directory).iterdir()], [cache_path.name])


if __name__ == "__main__":
  unittest.main()
