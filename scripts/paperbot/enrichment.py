from __future__ import annotations

import html
import hashlib
import json
import os
import re
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path
from typing import Any, Callable, Mapping


EUROPE_PMC = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
CROSSREF = "https://api.crossref.org/works"
ARXIV_API = "https://export.arxiv.org/api/query"
OPENREVIEW_API = "https://api2.openreview.net/notes"
PUBMED_ESEARCH = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
PUBMED_EFETCH = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
BIORXIV_API = "https://api.biorxiv.org/details"
CAMBRIDGE_OPEN_ENGAGE_API = (
  "https://www.cambridge.org/engage/coe/public-api/v1/items/doi"
)
DEFAULT_CACHE = Path(os.getenv("PAPERBOT_METADATA_CACHE", "/tmp/skm-paperbot-abstract-cache.json"))

ARXIV_ID_RE = re.compile(r"(?:arxiv[.:/]|abs/)(\d{4}\.\d{4,5}|[a-z-]+/\d{7})(?:v\d+)?", re.I)
BARE_ARXIV_ID_RE = re.compile(
  r"^(\d{4}\.\d{4,5}|[a-z-]+/\d{7})(?:v\d+)?$", re.I
)
DOI_RE = re.compile(r"10\.\d{4,9}/[^\s<>{}\[\]\"']+", re.I)
TRAILING_SECTIONS = re.compile(
  r"\s+(?:Competing Interests?(?: Statement)?|Conflict of Interest(?: Statement)?|Copyright|Keywords?)\s*[:.]\s+.*$",
  re.I | re.S,
)


@dataclass(frozen=True)
class ResolvedAbstract:
  text: str
  source: str
  source_url: str
  license: str = "unknown"


def normalize_abstract(value: str) -> str:
  value = re.sub(r"<[^>]+>", " ", html.unescape(value or ""))
  value = unicodedata.normalize("NFC", value)
  value = " ".join(value.split())
  value = TRAILING_SECTIONS.sub("", value).strip()
  return value


def _identity_text(value: str) -> str:
  value = re.sub(r"<[^>]+>", " ", html.unescape(value or ""))
  value = unicodedata.normalize("NFKD", value.casefold())
  value = "".join(character for character in value if not unicodedata.combining(character))
  return re.sub(r"[^a-z0-9]+", " ", value).strip()


def _first_author_surname(value: str) -> str:
  first = re.split(r"\s+and\s+", normalize_abstract(value), maxsplit=1, flags=re.I)[0]
  if not first:
    return ""
  surname = first.split(",", 1)[0] if "," in first else first.split()[-1]
  return re.sub(r"[^a-z0-9]", "", _identity_text(surname))


def normalize_doi(value: str) -> str:
  match = DOI_RE.search(urllib.parse.unquote(value or ""))
  if not match:
    return ""
  return match.group(0).rstrip(".,;)").lower()


def extract_arxiv_id(*values: str) -> str:
  for value in values:
    candidate = (value or "").strip()
    match = ARXIV_ID_RE.search(candidate) or BARE_ARXIV_ID_RE.match(candidate)
    if match:
      return re.sub(r"v\d+$", "", match.group(1), flags=re.I)
  return ""


class MetadataHTMLParser(HTMLParser):
  def __init__(self) -> None:
    super().__init__()
    self.values: dict[str, list[str]] = {}
    self.json_ld: list[str] = []
    self._json_depth = 0
    self._json_parts: list[str] = []

  def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
    attributes = {key.lower(): value for key, value in attrs if value is not None}
    if tag.lower() == "meta":
      key = (attributes.get("name") or attributes.get("property") or "").lower()
      content = attributes.get("content", "").strip()
      if key and content:
        self.values.setdefault(key, []).append(content)
    if tag.lower() == "script" and attributes.get("type", "").lower() == "application/ld+json":
      self._json_depth = 1
      self._json_parts = []
    elif self._json_depth:
      self._json_depth += 1

  def handle_endtag(self, tag: str) -> None:
    if not self._json_depth:
      return
    self._json_depth -= 1
    if self._json_depth == 0:
      value = "".join(self._json_parts).strip()
      if value:
        self.json_ld.append(value)
      self._json_parts = []

  def handle_data(self, data: str) -> None:
    if self._json_depth:
      self._json_parts.append(data)


