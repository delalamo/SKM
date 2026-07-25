from __future__ import annotations

from datetime import UTC, datetime
from itertools import permutations

from scripts.paperbot.records import (
  PaperRecord,
  arxiv_version,
  chemrxiv_version,
  deduplicate_records,
  normalize_arxiv_id,
  normalize_doi,
  normalize_pmid,
  normalize_title,
)


def paper(**overrides: object) -> PaperRecord:
  values: dict[str, object] = {
    "source": "biorxiv",
    "source_id": "10.1101/2026.01.01.123456",
    "title": "A useful protein paper",
    "abstract": "First abstract.",
    "authors": ("Ada Lovelace", "Grace Hopper"),
    "created_at": datetime(2026, 1, 1, tzinfo=UTC),
    "updated_at": datetime(2026, 1, 1, tzinfo=UTC),
    "doi": "10.1101/2026.01.01.123456",
    "version": "1",
  }
  values.update(overrides)
  return PaperRecord(**values)  # type: ignore[arg-type]


def test_identifier_and_title_normalization() -> None:
  assert normalize_doi("https://doi.org/10.1234/ABC.5.") == "10.1234/abc.5"
  assert normalize_pmid("https://pubmed.ncbi.nlm.nih.gov/12345678/") == "12345678"
  assert normalize_arxiv_id("https://arxiv.org/pdf/2401.12345v7.pdf") == "2401.12345"
  assert arxiv_version("arXiv:2401.12345v7") == "7"
  assert chemrxiv_version("10.26434/chemrxiv.15006393/v4") == "4"
  assert normalize_title("{Café}: A <i>Test</i>") == "cafe a test"


def test_record_normalizes_utc_and_exposes_stable_aliases() -> None:
  record = PaperRecord(
    source="ChemRxiv",
    source_id="ABC123",
    title="  New chemistry  ",
    abstract="<p>An abstract</p>",
    authors=("Lovelace, Ada",),
    created_at="2026-02-03T04:05:06Z",
    doi="10.26434/chemrxiv-2026-abcd-v3",
    version="3",
    related_ids=("doi:10.1000/JOURNAL", "chemrxiv:older-id"),
  )

  assert record.created_at == datetime(2026, 2, 3, 4, 5, 6, tzinfo=UTC)
  assert record.canonical_id == "doi:10.26434/chemrxiv-2026-abcd"
  assert {
    "doi:10.26434/chemrxiv-2026-abcd-v3",
    "doi:10.26434/chemrxiv-2026-abcd",
    "doi:10.1000/journal",
    "chemrxiv:abc123",
    "chemrxiv:older-id",
  }.issubset(record.identity_aliases(include_title=False))


def test_record_removes_unmistakable_abstract_trailers() -> None:
  record = paper(
    abstract=(
      r"The result was 98.5\%. The scientific abstract ends here. "
      "TOC Figure O_FIG O_LINKSMALLFIG "
      'WIDTH=200 SRC="FIGDIR/small/example.gif"> View larger version (27K): '
      "org.highwire.dtl.DTLVardef@deadbeef"
    )
  )

  assert record.abstract == "The result was 98.5%. The scientific abstract ends here."


def test_current_chemrxiv_slash_versions_share_one_identity() -> None:
  first = PaperRecord(
    source="chemrxiv",
    source_id="10.26434/chemrxiv.15006393/v1",
    title="New chemistry",
    abstract="First version.",
    authors=("Ada Lovelace",),
    created_at="2026-02-03T00:00:00Z",
    updated_at="2026-02-03T00:00:00Z",
    doi="10.26434/chemrxiv.15006393/v1",
    version="1",
  )
  second = PaperRecord(
    source="chemrxiv",
    source_id="10.26434/chemrxiv.15006393/v2",
    title="New chemistry",
    abstract="Second version.",
    authors=("Ada Lovelace",),
    created_at="2026-02-03T00:00:00Z",
    updated_at="2026-02-04T00:00:00Z",
    doi="10.26434/chemrxiv.15006393/v2",
    version="2",
  )

  assert first.canonical_id == "doi:10.26434/chemrxiv.15006393"
  assert second.canonical_id == first.canonical_id
  merged = deduplicate_records([first, second])
  assert len(merged) == 1
  assert merged[0].version == "2"
  assert merged[0].abstract == "Second version."


def test_deduplicate_revisions_uses_latest_version_metadata() -> None:
  first = paper()
  second = paper(
    abstract="The revised and more complete abstract.",
    updated_at=datetime(2026, 1, 4, tzinfo=UTC),
    version="2",
  )

  merged = deduplicate_records([second, first])

  assert len(merged) == 1
  assert merged[0].abstract == "The revised and more complete abstract."
  assert merged[0].version == "2"
  assert merged[0].created_at == first.created_at


