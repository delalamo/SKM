from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.paperbot.enrichment import (
  AbstractResolver,
  MetadataHTMLParser,
  extract_arxiv_id,
  normalize_abstract,
)


class EnrichmentTests(unittest.TestCase):
  def test_extracts_bare_versionless_arxiv_eprint(self) -> None:
    self.assertEqual(extract_arxiv_id("2405.09673v2"), "2405.09673")

  def test_normalize_removes_markup_and_competing_interest_tail(self) -> None:
    value = "<jats:p>A useful abstract.</jats:p> Competing Interest Statement: none"
    self.assertEqual(normalize_abstract(value), "A useful abstract.")

  def test_html_metadata_prefers_citation_abstract(self) -> None:
    parser = MetadataHTMLParser()
    parser.feed('<meta name="citation_abstract" content="A sufficiently long abstract with more than twenty words for a reliable metadata test that describes a complete scientific result and conclusion.">')
    self.assertIn("citation_abstract", parser.values)

  def test_existing_abstract_requires_no_network(self) -> None:
    with tempfile.TemporaryDirectory() as directory:
      resolver = AbstractResolver(
        cache_path=Path(directory) / "cache.json",
        request=lambda _url, _headers: self.fail("network should not be used"),
      )
      result = resolver.resolve({"abstract": "An existing abstract", "url": "https://example.test"})
      self.assertIsNotNone(result)
      self.assertEqual(result.source, "bibliography")

  def test_openrxiv_native_metadata(self) -> None:
    payload = {
      "collection": [
        {"abstract": "<p>A native preprint abstract.</p>", "license": "cc_by"}
      ]
    }
    requested: list[str] = []

    def request(url: str, _headers: dict[str, str]) -> bytes:
      requested.append(url)
      return json.dumps(payload).encode()

    with tempfile.TemporaryDirectory() as directory:
      resolver = AbstractResolver(
        cache_path=Path(directory) / "cache.json",
        request=request,
      )
      result = resolver.openrxiv("10.1101/2025.01.01.123456", "biorxiv")
      self.assertIsNotNone(result)
      self.assertEqual(result.text, "A native preprint abstract.")
      self.assertEqual(result.source, "biorxiv")
      self.assertTrue(requested[0].endswith("/na/json"))

  def test_chemrxiv_native_metadata_envelope(self) -> None:
    payload = {
      "item": {
        "abstract": "A ChemRxiv abstract from the public API.",
        "license": {"name": "CC BY 4.0"},
      }
    }
    requested: list[str] = []

    def request(url: str, _headers: dict[str, str]) -> bytes:
      requested.append(url)
      return json.dumps(payload).encode()

    with tempfile.TemporaryDirectory() as directory:
      resolver = AbstractResolver(
        cache_path=Path(directory) / "cache.json",
        request=request,
      )
      result = resolver.chemrxiv("10.26434/chemrxiv-2025-example")
      self.assertIsNotNone(result)
      self.assertEqual(result.source, "chemrxiv")
      self.assertEqual(result.license, "CC BY 4.0")
      self.assertIn("/engage/coe/public-api/", requested[0])

  def test_transient_provider_failure_falls_through_to_next_resolver(self) -> None:
    def request(url: str, _headers: dict[str, str]) -> bytes:
      if "europepmc" in url:
        raise RuntimeError("temporary upstream failure")
      return json.dumps(
        {"message": {"abstract": "<jats:p>A Crossref fallback abstract.</jats:p>"}}
      ).encode()

    with tempfile.TemporaryDirectory() as directory:
      resolver = AbstractResolver(
        cache_path=Path(directory) / "cache.json",
        request=request,
      )
      result = resolver.resolve({"doi": "10.1234/fallback"})

      self.assertIsNotNone(result)
      self.assertEqual(result.source, "crossref")
      self.assertEqual(result.text, "A Crossref fallback abstract.")

  def test_arxiv_title_fallback_requires_exact_title_and_first_author(self) -> None:
    payload = b"""
      <li class="arxiv-result">
        <a href="https://arxiv.org/abs/2405.09673">paper</a>
        <p class="title is-5"><span>LoRA</span> Learns Less and Forgets Less</p>
        <p class="authors">Authors: <a>Dan Biderman</a></p>
        <p class="abstract"><span class="abstract-full">A complete exact-title
        abstract with enough scientific content for the metadata resolver.</span></p>
      </li>
    """
    with tempfile.TemporaryDirectory() as directory:
      resolver = AbstractResolver(
        cache_path=Path(directory) / "cache.json",
        request=lambda _url, _headers: payload,
      )
      result = resolver.arxiv_title(
        "LoRA Learns Less and Forgets Less", "Biderman, Dan and Example, Ada"
      )
      mismatch = resolver.arxiv_title("A different title", "Biderman, Dan")

      self.assertIsNotNone(result)
      self.assertEqual(result.source, "arxiv-title")
      self.assertIsNone(mismatch)

  def test_pubmed_direct_fallback_parses_structured_abstract(self) -> None:
    search = json.dumps({"esearchresult": {"idlist": ["123"]}}).encode()
    article = b"""<PubmedArticleSet><PubmedArticle><MedlineCitation><Article>
      <Abstract><AbstractText Label="RESULTS">A direct PubMed abstract.</AbstractText>
      </Abstract></Article></MedlineCitation></PubmedArticle></PubmedArticleSet>"""

    def request(url: str, _headers: dict[str, str]) -> bytes:
      return search if "esearch.fcgi" in url else article

    with tempfile.TemporaryDirectory() as directory:
      resolver = AbstractResolver(
        cache_path=Path(directory) / "cache.json", request=request
      )
      result = resolver.pubmed("10.1234/example")

      self.assertIsNotNone(result)
      self.assertEqual(result.source, "pubmed")
      self.assertEqual(result.text, "RESULTS: A direct PubMed abstract.")

  def test_structured_proceedings_heading_is_an_abstract(self) -> None:
    payload = (
      b"<html><h4>Abstract</h4><p>This proceedings abstract contains more than "
      b"twenty words and describes the method, experiments, findings, limitations, "
      b"and scientific conclusions in a complete paragraph for readers.</p></html>"
    )
    with tempfile.TemporaryDirectory() as directory:
      resolver = AbstractResolver(
        cache_path=Path(directory) / "cache.json",
        request=lambda _url, _headers: payload,
      )
      result = resolver.html_metadata("https://proceedings.example.test/paper")

      self.assertIsNotNone(result)
      self.assertEqual(result.source, "structured-html")

  def test_direct_provider_page_precedes_optional_arxiv_title_search(self) -> None:
    payload = (
      b"<html><h4>Abstract</h4><p>This direct provider abstract contains more "
      b"than twenty words and should be accepted before attempting any optional "
      b"title search against a rate-limited secondary scholarly service.</p></html>"
    )

    def request(url: str, _headers: dict[str, str]) -> bytes:
      if "arxiv.org/search" in url:
        self.fail("the arXiv fallback should not run after a direct match")
      return payload

    with tempfile.TemporaryDirectory() as directory:
      resolver = AbstractResolver(
        cache_path=Path(directory) / "cache.json", request=request
      )
      result = resolver.resolve(
        {
          "title": "A proceedings paper",
          "url": "https://proceedings.example.test/paper",
        }
      )

      self.assertIsNotNone(result)
      self.assertEqual(result.source, "structured-html")

  def test_privileged_pr_mode_does_not_fetch_candidate_supplied_urls(self) -> None:
    with tempfile.TemporaryDirectory() as directory:
      resolver = AbstractResolver(
        cache_path=Path(directory) / "cache.json",
        request=lambda _url, _headers: self.fail(
          "candidate-supplied URL must not be fetched"
        ),
        allow_arbitrary_html=False,
      )
      result = resolver.resolve(
        {
          "url": "http://127.0.0.1/private-runner-service",
        }
      )
      self.assertIsNone(result)


if __name__ == "__main__":
  unittest.main()