class AbstractResolver:
  def __init__(
    self,
    *,
    contact_email: str = "",
    cache_path: Path = DEFAULT_CACHE,
    request: Callable[[str, Mapping[str, str]], bytes] | None = None,
    allow_arbitrary_html: bool | None = None,
  ) -> None:
    self.contact_email = contact_email
    self.cache_path = cache_path
    self._request_override = request
    self.allow_arbitrary_html = (
      os.getenv("PAPERBOT_DISABLE_ARBITRARY_HTML", "").strip().casefold()
      not in {"1", "true", "yes"}
      if allow_arbitrary_html is None
      else allow_arbitrary_html
    )
    self._last_request_at: dict[str, float] = {}
    self.cache: dict[str, dict[str, str]] = {}
    if cache_path.exists():
      try:
        raw = json.loads(cache_path.read_text())
        if isinstance(raw, dict):
          self.cache = raw
      except (OSError, json.JSONDecodeError):
        pass

  @property
  def user_agent(self) -> str:
    contact = self.contact_email or "https://github.com/delalamo/SKM"
    return f"SKM-Paperbot/1.0 ({contact})"

  def _request(self, url: str, *, accept: str = "application/json", attempts: int = 4) -> bytes:
    headers = {"User-Agent": self.user_agent, "Accept": accept}
    if self._request_override:
      return self._request_override(url, headers)
    for attempt in range(attempts):
      self._throttle(url)
      request = urllib.request.Request(url, headers=headers)
      try:
        with urllib.request.urlopen(request, timeout=45) as response:
          return response.read()
      except urllib.error.HTTPError as error:
        if error.code not in {429, 500, 502, 503, 504}:
          raise
        if attempt == attempts - 1:
          raise
        retry_after = error.headers.get("Retry-After")
        delay = float(retry_after) if retry_after else min(30.0, 2.0 * (2**attempt))
      except (TimeoutError, urllib.error.URLError):
        if attempt == attempts - 1:
          raise
        delay = min(30.0, 2.0 * (2**attempt))
      time.sleep(delay)
    raise RuntimeError(f"failed to fetch {url}")

  def _throttle(self, url: str) -> None:
    host = (urllib.parse.urlparse(url).hostname or "").casefold()
    if host in {"arxiv.org", "export.arxiv.org"}:
      interval = 3.1
    elif host == "eutils.ncbi.nlm.nih.gov":
      interval = 0.11 if os.getenv("NCBI_API_KEY", "").strip() else 0.34
    elif host.endswith("europepmc.org") or host.endswith("ebi.ac.uk"):
      interval = 0.1
    else:
      interval = 0.0
    if interval <= 0:
      return
    now = time.monotonic()
    delay = interval - (now - self._last_request_at.get(host, 0.0))
    if delay > 0:
      time.sleep(delay)
    self._last_request_at[host] = time.monotonic()

  def _cached(self, key: str, resolver: Callable[[], ResolvedAbstract | None]) -> ResolvedAbstract | None:
    cached = self.cache.get(key)
    if cached:
      return ResolvedAbstract(**cached)
    result = resolver()
    if result and result.text:
      self.cache[key] = {
        "text": result.text,
        "source": result.source,
        "source_url": result.source_url,
        "license": result.license,
      }
      self.cache_path.parent.mkdir(parents=True, exist_ok=True)
      self.cache_path.write_text(json.dumps(self.cache, ensure_ascii=False, indent=2, sort_keys=True))
    return result

  def europe_pmc(self, doi: str = "", pmid: str = "") -> ResolvedAbstract | None:
    identity = f"EXT_ID:{pmid} AND SRC:MED" if pmid else f'DOI:"{doi}"'
    params = urllib.parse.urlencode({"query": identity, "format": "json", "resultType": "core", "pageSize": 3})
    url = f"{EUROPE_PMC}?{params}"

    def resolve() -> ResolvedAbstract | None:
      data = json.loads(self._request(url))
      for record in data.get("resultList", {}).get("result", []):
        abstract = normalize_abstract(str(record.get("abstractText", "")))
        if abstract:
          return ResolvedAbstract(abstract, "europe-pmc", url, str(record.get("license", "unknown")))
      return None

    return self._cached(f"europe-pmc:{pmid or doi}", resolve)

  def arxiv(self, arxiv_id: str) -> ResolvedAbstract | None:
    url = f"{ARXIV_API}?{urllib.parse.urlencode({'id_list': arxiv_id, 'max_results': 1})}"

    def resolve() -> ResolvedAbstract | None:
      root = ET.fromstring(self._request(url, accept="application/atom+xml"))
      namespace = "{http://www.w3.org/2005/Atom}"
      entry = root.find(f"{namespace}entry")
      if entry is None:
        return None
      abstract = normalize_abstract(entry.findtext(f"{namespace}summary", ""))
      if not abstract:
        return None
      return ResolvedAbstract(abstract, "arxiv", f"https://arxiv.org/abs/{arxiv_id}", "CC0-1.0 metadata")

    return self._cached(f"arxiv:{arxiv_id}", resolve)

  def arxiv_title(self, title: str, author: str = "") -> ResolvedAbstract | None:
    """Resolve an exact-title arXiv result when a citation omits its arXiv ID."""

    normalized_title = _identity_text(title)
    if not normalized_title:
      return None
    params = urllib.parse.urlencode(
      {"query": title, "searchtype": "title", "abstracts": "show"}
    )
    search_url = f"https://arxiv.org/search/?{params}"
    cache_key = hashlib.sha256(normalized_title.encode("utf-8")).hexdigest()

    def resolve() -> ResolvedAbstract | None:
      # This is a last-resort lookup. Fail fast when arXiv is rate-limiting so
      # one optional search cannot hold up every unresolved bibliography item.
      payload = self._request(search_url, accept="text/html", attempts=1).decode(
        "utf-8", "replace"
      )
      expected_author = _first_author_surname(author)
      for block in re.findall(
        r'<li\s+class="arxiv-result"[^>]*>(.*?)</li>', payload, flags=re.I | re.S
      ):
        title_match = re.search(
          r'<p\s+class="[^"]*\btitle\b[^"]*"[^>]*>(.*?)</p>',
          block,
          flags=re.I | re.S,
        )
        if not title_match or _identity_text(title_match.group(1)) != normalized_title:
          continue
        if expected_author:
          author_match = re.search(
            r'<p\s+class="authors"[^>]*>.*?<a[^>]*>(.*?)</a>',
            block,
            flags=re.I | re.S,
          )
          if not author_match or _first_author_surname(author_match.group(1)) != expected_author:
            continue
        abstract_match = re.search(
          r'<span\s+class="[^"]*abstract-full[^"]*"[^>]*>(.*?)</span>',
          block,
          flags=re.I | re.S,
        )
        id_match = re.search(r'href="https?://arxiv\.org/abs/([^"?#]+)', block, re.I)
        abstract = normalize_abstract(abstract_match.group(1) if abstract_match else "")
        if abstract:
          source_url = (
            f"https://arxiv.org/abs/{id_match.group(1)}" if id_match else search_url
          )
          return ResolvedAbstract(
            abstract, "arxiv-title", source_url, "CC0-1.0 metadata"
          )
      return None

    return self._cached(f"arxiv-title:{cache_key}", resolve)

  def pubmed(self, doi: str = "", pmid: str = "") -> ResolvedAbstract | None:
    """Resolve directly through NCBI when Europe PMC has no abstract."""

    identity = pmid or doi
    if not identity:
      return None

    def resolve() -> ResolvedAbstract | None:
      resolved_pmid = pmid
      if not resolved_pmid:
        params: dict[str, str] = {
          "db": "pubmed",
          "retmode": "json",
          "retmax": "3",
          "term": f'"{doi}"[AID]',
          "tool": "SKM-paperbot",
        }
        if self.contact_email:
          params["email"] = self.contact_email
        api_key = os.getenv("NCBI_API_KEY", "").strip()
        if api_key:
          params["api_key"] = api_key
        search_url = f"{PUBMED_ESEARCH}?{urllib.parse.urlencode(params)}"
        data = json.loads(self._request(search_url))
        ids = data.get("esearchresult", {}).get("idlist", [])
        resolved_pmid = str(ids[0]) if ids else ""
      if not resolved_pmid:
        return None
      params = {
        "db": "pubmed",
        "retmode": "xml",
        "id": resolved_pmid,
        "tool": "SKM-paperbot",
      }
      if self.contact_email:
        params["email"] = self.contact_email
      api_key = os.getenv("NCBI_API_KEY", "").strip()
      if api_key:
        params["api_key"] = api_key
      fetch_url = f"{PUBMED_EFETCH}?{urllib.parse.urlencode(params)}"
      root = ET.fromstring(self._request(fetch_url, accept="application/xml"))
      parts: list[str] = []
      for node in root.findall(".//Article/Abstract/AbstractText"):
        text = normalize_abstract("".join(node.itertext()))
        label = normalize_abstract(node.attrib.get("Label", ""))
        if text:
          parts.append(f"{label}: {text}" if label else text)
      abstract = normalize_abstract(" ".join(parts))
      if not abstract:
        return None
      return ResolvedAbstract(
        abstract,
        "pubmed",
        f"https://pubmed.ncbi.nlm.nih.gov/{resolved_pmid}/",
        "unknown",
      )

    return self._cached(f"pubmed:{identity}", resolve)

  def crossref(self, doi: str) -> ResolvedAbstract | None:
    url = f"{CROSSREF}/{urllib.parse.quote(doi, safe='/')}"

    def resolve() -> ResolvedAbstract | None:
      data = json.loads(self._request(url))
      message = data.get("message", {})
      abstract = normalize_abstract(str(message.get("abstract", "")))
      if not abstract:
        return None
      licenses = message.get("license", [])
      license_value = "unknown"
      if licenses and isinstance(licenses[0], dict):
        license_value = str(licenses[0].get("URL", "unknown"))
      return ResolvedAbstract(abstract, "crossref", url, license_value)

    return self._cached(f"crossref:{doi}", resolve)

  def openrxiv(self, doi: str, server: str) -> ResolvedAbstract | None:
    """Resolve a bioRxiv or medRxiv DOI through its native metadata API."""

    if server not in {"biorxiv", "medrxiv"}:
      raise ValueError(f"unsupported openRxiv server: {server}")
    url = f"{BIORXIV_API}/{server}/{urllib.parse.quote(doi, safe='/')}/na/json"

    def resolve() -> ResolvedAbstract | None:
      data = json.loads(self._request(url))
      for record in data.get("collection", []):
        abstract = normalize_abstract(str(record.get("abstract", "")))
        if abstract:
          return ResolvedAbstract(
            abstract,
            server,
            url,
            str(record.get("license", "unknown")),
          )
      return None

    return self._cached(f"{server}:{doi}", resolve)

  def chemrxiv(self, doi: str) -> ResolvedAbstract | None:
    """Resolve a ChemRxiv DOI through Cambridge Open Engage's public API."""

    url = f"{CAMBRIDGE_OPEN_ENGAGE_API}/{urllib.parse.quote(doi, safe='/')}"

    def resolve() -> ResolvedAbstract | None:
      data = json.loads(self._request(url))
      records = data if isinstance(data, list) else [data]
      for record in records:
        if not isinstance(record, dict):
          continue
        # The API has used both a direct item and a small envelope over time.
        candidates = [record]
        candidates.extend(
          value for value in record.values() if isinstance(value, dict)
        )
        for candidate in candidates:
          abstract = normalize_abstract(str(candidate.get("abstract", "")))
          if not abstract:
            continue
          license_value: Any = candidate.get("license", "unknown")
          if isinstance(license_value, dict):
            license_value = (
              license_value.get("url")
              or license_value.get("name")
              or license_value.get("label")
              or "unknown"
            )
          return ResolvedAbstract(
            abstract,
            "chemrxiv",
            url,
            str(license_value),
          )
      return None

    return self._cached(f"chemrxiv:{doi}", resolve)

  def openreview(self, forum_id: str) -> ResolvedAbstract | None:
    url = f"{OPENREVIEW_API}?{urllib.parse.urlencode({'forum': forum_id, 'limit': 1000})}"

    def resolve() -> ResolvedAbstract | None:
      data = json.loads(self._request(url))
      for note in data.get("notes", []):
        content = note.get("content", {})
        value: Any = content.get("abstract", "")
        if isinstance(value, dict):
          value = value.get("value", "")
        abstract = normalize_abstract(str(value))
        if abstract:
          return ResolvedAbstract(abstract, "openreview", f"https://openreview.net/forum?id={forum_id}", "CC0-1.0 metadata")
      return None

    return self._cached(f"openreview:{forum_id}", resolve)

  def html_metadata(self, url: str) -> ResolvedAbstract | None:
    def resolve() -> ResolvedAbstract | None:
      payload = self._request(url, accept="text/html,application/xhtml+xml").decode("utf-8", "replace")
      parser = MetadataHTMLParser()
      parser.feed(payload)
      for key in ("citation_abstract", "dc.description", "dcterms.abstract", "og:description", "description"):
        for value in parser.values.get(key, []):
          abstract = normalize_abstract(value)
          if len(abstract.split()) >= 20:
            return ResolvedAbstract(abstract, "html-metadata", url)
      for raw in parser.json_ld:
        try:
          values = json.loads(raw)
        except json.JSONDecodeError:
          continue
        nodes = values if isinstance(values, list) else [values]
        for node in nodes:
          if not isinstance(node, dict):
            continue
          value = node.get("abstract") or node.get("description")
          abstract = normalize_abstract(str(value or ""))
          if len(abstract.split()) >= 20:
            return ResolvedAbstract(abstract, "json-ld", url, str(node.get("license", "unknown")))
      # Proceedings sites such as NeurIPS expose a plainly headed abstract but
      # no citation_abstract meta tag. Keep this deliberately narrow.
      for pattern in (
        r'<h[1-6][^>]*>\s*Abstract\s*</h[1-6]>\s*<p[^>]*>(.*?)</p>',
        r'<p[^>]*class="[^"]*\babstract\b[^"]*"[^>]*>(.*?)</p>',
      ):
        match = re.search(pattern, payload, flags=re.I | re.S)
        abstract = normalize_abstract(match.group(1) if match else "")
        if len(abstract.split()) >= 20:
          return ResolvedAbstract(abstract, "structured-html", url)
      return None

    return self._cached(f"html:{url}", resolve)

  def resolve(self, fields: Mapping[str, str]) -> ResolvedAbstract | None:
    existing = normalize_abstract(fields.get("abstract", ""))
    if existing:
      return ResolvedAbstract(existing, "bibliography", fields.get("url", ""))

    doi = normalize_doi(fields.get("doi", "") or fields.get("url", ""))
    pmid = fields.get("pmid", "").strip()
    url = fields.get("url", "").strip()
    arxiv_id = extract_arxiv_id(
      fields.get("eprint", ""), fields.get("arxiv", ""), fields.get("doi", ""), url
    )
    resolvers: list[Callable[[], ResolvedAbstract | None]] = []
    if doi or pmid:
      resolvers.append(lambda: self.europe_pmc(doi, pmid))
      resolvers.append(lambda: self.pubmed(doi, pmid))
    if arxiv_id:
      # The canonical abstract page carries citation_abstract metadata and is
      # more reliable than the legacy export host; retain Atom as a fallback.
      resolvers.append(
        lambda: self.html_metadata(f"https://arxiv.org/abs/{arxiv_id}")
      )
      resolvers.append(lambda: self.arxiv(arxiv_id))
    server = fields.get("server", "").strip().casefold()
    if doi.startswith("10.1101/"):
      if server in {"biorxiv", "medrxiv"}:
        resolvers.append(lambda: self.openrxiv(doi, server))
      else:
        # The DOI prefix is shared. Trying both native endpoints is cheap and
        # keeps old bibliography entries from needing a provider annotation.
        resolvers.append(lambda: self.openrxiv(doi, "biorxiv"))
        resolvers.append(lambda: self.openrxiv(doi, "medrxiv"))
    if doi.startswith("10.26434/") or "chemrxiv" in url.casefold():
      resolvers.append(lambda: self.chemrxiv(doi))
    if doi:
      resolvers.append(lambda: self.crossref(doi))
    openreview_match = re.search(r"openreview\.net/forum\?id=([^&#]+)", url)
    if openreview_match:
      forum_id = urllib.parse.unquote(openreview_match.group(1))
      resolvers.append(lambda: self.openreview(forum_id))
    if url and self.allow_arbitrary_html:
      resolvers.append(lambda: self.html_metadata(url))
    if fields.get("title", "").strip():
      resolvers.append(
        lambda: self.arxiv_title(
          fields.get("title", ""), fields.get("author", "")
        )
      )

    for resolver in resolvers:
      try:
        result = resolver()
      except (OSError, RuntimeError, ValueError, ET.ParseError, json.JSONDecodeError):
        continue
      if result and result.text:
        return result
    return None