def test_preprint_publication_relationship_merges_transitively() -> None:
  preprint = paper(related_ids=("doi:10.1000/final",))
  pubmed = PaperRecord(
    source="pubmed",
    source_id="999",
    title=preprint.title,
    abstract="Published abstract.",
    authors=preprint.authors,
    created_at=datetime(2026, 2, 1, tzinfo=UTC),
    updated_at=datetime(2026, 2, 2, tzinfo=UTC),
    doi="10.1000/final",
    pmid="999",
  )

  merged = deduplicate_records([preprint, pubmed])

  assert len(merged) == 1
  assert merged[0].doi == "10.1000/final"
  assert "doi:10.1101/2026.01.01.123456" in merged[0].identity_aliases()
  assert "pmid:999" in merged[0].identity_aliases()


def test_title_fallback_requires_first_author_and_year() -> None:
  original = paper(doi="", source_id="one")
  same = paper(doi="", source="arxiv", source_id="two", arxiv_id="", abstract="Richer")
  other_author = paper(
    doi="",
    source="arxiv",
    source_id="three",
    authors=("Katherine Johnson",),
  )
  other_year = paper(
    doi="",
    source="arxiv",
    source_id="four",
    created_at=datetime(2025, 1, 1, tzinfo=UTC),
    updated_at=datetime(2025, 1, 1, tzinfo=UTC),
  )

  merged = deduplicate_records([original, same, other_author, other_year])

  assert len(merged) == 3


def test_live_preprint_publication_pair_merges_across_adjacent_years() -> None:
  preprint = PaperRecord(
    source="biorxiv",
    source_id="10.1101/2024.05.22.595374",
    title=(
      "Skeletal Muscle PGC-1α Remodels Mitochondrial Phospholipidome but "
      "Does Not Alter Energy Efficiency for ATP Synthesis."
    ),
    abstract="Preprint abstract.",
    authors=("Takuya Karasawa", "Ran Hee Choi", "Cesar A Meza"),
    created_at=datetime(2024, 5, 22, tzinfo=UTC),
    updated_at=datetime(2024, 5, 22, tzinfo=UTC),
    doi="10.1101/2024.05.22.595374",
    metadata={"publication_year": 2024, "record_kind": "preprint-version"},
  )
  publication = PaperRecord(
    source="pubmed",
    source_id="40795873",
    title=preprint.title,
    abstract="Published abstract.",
    authors=("Takuya Karasawa", "Ran Hee Choi", "Cesar A Meza", "Shinya Watanabe"),
    created_at=datetime(2025, 7, 1, tzinfo=UTC),
    updated_at=datetime(2025, 7, 2, tzinfo=UTC),
    doi="10.1002/jcsm.70090",
    pmid="40795873",
    metadata={"publication_year": 2025},
  )

  merged = deduplicate_records([preprint, publication])

  assert len(merged) == 1
  assert merged[0].doi == "10.1002/jcsm.70090"
  assert merged[0].pmid == "40795873"
  assert merged[0].abstract == "Published abstract."
  assert "doi:10.1101/2024.05.22.595374" in merged[0].identity_aliases()


def test_preprint_publication_fallback_allows_two_year_indexing_lag() -> None:
  preprint = paper(
    title="Ordering molecular diversity in untargeted metabolomics via molecular community networking.",
    authors=("Elizabeth A Coler", "Alexey Melnik"),
    doi="10.1101/2024.08.02.606356",
    source_id="10.1101/2024.08.02.606356",
    metadata={"publication_year": 2024},
  )
  publication = paper(
    source="pubmed",
    source_id="999001",
    title=preprint.title,
    authors=preprint.authors,
    doi="10.1016/j.crmeth.2026.101468",
    pmid="999001",
    created_at=datetime(2026, 1, 1, tzinfo=UTC),
    updated_at=datetime(2026, 1, 1, tzinfo=UTC),
    metadata={"publication_year": 2026},
  )

  merged = deduplicate_records([publication, preprint])

  assert len(merged) == 1
  assert merged[0].doi == "10.1016/j.crmeth.2026.101468"


def test_revised_preprint_titles_do_not_choose_a_publication_by_order() -> None:
  preprint_old = paper(
    title="Original preprint title",
    abstract="Original preprint abstract.",
    metadata={"publication_year": 2022},
  )
  preprint_new = paper(
    title="Revised preprint title",
    abstract="Revised preprint abstract.",
    metadata={"publication_year": 2022},
  )
  publication_old = paper(
    source="pubmed",
    source_id="publication-old",
    title=preprint_old.title,
    abstract="First plausible publication.",
    doi="10.1000/old-title",
    pmid="1001",
    metadata={"publication_year": 2023},
  )
  publication_new = paper(
    source="pubmed",
    source_id="publication-new",
    title=preprint_new.title,
    abstract="Second plausible publication.",
    doi="10.1000/new-title",
    pmid="1002",
    metadata={"publication_year": 2024},
  )
  records = (
    preprint_old,
    preprint_new,
    publication_old,
    publication_new,
  )
  expected_ids = {
    "doi:10.1101/2026.01.01.123456",
    "doi:10.1000/old-title",
    "doi:10.1000/new-title",
  }

  for ordering in permutations(records):
    merged = deduplicate_records(ordering)
    assert {record.canonical_id for record in merged} == expected_ids


