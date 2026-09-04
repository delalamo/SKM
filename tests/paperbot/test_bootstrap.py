from __future__ import annotations

import json
import tempfile
import unittest
import urllib.parse
from pathlib import Path

from scripts.paperbot.bootstrap import (
  BibliographyIdentityIndex,
  PubmedMetadata,
  bibliography_identity_index,
  build_pubmed_query,
  fetch_pubmed_ids,
  parse_pubmed_feed,
  rank_negative_records,
  select_negative_records,
)
from scripts.paperbot.negative_policy import (
  MANUALLY_EXCLUDED_PMIDS,
  NEGATIVE_DATASET,
  NEGATIVE_GROUPS,
  TARGET_TEXT_RE,
)


def paper(
  pmid: str,
  group: str,
  *,
  title: str = "An unrelated biological result",
  abstract: str = "We study a distant biological population and report reproducible observations.",
  doi: str = "",
  mesh_headings: tuple[str, ...] | None = None,
  major_topics: tuple[str, ...] | None = None,
) -> PubmedMetadata:
  configured_topics = NEGATIVE_GROUPS[group][1]
  topics = major_topics or (configured_topics[0],)
  return PubmedMetadata(
    pmid=pmid,
    doi=doi,
    title=title,
    abstract=abstract,
    authors=("Example, Ada",),
    mesh_headings=mesh_headings or topics,
    major_topics=topics,
    publication_types=("Journal Article",),
    languages=("eng",),
    published_year=2022,
    journal="Journal of Unrelated Biology",
    medline_status="MEDLINE",
    url=f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
  )


