from __future__ import annotations

from collections import deque
from datetime import UTC, datetime
import http.client
import json
from typing import Any, Callable, Mapping

import pytest

from scripts.paperbot.records import PaperRecord
from scripts.paperbot.sources import (
  ARXIV_API,
  ARXIV_PAGE_SIZE,
  CHEMRXIV_API,
  CHEMRXIV_CROSSREF_API,
  CHEMRXIV_FALLBACK_API,
  PUBMED_EFETCH,
  PUBMED_ESEARCH,
  FetchWindow,
  HttpClient,
  HttpRequestError,
  HttpResponse,
  SourceFailure,
  SourceResult,
  fetch_all_sources,
  fetch_arxiv,
  fetch_chemrxiv,
  fetch_pubmed,
  fetch_rxiv,
  _pubmed_collect_term_ids,
  parse_arxiv_atom,
  parse_chemrxiv_item,
  parse_crossref_chemrxiv_item,
  parse_pubmed_xml,
  parse_rxiv_item,
)


PUBMED_XML = b"""<?xml version="1.0"?>
<PubmedArticleSet>
  <PubmedArticle>
    <MedlineCitation>
      <PMID>123456</PMID>
      <DateCreated><Year>2026</Year><Month>07</Month><Day>21</Day></DateCreated>
      <DateRevised><Year>2026</Year><Month>07</Month><Day>21</Day></DateRevised>
      <Article>
        <ArticleTitle>A <i>structured</i> title</ArticleTitle>
        <Abstract>
          <AbstractText Label="BACKGROUND">Earlier work.</AbstractText>
          <AbstractText Label="RESULTS">The result.</AbstractText>
        </Abstract>
        <AuthorList>
          <Author><ForeName>Ada</ForeName><LastName>Lovelace</LastName></Author>
          <Author><CollectiveName>Example Consortium</CollectiveName></Author>
        </AuthorList>
        <Journal>
          <JournalIssue><PubDate><Year>2024</Year><Month>Jul</Month><Day>20</Day></PubDate></JournalIssue>
          <Title>Journal of Fixtures</Title>
        </Journal>
        <ELocationID EIdType="doi">10.1000/FIXTURE</ELocationID>
      </Article>
    </MedlineCitation>
    <PubmedData>
      <History>
        <PubMedPubDate PubStatus="entrez">
          <Year>2026</Year><Month>07</Month><Day>21</Day>
          <Hour>12</Hour><Minute>34</Minute><Second>56</Second>
        </PubMedPubDate>
      </History>
      <ArticleIdList>
        <ArticleId IdType="pubmed">123456</ArticleId>
        <ArticleId IdType="doi">10.1000/FIXTURE</ArticleId>
        <ArticleId IdType="pmc">PMC999</ArticleId>
      </ArticleIdList>
    </PubmedData>
  </PubmedArticle>
</PubmedArticleSet>
"""


PUBMED_BOOK_XML = b"""<?xml version="1.0"?>
<PubmedArticleSet>
  <PubmedBookArticle>
    <BookDocument>
      <PMID>654321</PMID>
      <ArticleIdList>
        <ArticleId IdType="doi">10.1000/BOOK-CHAPTER</ArticleId>
      </ArticleIdList>
      <Book>
        <BookTitle>Fixture Methods</BookTitle>
        <PubDate><Year>2022</Year></PubDate>
      </Book>
      <ArticleTitle>A book chapter in PubMed</ArticleTitle>
      <AuthorList>
        <Author><ForeName>Grace</ForeName><LastName>Hopper</LastName></Author>
      </AuthorList>
      <Abstract><AbstractText>A complete chapter abstract.</AbstractText></Abstract>
      <DateRevised><Year>2026</Year><Month>07</Month><Day>21</Day></DateRevised>
    </BookDocument>
    <PubmedBookData>
      <History>
        <PubMedPubDate PubStatus="entrez">
          <Year>2026</Year><Month>07</Month><Day>20</Day>
          <Hour>03</Hour><Minute>04</Minute><Second>05</Second>
        </PubMedPubDate>
      </History>
      <ArticleIdList><ArticleId IdType="pubmed">654321</ArticleId></ArticleIdList>
    </PubmedBookData>
  </PubmedBookArticle>
</PubmedArticleSet>
"""