def test_research_square_fallback_prefers_version_of_record_doi() -> None:
  preprint = paper(
    source="medrxiv",
    source_id="10.21203/rs.3.rs-6819284/v1",
    title="Subtypes of Type 2 Diabetes and Prediabetes: Mortality and Excess Life Lost in South Asians.",
    authors=("Ram Jagannathan", "Dimple Kondal"),
    doi="10.21203/rs.3.rs-6819284/v1",
    metadata={"publication_year": 2025},
  )
  publication = paper(
    source="pubmed",
    source_id="999003",
    title=preprint.title,
    authors=preprint.authors,
    doi="10.2337/dc26-0043",
    pmid="999003",
    created_at=datetime(2026, 1, 1, tzinfo=UTC),
    updated_at=datetime(2026, 1, 1, tzinfo=UTC),
    metadata={"publication_year": 2026},
  )

  merged = deduplicate_records([preprint, publication])

  assert len(merged) == 1
  assert merged[0].doi == "10.2337/dc26-0043"
  assert "doi:10.21203/rs.3.rs-6819284/v1" in merged[0].identity_aliases()


def test_relaxed_fallback_does_not_merge_changed_first_author() -> None:
  preprint = paper(
    title="Glucuronidation metabolomic fingerprinting to map host-microbe metabolism.",
    authors=("Andrew Patterson", "Nina Boyle"),
    doi="10.21203/rs.3.rs-6321321/v1",
    source_id="10.21203/rs.3.rs-6321321/v1",
    metadata={"publication_year": 2025},
  )
  publication = paper(
    source="pubmed",
    source_id="999002",
    title=preprint.title,
    authors=("Nina R Boyle", "Josh J Sekela"),
    doi="10.1038/s41467-026-73398-1",
    pmid="999002",
    created_at=datetime(2026, 1, 1, tzinfo=UTC),
    updated_at=datetime(2026, 1, 1, tzinfo=UTC),
    metadata={"publication_year": 2026},
  )

  assert len(deduplicate_records([preprint, publication])) == 2


def test_title_fallback_does_not_merge_distinct_publication_dois() -> None:
  article = paper(
    source="pubmed",
    source_id="one",
    title="A design-weighted intersectional analysis.",
    authors=("F Hunter McGuire",),
    doi="10.1093/aje/kwae121",
    pmid="111",
    metadata={"publication_year": 2026},
  )
  correction = paper(
    source="pubmed",
    source_id="two",
    title=article.title,
    authors=article.authors,
    doi="10.1093/aje/kwag144",
    pmid="222",
    metadata={"publication_year": 2026},
  )

  assert len(deduplicate_records([article, correction])) == 2


def test_generic_title_never_drives_metadata_deduplication() -> None:
  first = paper(
    source="pubmed",
    source_id="one",
    title="[Not Available].",
    authors=("Ada Lovelace",),
    doi="",
    pmid="111",
    metadata={"publication_year": 2025},
  )
  second = paper(
    source="pubmed",
    source_id="two",
    title="[Not Available].",
    authors=("Ada Lovelace",),
    doi="",
    pmid="222",
    metadata={"publication_year": 2025},
  )

  assert len(deduplicate_records([first, second])) == 2


def test_adjacent_year_doi_pmid_complement_merges() -> None:
  doi_record = paper(
    source="biorxiv",
    source_id="publication-record",
    title="Associations between iron and mean kurtosis in aging.",
    authors=("Jason Langley", "Kitzia Solis"),
    doi="10.1007/s10334-026-01355-6",
    pmid="",
    metadata={"publication_year": 2026},
  )
  pubmed_record = paper(
    source="pubmed",
    source_id="40463705",
    title=doi_record.title,
    authors=doi_record.authors,
    doi="",
    pmid="40463705",
    metadata={"publication_year": 2025},
  )

  merged = deduplicate_records([doi_record, pubmed_record])

  assert len(merged) == 1
  assert merged[0].doi == "10.1007/s10334-026-01355-6"
  assert merged[0].pmid == "40463705"


def test_serialization_round_trip_and_hash_are_deterministic() -> None:
  original = paper(metadata={"provider": "fixture"}, related_ids=("pmid:123",))
  restored = PaperRecord.from_dict(original.to_dict())

  assert restored == original
  assert restored.metadata == original.metadata
  assert restored.metadata_hash == original.metadata_hash