class BootstrapTests(unittest.TestCase):
  def test_strata_have_clear_and_hard_biological_quotas(self) -> None:
    self.assertEqual(sum(quota for quota, _topics in NEGATIVE_GROUPS.values()), 669)
    self.assertEqual(
      sum(NEGATIVE_GROUPS[group][0] for group in tuple(NEGATIVE_GROUPS)[:5]), 535
    )
    self.assertEqual(
      sum(NEGATIVE_GROUPS[group][0] for group in tuple(NEGATIVE_GROUPS)[5:]), 134
    )
    self.assertTrue(all(topics for _quota, topics in NEGATIVE_GROUPS.values()))

  def test_query_requires_medline_major_topic_and_narrow_target_exclusions(self) -> None:
    query = build_pubmed_query(("Ecology",))
    for expected in (
      "medline[sb]",
      "english[la]",
      "hasabstract",
      '"Journal Article"[pt]',
      '"Ecology"[majr]',
      '"2018/01/01"[dp] : "2025/12/31"[dp]',
      '"Protein Engineering"[mh]',
      '"protein design"[tiab]',
    ):
      self.assertIn(expected, query)
    self.assertNotIn('"protein"[tiab]', query)
    self.assertNotIn('"machine learning"[tiab]', query)

  def test_narrow_text_guard_handles_variants_without_blocking_generic_biology(self) -> None:
    for text in (
      "antibody-engineering",
      "de novo protein design",
      "protein language models",
      "directed molecular evolution",
      "RFdiffusion",
    ):
      self.assertIsNotNone(TARGET_TEXT_RE.search(text), text)
    self.assertIsNone(
      TARGET_TEXT_RE.search("Machine learning measures proteins in an ecological survey")
    )

  def test_manually_audited_target_leaks_are_ineligible(self) -> None:
    candidates = {
      "biosensors": [
        paper(
          "34199271",
          "biosensors",
          title="Characterization of Two NMN Deamidase Mutants",
        ),
        paper("12345", "biosensors", title="A clean electrochemical biosensor"),
      ]
    }
    ranked = rank_negative_records(candidates, "seed")
    self.assertEqual([row.pmid for row in ranked["biosensors"]], ["12345"])
    self.assertIn("34199271", MANUALLY_EXCLUDED_PMIDS)

  def test_parse_pubmed_feed_preserves_major_mesh_and_structured_abstract(self) -> None:
    payload = b"""<?xml version='1.0'?>
    <PubmedArticleSet>
      <PubmedArticle>
        <MedlineCitation Status='MEDLINE'>
          <PMID>12345</PMID>
          <DateCompleted><Year>2023</Year></DateCompleted>
          <Article>
            <Journal><JournalIssue><PubDate><Year>2022</Year></PubDate></JournalIssue>
              <Title>Ecology Letters</Title></Journal>
            <ArticleTitle>Seasonal &amp; ecological dynamics</ArticleTitle>
            <Abstract>
              <AbstractText Label='BACKGROUND'>Earlier observations.</AbstractText>
              <AbstractText Label='RESULTS'>We report a new result.</AbstractText>
            </Abstract>
            <AuthorList><Author><LastName>Example</LastName><ForeName>Ada</ForeName></Author></AuthorList>
            <Language>eng</Language>
            <PublicationTypeList><PublicationType>Journal Article</PublicationType></PublicationTypeList>
          </Article>
          <MeshHeadingList>
            <MeshHeading><DescriptorName MajorTopicYN='Y'>Ecology</DescriptorName></MeshHeading>
            <MeshHeading><DescriptorName MajorTopicYN='N'>Seasons</DescriptorName></MeshHeading>
          </MeshHeadingList>
        </MedlineCitation>
        <PubmedData><ArticleIdList><ArticleId IdType='doi'>10.1000/ABC</ArticleId></ArticleIdList></PubmedData>
      </PubmedArticle>
    </PubmedArticleSet>"""
    records = parse_pubmed_feed(payload)
    self.assertEqual(len(records), 1)
    record = records[0]
    self.assertEqual(record.pmid, "12345")
    self.assertEqual(record.doi, "10.1000/abc")
    self.assertEqual(record.major_topics, ("Ecology",))
    self.assertEqual(record.mesh_headings, ("Ecology", "Seasons"))
    self.assertEqual(
      record.abstract,
      "BACKGROUND: Earlier observations. RESULTS: We report a new result.",
    )
    self.assertEqual(record.published_year, 2022)

  def test_esearch_recursively_partitions_a_query_over_the_uid_limit(self) -> None:
    seen_terms: list[str] = []

    def request(url: str, _agent: str) -> bytes:
      term = urllib.parse.parse_qs(urllib.parse.urlsplit(url).query)["term"][0]
      seen_terms.append(term)
      if '"2018/01/01"[dp] : "2025/12/31"[dp]' in term:
        result = {"count": "10000", "idlist": [str(i) for i in range(9999)]}
      elif '"2018/01/01"[dp]' in term:
        result = {"count": "1", "idlist": ["10"]}
      else:
        result = {"count": "1", "idlist": ["20"]}
      return json.dumps({"esearchresult": result}).encode()

    ids = fetch_pubmed_ids(
      ("Ecology",), contact_email="bot@example.org", request_bytes=request, sleep=lambda _: None
    )
    self.assertEqual(ids, ["10", "20"])
    self.assertEqual(len(seen_terms), 3)

  def test_bibliography_identity_index_includes_doi_pmid_and_title(self) -> None:
    with tempfile.TemporaryDirectory() as directory:
      path = Path(directory) / "bibliography.bib"
      path.write_text(
        """@article{known, title={A Known Work}, author={Doe, Jane}, year={2022},
        doi={10.1000/KNOWN}, pmid={777}, abstract={Known abstract.}}\n""",
        encoding="utf-8",
      )
      index = bibliography_identity_index(path)
    self.assertIn("doi:10.1000/known", index.identifiers)
    self.assertIn("pmid:777", index.identifiers)
    self.assertIn("a known work", index.normalized_titles)

  def test_mesh_descendant_major_topic_remains_in_queried_stratum(self) -> None:
    # PubMed explodes Plant Physiological Phenomena to narrower descriptors;
    # the fetched record need not repeat the parent descriptor verbatim.
    candidate = paper(
      "12346",
      "plant_biology",
      major_topics=("Photosynthesis",),
    )
    ranked = rank_negative_records({"plant_biology": [candidate]}, "seed")
    self.assertEqual(ranked["plant_biology"], [candidate])

  def test_selection_is_deterministic_deduplicated_and_excludes_bibliography(self) -> None:
    candidates: dict[str, list[PubmedMetadata]] = {}
    next_id = 100_000
    for group, (quota, _topics) in NEGATIVE_GROUPS.items():
      rows = []
      for index in range(quota + 4):
        next_id += 1
        rows.append(
          paper(
            str(next_id),
            group,
            title=f"Unrelated {group} observation {index}",
            doi=f"10.1000/{next_id}",
          )
        )
      rows.extend(
        (
          paper(
            str(next_id + 1),
            group,
            title=f"Protein design in {group}",
            abstract="We introduce a de novo protein design method.",
          ),
          paper("777", group, title=f"Known PMID in {group}"),
          paper(str(next_id + 2), group, title="A Known Bibliography Title"),
        )
      )
      candidates[group] = rows
      next_id += 2

    bibliography = BibliographyIdentityIndex(
      frozenset({"pmid:777"}), frozenset({"a known bibliography title"})
    )
    first = select_negative_records(candidates, "seed", bibliography=bibliography)
    second = select_negative_records(candidates, "seed", bibliography=bibliography)
    self.assertEqual(first, second)
    self.assertEqual(len(first), 669)
    self.assertTrue(all(row["dataset"] == NEGATIVE_DATASET for row in first))
    self.assertTrue(all(str(row["paper_id"]).startswith("pmid:") for row in first))
    self.assertFalse(any(row["pmid"] == "777" for row in first))
    self.assertFalse(any("Protein design" in str(row["title"]) for row in first))

  def test_graph_acceptance_filter_is_applied_before_quota_fill(self) -> None:
    candidates: dict[str, list[PubmedMetadata]] = {}
    next_id = 800_000
    for group, (quota, _topics) in NEGATIVE_GROUPS.items():
      rows = []
      for index in range(quota + 2):
        next_id += 1
        rows.append(paper(str(next_id), group, title=f"Graph candidate {group} {index}"))
      candidates[group] = rows
    ranked = rank_negative_records(candidates, "seed")
    accepted = {
      f"pmid:{record.pmid}"
      for rows in ranked.values()
      for record in rows[1:]
    }
    graph_audit = {
      identifier: {
        "accepted": True,
        "pmid": identifier.removeprefix("pmid:"),
        "references_available": True,
        "reference_count": 1,
        "direct_positive_work_count": 0,
        "shared_reference_count": 0,
        "max_shared_reference_count": 0,
        "shared_reference_rejection_threshold": 3,
      }
      for identifier in accepted
    }
    selected = select_negative_records(
      candidates,
      "seed",
      accepted_pmids=accepted,
      graph_audit=graph_audit,
    )
    self.assertEqual(len(selected), 669)
    self.assertTrue(all(row["academic_graph"]["accepted"] for row in selected))
    for group, rows in ranked.items():
      selected_ids = [row["pmid"] for row in selected if row["group"] == group]
      self.assertNotIn(rows[0].pmid, selected_ids)

  def test_graph_audit_must_be_bound_to_the_selected_pmid(self) -> None:
    candidates: dict[str, list[PubmedMetadata]] = {}
    next_id = 900_000
    for group, (quota, _topics) in NEGATIVE_GROUPS.items():
      rows = []
      for index in range(quota):
        next_id += 1
        rows.append(paper(str(next_id), group, title=f"Bound graph {group} {index}"))
      candidates[group] = rows
    ranked = rank_negative_records(candidates, "seed")
    accepted = {
      f"pmid:{record.pmid}"
      for rows in ranked.values()
      for record in rows
    }
    graph_audit = {
      identifier: {
        "accepted": True,
        "pmid": "wrong-pmid",
        "references_available": True,
        "reference_count": 1,
      }
      for identifier in accepted
    }
    with self.assertRaisesRegex(RuntimeError, "not bound"):
      select_negative_records(
        candidates,
        "seed",
        accepted_pmids=accepted,
        graph_audit=graph_audit,
      )


if __name__ == "__main__":
  unittest.main()