def arxiv_xml(
  identifier: str = "2401.12345v2", *, total: int = 1, updated: str = "2026-07-21T12:00:00Z"
) -> bytes:
  return f"""<?xml version="1.0"?>
  <feed xmlns="http://www.w3.org/2005/Atom"
        xmlns:opensearch="http://a9.com/-/spec/opensearch/1.1/"
        xmlns:arxiv="http://arxiv.org/schemas/atom">
    <opensearch:totalResults>{total}</opensearch:totalResults>
    <entry>
      <id>https://arxiv.org/abs/{identifier}</id>
      <updated>{updated}</updated>
      <published>2026-07-20T11:00:00Z</published>
      <title>Fixture arXiv paper {identifier}</title>
      <summary>A complete abstract from the Atom feed.</summary>
      <author><name>Ada Lovelace</name></author>
      <category term="q-bio.BM"/>
      <arxiv:primary_category term="q-bio.BM"/>
      <arxiv:doi>10.1000/{identifier}</arxiv:doi>
    </entry>
  </feed>""".encode()


def pubmed_xml_at(pmid: str, entered_at: datetime) -> bytes:
  """Return one minimal PubMed article with an exact Entrez timestamp."""

  entered_at = entered_at.astimezone(UTC)
  return f"""<?xml version="1.0"?>
  <PubmedArticleSet>
    <PubmedArticle>
      <MedlineCitation>
        <PMID>{pmid}</PMID>
        <DateCreated>
          <Year>{entered_at.year}</Year><Month>{entered_at.month:02d}</Month>
          <Day>{entered_at.day:02d}</Day>
        </DateCreated>
        <Article>
          <ArticleTitle>Boundary fixture {pmid}</ArticleTitle>
          <Abstract><AbstractText>A complete boundary abstract.</AbstractText></Abstract>
          <Journal>
            <JournalIssue><PubDate><Year>2026</Year></PubDate></JournalIssue>
            <Title>Journal of Boundaries</Title>
          </Journal>
        </Article>
      </MedlineCitation>
      <PubmedData>
        <History>
          <PubMedPubDate PubStatus="entrez">
            <Year>{entered_at.year}</Year><Month>{entered_at.month:02d}</Month>
            <Day>{entered_at.day:02d}</Day><Hour>{entered_at.hour:02d}</Hour>
            <Minute>{entered_at.minute:02d}</Minute><Second>{entered_at.second:02d}</Second>
          </PubMedPubDate>
        </History>
        <ArticleIdList><ArticleId IdType="pubmed">{pmid}</ArticleId></ArticleIdList>
      </PubmedData>
    </PubmedArticle>
  </PubmedArticleSet>""".encode()


def window() -> FetchWindow:
  return FetchWindow.ending_at(datetime(2026, 7, 22, tzinfo=UTC))


class RoutingClient:
  def __init__(
    self,
    *,
    json_route: Callable[[str, Mapping[str, Any]], Any] | None = None,
    bytes_route: Callable[[str, Mapping[str, Any]], bytes] | None = None,
  ):
    self.json_route = json_route
    self.bytes_route = bytes_route
    self.calls: list[tuple[str, str, Mapping[str, Any], float]] = []

  def get_json(
    self,
    url: str,
    *,
    params: Mapping[str, Any] | None = None,
    headers: Mapping[str, str] | None = None,
    min_interval: float = 0.0,
  ) -> Any:
    self.calls.append(("json", url, params or {}, min_interval))
    assert self.json_route is not None
    return self.json_route(url, params or {})

  def get_bytes(
    self,
    url: str,
    *,
    params: Mapping[str, Any] | None = None,
    headers: Mapping[str, str] | None = None,
    min_interval: float = 0.0,
  ) -> bytes:
    self.calls.append(("bytes", url, params or {}, min_interval))
    assert self.bytes_route is not None
    return self.bytes_route(url, params or {})


def test_fetch_window_has_24_hour_tranche_and_72_hour_overlap() -> None:
  value = window()

  assert value.logical_since == datetime(2026, 7, 21, tzinfo=UTC)
  assert value.query_since == datetime(2026, 7, 19, tzinfo=UTC)
  assert value.until == datetime(2026, 7, 22, tzinfo=UTC)
  assert value.query_end_date.isoformat() == "2026-07-21"
  assert value.includes_query_timestamp("2026-07-20T12:00:00Z")
  assert value.includes_logical_timestamp("2026-07-21T00:00:00Z")
  assert not value.includes_logical_timestamp("2026-07-20T23:59:59Z")
  assert not value.includes_logical_timestamp("2026-07-22T00:00:00Z")
  assert not value.includes_query_timestamp("2026-07-22T00:00:00Z")
  assert not value.includes_query_date("2026-07-22")
  assert not value.includes_query_timestamp("2026-07-18T23:59:59Z")

  manual = FetchWindow.between(
    datetime(2026, 7, 1, tzinfo=UTC), datetime(2026, 7, 10, tzinfo=UTC)
  )
  assert manual.query_since == manual.logical_since


def test_parse_pubmed_xml_preserves_sections_identifiers_and_revision_date() -> None:
  records = parse_pubmed_xml(PUBMED_XML)

  assert len(records) == 1
  record = records[0]
  assert record.title == "A structured title"
  assert record.abstract == "BACKGROUND: Earlier work. RESULTS: The result."
  assert record.authors == ("Ada Lovelace", "Example Consortium")
  assert record.doi == "10.1000/fixture"
  assert record.pmid == "123456"
  assert record.updated_at == datetime(2026, 7, 21, tzinfo=UTC)
  assert record.year == 2024
  assert record.metadata["publication_date"] == "2024-07-20"
  assert record.created_at == datetime(2026, 7, 21, 12, 34, 56, tzinfo=UTC)
  assert record.metadata["timestamp_precision"] == "second"
  assert "pmc:pmc999" in record.related_ids


def test_parse_pubmed_book_article_with_abstract() -> None:
  records = parse_pubmed_xml(PUBMED_BOOK_XML)

  assert len(records) == 1
  record = records[0]
  assert record.pmid == "654321"
  assert record.doi == "10.1000/book-chapter"
  assert record.title == "A book chapter in PubMed"
  assert record.abstract == "A complete chapter abstract."
  assert record.authors == ("Grace Hopper",)
  assert record.venue == "Fixture Methods"
  assert record.year == 2022
  assert record.created_at == datetime(2026, 7, 20, 3, 4, 5, tzinfo=UTC)
  assert record.metadata["timestamp_precision"] == "second"
  assert record.metadata["publication_date"] == "2022"


def test_fetch_pubmed_queries_only_crdt_for_the_logical_window() -> None:
  def get_json(url: str, params: Mapping[str, Any]) -> Any:
    assert url == PUBMED_ESEARCH
    term = str(params["term"])
    assert "[CRDT]" in term
    assert "[LR]" not in term
    if "2026/07/21" in str(params["term"]):
      return {"esearchresult": {"count": "1", "idlist": ["123456"]}}
    return {"esearchresult": {"count": "0", "idlist": []}}

  client = RoutingClient(
    json_route=get_json,
    bytes_route=lambda url, _params: PUBMED_XML if url == PUBMED_EFETCH else b"",
  )

  result = fetch_pubmed(window(), client, contact_email="reader@example.test")

  assert result.ok
  assert len(result.records) == 1
  assert len([call for call in client.calls if call[1] == PUBMED_ESEARCH]) == 1
  assert len([call for call in client.calls if call[1] == PUBMED_EFETCH]) == 1
  assert all(call[3] == 0.34 for call in client.calls)


@pytest.mark.parametrize(
  ("entered_at", "included"),
  [
    (datetime(2026, 7, 21, 18, 0, 0, tzinfo=UTC), True),
    (datetime(2026, 7, 22, 17, 59, 59, tzinfo=UTC), True),
    (datetime(2026, 7, 21, 17, 59, 59, tzinfo=UTC), False),
    (datetime(2026, 7, 22, 18, 0, 0, tzinfo=UTC), False),
  ],
)
def test_fetch_pubmed_filters_new_records_by_exact_half_open_window(
  entered_at: datetime, included: bool
) -> None:
  exact_window = FetchWindow.between(
    datetime(2026, 7, 21, 18, tzinfo=UTC),
    datetime(2026, 7, 22, 18, tzinfo=UTC),
  )

  def get_json(_url: str, _params: Mapping[str, Any]) -> Any:
    return {"esearchresult": {"count": "1", "idlist": ["700001"]}}

  client = RoutingClient(
    json_route=get_json,
    bytes_route=lambda _url, _params: pubmed_xml_at("700001", entered_at),
  )
  result = fetch_pubmed(exact_window, client)

  assert result.ok
  assert bool(result.records) is included
  assert result.skipped == (0 if included else 1)
  search_terms = [
    str(call[2]["term"]) for call in client.calls if call[1] == PUBMED_ESEARCH
  ]
  assert search_terms == [
    '"2026/07/21"[CRDT] AND hasabstract',
    '"2026/07/22"[CRDT] AND hasabstract',
  ]


def test_fetch_pubmed_refetches_known_pmids_outside_discovery_window() -> None:
  def get_json(_url: str, _params: Mapping[str, Any]) -> Any:
    return {"esearchresult": {"count": "0", "idlist": []}}

  client = RoutingClient(
    json_route=get_json,
    bytes_route=lambda _url, _params: pubmed_xml_at(
      "700002", datetime(2020, 1, 2, 3, 4, 5, tzinfo=UTC)
    ),
  )
  result = fetch_pubmed(
    window(), client, known_pubmed_ids={"700002", "not-a-pmid"}
  )

  assert result.ok
  assert [record.pmid for record in result.records] == ["700002"]
  fetch_call = next(call for call in client.calls if call[1] == PUBMED_EFETCH)
  assert fetch_call[2]["id"] == "700002"


def test_pubmed_partitions_uid_space_beyond_the_9999_result_cap() -> None:
  lower_ids = [str(value) for value in range(1, 5_001)]
  upper_ids = [str(value) for value in range(50_000_001, 50_005_001)]

  def get_json(url: str, params: Mapping[str, Any]) -> Any:
    assert url == PUBMED_ESEARCH
    term = str(params["term"])
    if "[UID]" not in term:
      return {"esearchresult": {"count": "10000", "idlist": lower_ids}}
    uid_range = term.rsplit(" AND ", 1)[-1]
    if uid_range == "1:99999999[UID]":
      return {"esearchresult": {"count": "10000", "idlist": lower_ids}}
    if uid_range == "1:50000000[UID]":
      return {"esearchresult": {"count": "5000", "idlist": lower_ids}}
    if uid_range == "50000001:99999999[UID]":
      return {"esearchresult": {"count": "5000", "idlist": upper_ids}}
    raise AssertionError(f"unexpected PubMed partition: {term}")

  client = RoutingClient(json_route=get_json)
  identifiers = _pubmed_collect_term_ids(
    client,
    {"db": "pubmed"},
    base_term='"2026/07/20"[CRDT] AND hasabstract',
    page_size=9_999,
    interval=0.34,
  )

  assert len(identifiers) == 10_000
  assert identifiers == set(lower_ids) | set(upper_ids)
  assert len(client.calls) == 4


def test_parse_and_paginate_arxiv_by_last_updated_date() -> None:
  parsed, total = parse_arxiv_atom(arxiv_xml(total=2))
  assert total == 2
  assert parsed[0].arxiv_id == "2401.12345"
  assert parsed[0].version == "2"
  assert parsed[0].categories == ("q-bio.BM",)

  pages = deque([arxiv_xml("2401.12345v2", total=2), arxiv_xml("2401.54321v1", total=2)])

  def get_bytes(url: str, params: Mapping[str, Any]) -> bytes:
    assert url == ARXIV_API
    query = str(params["search_query"])
    assert "lastUpdatedDate:[202607190000 TO 202607212359]" in query
    assert all(category in query for category in ("q-bio*", "cond-mat*", "stat.*"))
    return pages.popleft()

  client = RoutingClient(bytes_route=get_bytes)
  # The provider may return fewer entries than requested before the final page;
  # reported total, not page length, controls exhaustion.
  result = fetch_arxiv(window(), client, page_size=5)

  assert result.ok
  assert len(result.records) == 2
  assert [call[2]["start"] for call in client.calls] == [0, 1]
  assert all(call[3] == 3.1 for call in client.calls)


def test_arxiv_uses_a_larger_bounded_default_page() -> None:
  client = RoutingClient(bytes_route=lambda _url, _params: arxiv_xml())

  result = fetch_arxiv(window(), client)

  assert result.ok
  assert client.calls[0][2]["max_results"] == ARXIV_PAGE_SIZE
  assert ARXIV_PAGE_SIZE == 500


@pytest.mark.parametrize("server", ["biorxiv", "medrxiv"])
def test_rxiv_paginates_versions_and_links_version_of_record(server: str) -> None:
  details = [
    {
      "doi": "10.1101/2026.01.01.123456",
      "title": "A preprint",
      "abstract": "Version one.",
      "authors": "Ada Lovelace; Grace Hopper",
      "date": "2026-07-20",
      "version": "1",
      "category": "bioinformatics",
      "license": "CC BY",
    },
    {
      "doi": "10.1101/2026.01.01.123456",
      "title": "A preprint",
      "abstract": "Version two.",
      "authors": "Ada Lovelace; Grace Hopper",
      "date": "2026-07-21",
      "version": "2",
      "category": "bioinformatics",
      "license": "CC BY",
    },
  ]
  publication = {
    "preprint_doi": "10.1101/2026.01.01.123456",
    "published_doi": "10.1000/final",
    "preprint_title": "A preprint",
    "preprint_abstract": "Published abstract.",
    "preprint_authors": "Ada Lovelace; Grace Hopper",
    "preprint_date": "2026-07-20",
    "published_date": "2026-07-21",
    "published_journal": "Journal of Fixtures",
  }

  direct = parse_rxiv_item(publication, server, publication=True)
  assert direct.doi == "10.1000/final"
  assert direct.source_id == "10.1101/2026.01.01.123456"
  assert direct.version == ""
  assert direct.year == 2026
  assert direct.metadata["preprint_date"] == "2026-07-20"
  assert direct.metadata["publication_date"] == "2026-07-21"
  assert direct.updated_at == datetime(2026, 7, 21, tzinfo=UTC)
  assert "doi:10.1101/2026.01.01.123456" in direct.related_ids

  def get_json(url: str, _params: Mapping[str, Any]) -> Any:
    if "/details/" in url:
      cursor = int(url.rsplit("/", 1)[-1])
      return {
        "collection": [details[cursor]],
        "messages": [{"total": "2", "cursor": cursor}],
      }
    return {"collection": [publication], "messages": [{"total": "1"}]}

  result = fetch_rxiv(window(), RoutingClient(json_route=get_json), server=server)

  assert result.ok
  assert len(result.records) == 1
  record = result.records[0]
  assert record.doi == "10.1000/final"
  assert record.abstract == "Published abstract."
  assert record.version == ""
  assert record.metadata["publication_date"] == "2026-07-21"
  assert "doi:10.1101/2026.01.01.123456" in record.identity_aliases()


def test_chemrxiv_parser_tracks_version_family_and_vor() -> None:
  record = parse_chemrxiv_item(
    {
      "item": {
        "id": "new-id",
        "doi": "10.26434/chemrxiv-2026-abcd-v2",
        "title": "Chemistry fixture",
        "abstract": "A chemistry abstract.",
        "authors": [{"firstName": "Ada", "lastName": "Lovelace"}],
        "categories": [{"name": "Biological Chemistry"}],
        "submittedDate": "2026-07-20T10:00:00Z",
        "statusDate": "2026-07-21T10:00:00Z",
        "version": "2",
        "versionRefs": [
          {"version": "1", "itemId": "old-id"},
          {"version": "2", "itemId": "new-id"},
        ],
        "vor": {"vorDoi": "10.1000/chem-final"},
        "license": {"name": "CC BY"},
        "origin": "ChemRxiv",
      }
    }
  )

  assert record.authors == ("Ada Lovelace",)
  assert record.canonical_id == "doi:10.1000/chem-final"
  assert "chemrxiv:old-id" in record.related_ids
  assert "doi:10.26434/chemrxiv-2026-abcd-v2" in record.related_ids
  assert "doi:10.26434/chemrxiv-2026-abcd" in record.identity_aliases()


def crossref_chemrxiv_item() -> dict[str, Any]:
  return {
    "DOI": "10.26434/chemrxiv.15006393/v1",
    "title": ["Chemistry fixture"],
    "abstract": "<jats:p>A chemistry abstract.</jats:p>",
    "author": [{"given": "Ada", "family": "Lovelace"}],
    "posted": {"date-parts": [[2026, 7, 20]]},
    "deposited": {"date-time": "2026-07-21T10:00:00Z"},
    "indexed": {"date-time": "2026-07-21T11:00:00Z"},
    "resource": {
      "primary": {"URL": "https://chemrxiv.org/doi/10.26434/chemrxiv.15006393/v1"}
    },
    "license": [{"URL": "https://creativecommons.org/licenses/by/4.0/"}],
    "type": "posted-content",
  }


def test_crossref_chemrxiv_parser_supports_slash_versions() -> None:
  record = parse_crossref_chemrxiv_item(crossref_chemrxiv_item())

  assert record.source_id == "10.26434/chemrxiv.15006393/v1"
  assert record.canonical_id == "doi:10.26434/chemrxiv.15006393"
  assert record.version == "1"
  assert record.abstract == "A chemistry abstract."
  assert record.authors == ("Ada Lovelace",)


def test_chemrxiv_falls_back_to_paginated_crossref_updates() -> None:
  crossref_item = crossref_chemrxiv_item()
  revised_item = {
    **crossref_item,
    "DOI": "10.26434/chemrxiv.15006393/v2",
    "abstract": "<jats:p>A revised chemistry abstract.</jats:p>",
    "deposited": {"date-time": "2026-07-21T12:00:00Z"},
  }

  def get_json(url: str, params: Mapping[str, Any]) -> Any:
    if url == CHEMRXIV_API:
      raise HttpRequestError("blocked", status=403)
    assert url == CHEMRXIV_CROSSREF_API == CHEMRXIV_FALLBACK_API
    item = crossref_item if params["cursor"] == "*" else revised_item
    return {
      "message": {
        "total-results": 2,
        "items": [item],
        "next-cursor": "page-2",
      }
    }

  client = RoutingClient(json_route=get_json)
  result = fetch_chemrxiv(window(), client, page_size=500)

  assert result.ok
  assert [record.source_id for record in result.records] == [
    "10.26434/chemrxiv.15006393/v2"
  ]
  fallback_calls = [call for call in client.calls if call[1] == CHEMRXIV_FALLBACK_API]
  fallback_call = fallback_calls[0]
  assert [call[2]["cursor"] for call in fallback_calls] == ["*", "page-2"]
  assert fallback_call[2]["rows"] == 1_000
  assert fallback_call[2]["cursor"] == "*"
  assert "prefix:10.26434" in str(fallback_call[2]["filter"])
  assert "until-update-date:2026-07-21" in str(fallback_call[2]["filter"])
  primary_call = next(call for call in client.calls if call[1] == CHEMRXIV_API)
  assert primary_call[2]["limit"] == 50


def test_chemrxiv_fallback_skips_permanently_missing_hydration_records() -> None:
  missing_abstract = {
    **crossref_chemrxiv_item(),
    "DOI": "10.26434/chemrxiv.99999999/v1",
    "abstract": "",
  }

  def get_json(url: str, _params: Mapping[str, Any]) -> Any:
    if url == CHEMRXIV_API:
      raise HttpRequestError("retired endpoint", status=404)
    if url == CHEMRXIV_CROSSREF_API:
      return {
        "message": {
          "total-results": 2,
          "items": [crossref_chemrxiv_item(), missing_abstract],
        }
      }
    raise HttpRequestError("legacy version unavailable", status=404)

  result = fetch_chemrxiv(window(), RoutingClient(json_route=get_json))

  assert result.ok
  assert [record.source_id for record in result.records] == [
    "10.26434/chemrxiv.15006393/v1"
  ]
  assert result.skipped == 1
  assert result.errors == []


def test_chemrxiv_fallback_does_not_hide_crossref_feed_failure() -> None:
  def get_json(url: str, _params: Mapping[str, Any]) -> Any:
    if url == CHEMRXIV_API:
      raise HttpRequestError("retired endpoint", status=404)
    raise HttpRequestError("Crossref unavailable", status=503, retryable=True)

  result = fetch_chemrxiv(window(), RoutingClient(json_route=get_json))

  assert not result.ok
  assert [failure.status for failure in result.errors] == [404, 503]
  assert result.errors[-1].retryable


def test_chemrxiv_fallback_reports_transient_hydration_failure() -> None:
  missing_abstract = {**crossref_chemrxiv_item(), "abstract": ""}

  def get_json(url: str, _params: Mapping[str, Any]) -> Any:
    if url == CHEMRXIV_API:
      raise HttpRequestError("retired endpoint", status=404)
    if url == CHEMRXIV_CROSSREF_API:
      return {
        "message": {"total-results": 1, "items": [missing_abstract]}
      }
    raise HttpRequestError("detail temporarily unavailable", status=503, retryable=True)

  result = fetch_chemrxiv(window(), RoutingClient(json_route=get_json))

  assert not result.ok
  assert [failure.status for failure in result.errors] == [404, 503]
  assert result.errors[-1].operation == "parse/hydrate Crossref record"


def test_http_client_exposes_retry_and_rate_limit_hooks() -> None:
  responses = deque(
    [
      HttpResponse(429, {"Retry-After": "0"}, b""),
      HttpResponse(200, {}, b'{"ok": true}'),
    ]
  )
  sleeps: list[float] = []
  ticks = iter([0.0, 0.0, 1.0, 1.0])
  client = HttpClient(
    user_agent="fixture",
    attempts=2,
    transport=lambda _request, _timeout: responses.popleft(),
    sleep=sleeps.append,
    monotonic=lambda: next(ticks),
  )

  assert client.get_json("https://example.test/feed", min_interval=0.5) == {"ok": True}
  assert sleeps


def test_http_client_retries_incomplete_response_body() -> None:
  responses: deque[HttpResponse | Exception] = deque(
    [
      http.client.IncompleteRead(b'{"ok":', 5),
      HttpResponse(200, {}, b'{"ok": true}'),
    ]
  )
  sleeps: list[float] = []

  def transport(_request: Any, _timeout: float) -> HttpResponse:
    response = responses.popleft()
    if isinstance(response, Exception):
      raise response
    return response

  client = HttpClient(
    user_agent="fixture", attempts=2, transport=transport, sleep=sleeps.append
  )

  assert client.get_json("https://example.test/feed") == {"ok": True}
  assert sleeps == [1.0]


def test_http_client_retries_invalid_json_response() -> None:
  responses = deque(
    [
      HttpResponse(200, {}, b"temporarily unavailable"),
      HttpResponse(200, {}, b'{"ok": true}'),
    ]
  )
  sleeps: list[float] = []
  client = HttpClient(
    user_agent="fixture",
    attempts=2,
    transport=lambda _request, _timeout: responses.popleft(),
    sleep=sleeps.append,
  )

  assert client.get_json("https://example.test/feed") == {"ok": True}
  assert sleeps == [1.0]


def test_pubmed_api_key_is_redacted_from_feed_errors_and_reports() -> None:
  secret = "ncbi-secret-value"
  requested_urls: list[str] = []

  def fail(request: Any, _timeout: float) -> HttpResponse:
    requested_urls.append(request.full_url)
    return HttpResponse(500, {}, b"")

  client = HttpClient(
    user_agent="fixture",
    attempts=1,
    transport=fail,
    sleep=lambda _delay: None,
    monotonic=lambda: 0.0,
  )
  result = fetch_pubmed(window(), client, api_key=secret)
  serialized_report_errors = json.dumps(
    [
      {
        "source": failure.source,
        "operation": failure.operation,
        "message": failure.message,
      }
      for failure in result.errors
    ]
  )

  assert requested_urls and any(secret in url for url in requested_urls)
  assert result.errors
  assert secret not in serialized_report_errors
  assert "api_key=REDACTED" in serialized_report_errors


def test_http_error_redacts_common_query_credential_names() -> None:
  secrets = {
    "api_key": "api-secret",
    "token": "token-secret",
    "access_token": "access-secret",
    "client_secret": "client-secret",
  }
  client = HttpClient(
    user_agent="fixture",
    attempts=1,
    transport=lambda _request, _timeout: HttpResponse(403, {}, b""),
  )

  with pytest.raises(HttpRequestError) as captured:
    client.get_bytes("https://example.test/feed", params={**secrets, "page": "2"})

  message = str(captured.value)
  assert all(value not in message for value in secrets.values())
  assert all(f"{key}=REDACTED" in message for key in secrets)
  assert "page=2" in message


def test_fetch_all_sources_isolates_failure_and_reports_progress(capsys: Any) -> None:
  record = PaperRecord(
    source="arxiv",
    source_id="2401.12345",
    title="One paper",
    abstract="One abstract.",
    authors=("Ada Lovelace",),
    created_at="2026-07-20T00:00:00Z",
    updated_at="2026-07-21T00:00:00Z",
    arxiv_id="2401.12345",
  )

  def good(_window: FetchWindow, _client: Any) -> SourceResult:
    return SourceResult("good", records=[record, record])

  def bad(_window: FetchWindow, _client: Any) -> SourceResult:
    raise RuntimeError("provider unavailable")

  report = fetch_all_sources(
    window(), client=object(), fetchers={"good": good, "bad": bad}  # type: ignore[arg-type]
  )

  assert len(report.records) == 1
  assert report.source_counts == {"good": 2, "bad": 0}
  assert len(report.errors) == 1
  assert report.errors[0].source == "bad"
  assert "provider unavailable" in report.errors[0].message
  assert capsys.readouterr().out.splitlines() == [
    "paperbot: fetching good",
    "paperbot: completed good: 2 records, 0 errors",
    "paperbot: fetching bad",
    "paperbot: completed bad: 0 records, 1 errors",
  ]


def test_fetch_all_sources_retries_only_transient_provider_failures() -> None:
  first = PaperRecord(
    source="arxiv",
    source_id="2401.12345",
    title="First paper",
    abstract="First abstract.",
    authors=("Ada Lovelace",),
    created_at="2026-07-20T00:00:00Z",
    updated_at="2026-07-21T00:00:00Z",
    arxiv_id="2401.12345",
  )
  second = PaperRecord(
    source="arxiv",
    source_id="2401.54321",
    title="Second paper",
    abstract="Second abstract.",
    authors=("Grace Hopper",),
    created_at="2026-07-20T00:00:00Z",
    updated_at="2026-07-21T00:00:00Z",
    arxiv_id="2401.54321",
  )
  transient_attempts = deque(
    [
      SourceResult(
        "transient",
        records=[first],
        errors=[SourceFailure("transient", "page at 1", "timeout", retryable=True)],
      ),
      SourceResult("transient", records=[first, second]),
    ]
  )
  calls = {"stable": 0, "transient": 0}
  sleeps: list[float] = []

  def stable(_window: FetchWindow, _client: Any) -> SourceResult:
    calls["stable"] += 1
    return SourceResult("stable", records=[first])

  def transient(_window: FetchWindow, _client: Any) -> SourceResult:
    calls["transient"] += 1
    return transient_attempts.popleft()

  report = fetch_all_sources(
    window(),
    client=object(),  # type: ignore[arg-type]
    fetchers={"stable": stable, "transient": transient},
    provider_retry_delays=(3_600.0,),
    sleep=sleeps.append,
  )

  assert report.ok
  assert len(report.records) == 2
  assert report.source_counts == {"stable": 1, "transient": 2}
  assert calls == {"stable": 1, "transient": 2}
  assert sleeps == [3_600.0]


def test_fetch_all_sources_passes_known_pubmed_ids(monkeypatch: Any) -> None:
  captured: dict[str, Any] = {}

  def fake_pubmed(
    _window: FetchWindow,
    _client: Any,
    **kwargs: Any,
  ) -> SourceResult:
    captured.update(kwargs)
    return SourceResult("pubmed")

  def fake_rxiv(
    _window: FetchWindow, _client: Any, *, server: str
  ) -> SourceResult:
    return SourceResult(server)

  monkeypatch.setattr("scripts.paperbot.sources.fetch_pubmed", fake_pubmed)
  monkeypatch.setattr(
    "scripts.paperbot.sources.fetch_arxiv",
    lambda _window, _client: SourceResult("arxiv"),
  )
  monkeypatch.setattr("scripts.paperbot.sources.fetch_rxiv", fake_rxiv)
  monkeypatch.setattr(
    "scripts.paperbot.sources.fetch_chemrxiv",
    lambda _window, _client: SourceResult("chemrxiv"),
  )

  report = fetch_all_sources(
    window(), client=object(), known_pubmed_ids=("123456", "654321")  # type: ignore[arg-type]
  )

  assert report.ok
  assert tuple(captured["known_pubmed_ids"]) == ("123456", "654321")


def test_invalid_fetch_window_is_rejected() -> None:
  with pytest.raises(ValueError, match="recovery_hours"):
    FetchWindow.ending_at(datetime(2026, 7, 22, tzinfo=UTC), recovery_hours=24)
