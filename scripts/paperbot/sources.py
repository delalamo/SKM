"""Direct, paginated metadata clients for the daily paper feeds.

Every provider returns a :class:`SourceResult`, retaining records fetched before
a later page failed.  ``fetch_all_sources`` isolates providers from one another
and returns both the successfully normalized records and structured failures.
No provider SDK or dataframe dependency is required.
"""

from __future__ import annotations

import hashlib
import http.client
import json
import math
import re
import socket
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from datetime import UTC, date, datetime, timedelta
from email.utils import parsedate_to_datetime
from typing import Any, Callable, Iterable, Mapping, Protocol, Sequence, TypeVar

from .records import (
  PaperRecord,
  arxiv_version,
  chemrxiv_version,
  clean_text,
  deduplicate_records,
  ensure_utc,
  normalize_arxiv_id,
  normalize_doi,
)


PUBMED_ESEARCH = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
PUBMED_EFETCH = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
ARXIV_API = "https://export.arxiv.org/api/query"
RXIV_API = "https://api.biorxiv.org"
CHEMRXIV_API = "https://chemrxiv.org/engage/chemrxiv/public-api/v1/items"
CHEMRXIV_CROSSREF_API = "https://api.crossref.org/works"
CHEMRXIV_DETAIL_API = "https://www.cambridge.org/engage/coe/public-api/v1/items/doi"
# Backward-compatible name for callers/tests that refer to the fallback endpoint.
CHEMRXIV_FALLBACK_API = CHEMRXIV_CROSSREF_API

ATOM = "{http://www.w3.org/2005/Atom}"
ARXIV = "{http://arxiv.org/schemas/atom}"
OPENSEARCH = "{http://a9.com/-/spec/opensearch/1.1/}"
# q-bio and cond-mat historically accepted archive-level submissions, so the
# wildcard intentionally precedes the dot and covers both the archive and all
# modern subcategories.  stat has only dotted subject classes.
ARXIV_CATEGORY_FAMILIES = ("q-bio*", "cond-mat*", "stat.*")
ARXIV_PAGE_SIZE = 500
RETRYABLE_STATUS = frozenset({429, 500, 502, 503, 504})
# Retry a failed provider before embedding: once quickly, then after an outage-sized pause.
PROVIDER_RETRY_DELAYS = (60.0, 3_600.0)
SENSITIVE_QUERY_KEYS = frozenset(
  {"api_key", "apikey", "token", "access_token", "client_secret"}
)
PUBMED_RESULT_CAP = 9_999
PUBMED_INITIAL_UID_MAX = 99_999_999


@dataclass(frozen=True, slots=True)
class FetchWindow:
  """One immutable run boundary plus its idempotent recovery overlap."""

  logical_since: datetime
  query_since: datetime
  until: datetime

  def __post_init__(self) -> None:
    logical = ensure_utc(self.logical_since)
    query = ensure_utc(self.query_since)
    until = ensure_utc(self.until)
    if logical is None or query is None or until is None:
      raise ValueError("fetch window timestamps are required")
    if not query <= logical < until:
      raise ValueError("fetch window must satisfy query_since <= logical_since < until")
    object.__setattr__(self, "logical_since", logical)
    object.__setattr__(self, "query_since", query)
    object.__setattr__(self, "until", until)

  @classmethod
  def ending_at(
    cls, as_of: datetime, *, logical_hours: int = 24, recovery_hours: int = 72
  ) -> FetchWindow:
    boundary = ensure_utc(as_of)
    if boundary is None:
      raise ValueError("as_of is required")
    if logical_hours <= 0 or recovery_hours <= logical_hours:
      raise ValueError("recovery_hours must be greater than logical_hours")
    return cls(
      logical_since=boundary - timedelta(hours=logical_hours),
      query_since=boundary - timedelta(hours=recovery_hours),
      until=boundary,
    )

  @classmethod
  def between(cls, since: datetime, until: datetime) -> FetchWindow:
    """Build an exact manual backfill window without adding recovery overlap."""

    return cls(logical_since=since, query_since=since, until=until)

  def includes_query_timestamp(self, value: datetime | date | str | None) -> bool:
    timestamp = ensure_utc(value)
    return timestamp is not None and self.query_since <= timestamp < self.until

  def includes_logical_timestamp(self, value: datetime | date | str | None) -> bool:
    """Return whether ``value`` belongs to the run's exact logical tranche."""

    timestamp = ensure_utc(value)
    return timestamp is not None and self.logical_since <= timestamp < self.until

  @property
  def query_end_date(self) -> date:
    """Last provider date included by the half-open ``[since, until)`` window."""

    return (self.until - timedelta(microseconds=1)).date()

  def includes_query_date(self, value: datetime | date | str | None) -> bool:
    timestamp = ensure_utc(value)
    return (
      timestamp is not None
      and self.query_since.date() <= timestamp.date() <= self.query_end_date
    )


@dataclass(frozen=True, slots=True)
class SourceFailure:
  source: str
  operation: str
  message: str
  retryable: bool = False
  status: int | None = None


@dataclass(slots=True)
class SourceResult:
  source: str
  records: list[PaperRecord] = field(default_factory=list)
  errors: list[SourceFailure] = field(default_factory=list)
  skipped: int = 0

  @property
  def ok(self) -> bool:
    return not self.errors


@dataclass(frozen=True, slots=True)
class FetchReport:
  window: FetchWindow
  records: tuple[PaperRecord, ...]
  errors: tuple[SourceFailure, ...]
  source_counts: Mapping[str, int]

  @property
  def ok(self) -> bool:
    return not self.errors


@dataclass(frozen=True, slots=True)
class HttpResponse:
  status: int
  headers: Mapping[str, str]
  body: bytes


class HttpRequestError(RuntimeError):
  def __init__(self, message: str, *, status: int | None = None, retryable: bool = False):
    super().__init__(message)
    self.status = status
    self.retryable = retryable


_ResponseValue = TypeVar("_ResponseValue")


class HttpClientProtocol(Protocol):
  def get_bytes(
    self,
    url: str,
    *,
    params: Mapping[str, Any] | None = None,
    headers: Mapping[str, str] | None = None,
    min_interval: float = 0.0,
  ) -> bytes: ...

  def get_json(
    self,
    url: str,
    *,
    params: Mapping[str, Any] | None = None,
    headers: Mapping[str, str] | None = None,
    min_interval: float = 0.0,
  ) -> Any: ...


def _default_transport(request: urllib.request.Request, timeout: float) -> HttpResponse:
  with urllib.request.urlopen(request, timeout=timeout) as response:
    return HttpResponse(
      status=getattr(response, "status", 200),
      headers=dict(response.headers.items()),
      body=response.read(),
    )


class HttpClient:
  """Small urllib client with injectable retry, sleeping, and rate limiting."""

  def __init__(
    self,
    *,
    user_agent: str,
    attempts: int = 5,
    timeout: float = 60.0,
    transport: Callable[[urllib.request.Request, float], HttpResponse] = _default_transport,
    sleep: Callable[[float], None] = time.sleep,
    monotonic: Callable[[], float] = time.monotonic,
  ):
    if not user_agent:
      raise ValueError("a descriptive user agent is required")
    if attempts < 1:
      raise ValueError("attempts must be positive")
    self.user_agent = user_agent
    self.attempts = attempts
    self.timeout = timeout
    self.transport = transport
    self.sleep = sleep
    self.monotonic = monotonic
    self._last_request: dict[str, float] = {}

  def _rate_limit(self, url: str, interval: float) -> None:
    if interval <= 0:
      return
    host = urllib.parse.urlparse(url).netloc.casefold()
    now = self.monotonic()
    previous = self._last_request.get(host)
    if previous is not None:
      delay = interval - (now - previous)
      if delay > 0:
        self.sleep(delay)
        now = self.monotonic()
    self._last_request[host] = now

  @staticmethod
  def _retry_after(headers: Mapping[str, str], fallback: float) -> float:
    value = next((item for key, item in headers.items() if key.casefold() == "retry-after"), "")
    if not value:
      return fallback
    try:
      return max(0.0, float(value))
    except ValueError:
      try:
        return max(0.0, (parsedate_to_datetime(value) - datetime.now(UTC)).total_seconds())
      except (TypeError, ValueError):
        return fallback

  def _get(
    self,
    url: str,
    *,
    params: Mapping[str, Any] | None = None,
    headers: Mapping[str, str] | None = None,
    min_interval: float = 0.0,
    decode: Callable[[bytes, str], _ResponseValue],
  ) -> _ResponseValue:
    if params:
      separator = "&" if "?" in url else "?"
      url = f"{url}{separator}{urllib.parse.urlencode(params, doseq=True)}"
    safe_url = _redact_url(url)
    request_headers = {"Accept": "*/*", "User-Agent": self.user_agent}
    request_headers.update(headers or {})
    last_error: Exception | None = None
    for attempt in range(self.attempts):
      self._rate_limit(url, min_interval)
      request = urllib.request.Request(url, headers=request_headers)
      try:
        response = self.transport(request, self.timeout)
        if response.status >= 400:
          retryable = response.status in RETRYABLE_STATUS
          raise HttpRequestError(
            f"HTTP {response.status} for {safe_url}",
            status=response.status,
            retryable=retryable,
          )
        return decode(response.body, safe_url)
      except urllib.error.HTTPError as error:
        retryable = error.code in RETRYABLE_STATUS
        last_error = HttpRequestError(
          f"HTTP {error.code} for {safe_url}",
          status=error.code,
          retryable=retryable,
        )
        error_headers = dict(error.headers.items()) if error.headers else {}
        delay = self._retry_after(error_headers, min(60.0, 2.0**attempt))
      except HttpRequestError as error:
        last_error = HttpRequestError(
          _redact_error_message(str(error), url),
          status=error.status,
          retryable=error.retryable,
        )
        retryable = error.retryable
        delay = min(60.0, 2.0**attempt)
      except (
        http.client.IncompleteRead,
        TimeoutError,
        socket.timeout,
        urllib.error.URLError,
        OSError,
      ) as error:
        last_error = HttpRequestError(
          _redact_error_message(str(error), url), retryable=True
        )
        retryable = True
        delay = min(60.0, 2.0**attempt)
      if not retryable or attempt + 1 == self.attempts:
        assert last_error is not None
        raise last_error
      self.sleep(delay)
    raise HttpRequestError(f"request failed for {safe_url}", retryable=True)

  def get_bytes(
    self,
    url: str,
    *,
    params: Mapping[str, Any] | None = None,
    headers: Mapping[str, str] | None = None,
    min_interval: float = 0.0,
  ) -> bytes:
    return self._get(
      url,
      params=params,
      headers=headers,
      min_interval=min_interval,
      decode=lambda body, _safe_url: body,
    )

  def get_json(
    self,
    url: str,
    *,
    params: Mapping[str, Any] | None = None,
    headers: Mapping[str, str] | None = None,
    min_interval: float = 0.0,
  ) -> Any:
    def decode(body: bytes, safe_url: str) -> Any:
      try:
        return json.loads(body)
      except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise HttpRequestError(
          f"invalid JSON from {safe_url}: {error}", retryable=True
        ) from error

    return self._get(
      url,
      params=params,
      headers=headers,
      min_interval=min_interval,
      decode=decode,
    )


def _redact_url(url: str) -> str:
  """Retain query parameter names while removing credential values."""

  try:
    parsed = urllib.parse.urlsplit(url)
    query = urllib.parse.parse_qsl(parsed.query, keep_blank_values=True)
    redacted = [
      (key, "REDACTED" if key.casefold() in SENSITIVE_QUERY_KEYS else value)
      for key, value in query
    ]
    return urllib.parse.urlunsplit(
      (parsed.scheme, parsed.netloc, parsed.path, urllib.parse.urlencode(redacted), parsed.fragment)
    )
  except (TypeError, ValueError):
    return "<invalid URL>"


def _redact_error_message(message: str, request_url: str) -> str:
  """Remove request credential values from provider-supplied error text too."""

  safe = message.replace(request_url, _redact_url(request_url))
  try:
    query = urllib.parse.parse_qsl(
      urllib.parse.urlsplit(request_url).query, keep_blank_values=True
    )
  except (TypeError, ValueError):
    return safe
  for key, value in query:
    if key.casefold() not in SENSITIVE_QUERY_KEYS or not value:
      continue
    for representation in {
      value,
      urllib.parse.quote(value, safe=""),
      urllib.parse.quote_plus(value, safe=""),
    }:
      safe = safe.replace(representation, "REDACTED")
  return safe


def _failure(source: str, operation: str, error: Exception) -> SourceFailure:
  return SourceFailure(
    source=source,
    operation=operation,
    message=str(error),
    retryable=bool(getattr(error, "retryable", False)),
    status=getattr(error, "status", None),
  )


def _xml_text(node: ET.Element | None) -> str:
  return clean_text("".join(node.itertext())) if node is not None else ""


MONTHS = {
  name.casefold(): number
  for number, name in enumerate(
    ("", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")
  )
  if name
}


def _pubmed_date(node: ET.Element | None) -> datetime | None:
  if node is None:
    return None
  try:
    year = int(_xml_text(node.find("Year")))
  except ValueError:
    return None
  month_text = _xml_text(node.find("Month"))
  try:
    month = int(month_text or "1")
  except ValueError:
    month = MONTHS.get(month_text[:3].casefold(), 1)
  try:
    day = int(_xml_text(node.find("Day")) or "1")
    hour = int(_xml_text(node.find("Hour")) or "0")
    minute = int(_xml_text(node.find("Minute")) or "0")
    second = int(_xml_text(node.find("Second")) or "0")
    return datetime(year, month, day, hour, minute, second, tzinfo=UTC)
  except ValueError:
    return datetime(year, 1, 1, tzinfo=UTC)


def _pubmed_date_precision(node: ET.Element | None) -> str:
  """Describe the finest timestamp component supplied by PubMed."""

  if node is None:
    return "day"
  for field, precision in (
    ("Second", "second"),
    ("Minute", "minute"),
    ("Hour", "hour"),
    ("Day", "day"),
    ("Month", "month"),
    ("Year", "year"),
  ):
    if _xml_text(node.find(field)):
      return precision
  return "day"


def _pubmed_entrez_date_node(item: ET.Element, *, is_book: bool) -> ET.Element | None:
  """Find PubMed's precise timestamp for first addition to the database."""

  history_path = (
    "./PubmedBookData/History/PubMedPubDate"
    if is_book
    else "./PubmedData/History/PubMedPubDate"
  )
  return next(
    (
      node
      for node in item.findall(history_path)
      if node.attrib.get("PubStatus", "").casefold() == "entrez"
    ),
    None,
  )


def _pubmed_date_text(node: ET.Element | None) -> str:
  """Return the date at the precision actually supplied by PubMed."""

  if node is None:
    return ""
  year_text = _xml_text(node.find("Year"))
  if not re.fullmatch(r"(?:19|20)\d{2}", year_text):
    return ""
  month_text = _xml_text(node.find("Month"))
  if not month_text:
    return year_text
  try:
    month = int(month_text)
  except ValueError:
    month = MONTHS.get(month_text[:3].casefold(), 0)
  if not 1 <= month <= 12:
    return year_text
  day_text = _xml_text(node.find("Day"))
  if not day_text:
    return f"{year_text}-{month:02d}"
  try:
    date = datetime(int(year_text), month, int(day_text), tzinfo=UTC)
  except ValueError:
    return f"{year_text}-{month:02d}"
  return date.date().isoformat()


def _pubmed_publication_date(article: ET.Element) -> datetime | None:
  pub_date = article.find("./MedlineCitation/Article/Journal/JournalIssue/PubDate")
  direct = _pubmed_date(pub_date)
  if direct:
    return direct
  medline_date = _xml_text(pub_date.find("MedlineDate")) if pub_date is not None else ""
  match = re.search(r"(?:19|20)\d{2}", medline_date)
  return datetime(int(match.group(0)), 1, 1, tzinfo=UTC) if match else None


def _pubmed_publication_date_text(article: ET.Element) -> str:
  pub_date = article.find("./MedlineCitation/Article/Journal/JournalIssue/PubDate")
  direct = _pubmed_date_text(pub_date)
  if direct:
    return direct
  medline_date = _xml_text(pub_date.find("MedlineDate")) if pub_date is not None else ""
  match = re.search(r"(?:19|20)\d{2}", medline_date)
  return match.group(0) if match else ""


def parse_pubmed_xml(payload: bytes) -> list[PaperRecord]:
  root = ET.fromstring(payload)
  records: list[PaperRecord] = []
  items = [
    *((item, False) for item in root.findall("./PubmedArticle")),
    *((item, True) for item in root.findall("./PubmedBookArticle")),
  ]
  for item, is_book in items:
    document_path = "./BookDocument" if is_book else "./MedlineCitation"
    content_path = document_path if is_book else f"{document_path}/Article"
    pmid = _xml_text(item.find(f"{document_path}/PMID"))
    title = _xml_text(item.find(f"{content_path}/ArticleTitle"))
    if is_book and not title:
      title = _xml_text(item.find("./BookDocument/Book/BookTitle"))
    abstract_parts: list[str] = []
    abstract_nodes = item.findall(f"{content_path}/Abstract/AbstractText")
    if not abstract_nodes and not is_book:
      abstract_nodes = item.findall("./MedlineCitation/OtherAbstract/AbstractText")
    for abstract_node in abstract_nodes:
      text = _xml_text(abstract_node)
      label = clean_text(
        abstract_node.attrib.get("Label") or abstract_node.attrib.get("NlmCategory", "")
      )
      if text:
        abstract_parts.append(f"{label}: {text}" if label and not text.startswith(f"{label}:") else text)
    abstract = clean_text(" ".join(abstract_parts))
    if not pmid or not title or not abstract:
      continue
    authors: list[str] = []
    author_nodes = item.findall(f"{content_path}/AuthorList/Author")
    if is_book and not author_nodes:
      author_nodes = item.findall("./BookDocument/Book/AuthorList/Author")
    for author in author_nodes:
      collective = _xml_text(author.find("CollectiveName"))
      if collective:
        authors.append(collective)
        continue
      given = _xml_text(author.find("ForeName")) or _xml_text(author.find("Initials"))
      family = _xml_text(author.find("LastName"))
      name = clean_text(f"{given} {family}")
      if name:
        authors.append(name)
    doi = ""
    related: list[str] = []
    identifier_nodes = (
      item.findall("./BookDocument/ArticleIdList/ArticleId")
      + item.findall("./PubmedBookData/ArticleIdList/ArticleId")
      if is_book
      else item.findall("./PubmedData/ArticleIdList/ArticleId")
    )
    for identifier in identifier_nodes:
      kind = identifier.attrib.get("IdType", "").casefold()
      value = _xml_text(identifier)
      if kind == "doi":
        doi = normalize_doi(value)
      elif kind in {"pmc", "pii", "mid"} and value:
        related.append(f"{kind}:{value.casefold()}")
    if not doi:
      location_path = (
        "./BookDocument/Book/ELocationID"
        if is_book
        else "./MedlineCitation/Article/ELocationID"
      )
      for identifier in item.findall(location_path):
        if identifier.attrib.get("EIdType", "").casefold() == "doi":
          doi = normalize_doi(_xml_text(identifier))
          if doi:
            break
    entrez_date_node = _pubmed_entrez_date_node(item, is_book=is_book)
    entrez_date = _pubmed_date(entrez_date_node)
    if is_book:
      history_dates = item.findall("./PubmedBookData/History/PubMedPubDate")
      history_by_status = {
        node.attrib.get("PubStatus", "").casefold(): _pubmed_date(node)
        for node in history_dates
      }
      created = (
        entrez_date
        or history_by_status.get("pubmed")
        or history_by_status.get("medline")
      )
      updated = _pubmed_date(item.find("./BookDocument/DateRevised")) or created
      publication_node = item.find("./BookDocument/Book/PubDate")
      published = _pubmed_date(publication_node)
      publication_date = _pubmed_date_text(publication_node)
      venue = _xml_text(item.find("./BookDocument/Book/BookTitle"))
    else:
      created = entrez_date or _pubmed_date(item.find("./MedlineCitation/DateCreated"))
      updated = _pubmed_date(item.find("./MedlineCitation/DateRevised")) or created
      published = _pubmed_publication_date(item)
      publication_date = _pubmed_publication_date_text(item)
      venue = _xml_text(item.find("./MedlineCitation/Article/Journal/Title"))
    records.append(
      PaperRecord(
        source="pubmed",
        source_id=pmid,
        title=title,
        abstract=abstract,
        authors=tuple(authors),
        venue=venue,
        created_at=created or published,
        updated_at=updated or created or published,
        url=f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
        doi=doi,
        pmid=pmid,
        related_ids=tuple(related),
        metadata={
          "timestamp_precision": (
            _pubmed_date_precision(entrez_date_node) if entrez_date else "day"
          ),
          **({"publication_year": published.year} if published else {}),
          **({"publication_date": publication_date} if publication_date else {}),
        },
      )
    )
  return records


def _pubmed_payload_pmids(payload: bytes) -> set[str]:
  root = ET.fromstring(payload)
  return {
    pmid
    for path in (
      "./PubmedArticle/MedlineCitation/PMID",
      "./PubmedBookArticle/BookDocument/PMID",
    )
    for node in root.findall(path)
    if (pmid := _xml_text(node))
  }


def _calendar_days(start: date, end: date) -> Iterable[date]:
  current = start
  while current <= end:
    yield current
    current += timedelta(days=1)


def _pubmed_search_page(
  client: HttpClientProtocol,
  common: Mapping[str, Any],
  *,
  term: str,
  offset: int,
  page_size: int,
  interval: float,
) -> tuple[list[str], int]:
  payload = client.get_json(
    PUBMED_ESEARCH,
    params={
      **common,
      "retmode": "json",
      "retstart": offset,
      "retmax": page_size,
      "term": term,
    },
    min_interval=interval,
  )
  if not isinstance(payload, Mapping) or not isinstance(payload.get("esearchresult"), Mapping):
    raise HttpRequestError("PubMed ESearch returned an unexpected response")
  search = payload["esearchresult"]
  if search.get("ERROR") or search.get("error"):
    raise HttpRequestError(f"PubMed ESearch error: {search.get('ERROR') or search.get('error')}")
  page = [str(value) for value in search.get("idlist", []) if str(value).isdigit()]
  try:
    total = int(search.get("count", 0))
  except (TypeError, ValueError) as error:
    raise HttpRequestError("PubMed ESearch returned an invalid count") from error
  return page, total


def _pubmed_collect_term_ids(
  client: HttpClientProtocol,
  common: Mapping[str, Any],
  *,
  base_term: str,
  page_size: int,
  interval: float,
) -> set[str]:
  """Exhaust one PubMed query, partitioning UID space above its 9,999 cap."""

  page_size = min(max(1, page_size), PUBMED_RESULT_CAP)
  first_page, root_total = _pubmed_search_page(
    client,
    common,
    term=base_term,
    offset=0,
    page_size=page_size,
    interval=interval,
  )

  def exhaust(term: str, first: list[str], expected: int) -> set[str]:
    values = set(first)
    offset = len(first)
    while offset < expected:
      page, page_total = _pubmed_search_page(
        client,
        common,
        term=term,
        offset=offset,
        page_size=page_size,
        interval=interval,
      )
      if page_total != expected:
        raise HttpRequestError(
          f"PubMed result count changed during pagination ({expected} to {page_total})",
          retryable=True,
        )
      if not page:
        raise HttpRequestError(
          f"PubMed pagination ended at {offset} of {expected} records", retryable=True
        )
      values.update(page)
      offset += len(page)
    if len(values) != expected:
      raise HttpRequestError(
        f"PubMed returned {len(values)} unique IDs for {expected} results", retryable=True
      )
    return values

  if root_total <= PUBMED_RESULT_CAP:
    return exhaust(base_term, first_page, root_total)

  largest_seen = max((int(value) for value in first_page), default=0)
  uid_max = max(PUBMED_INITIAL_UID_MAX, largest_seen * 2)

  def partition(lower: int, upper: int) -> tuple[set[str], int]:
    term = f"({base_term}) AND {lower}:{upper}[UID]"
    first, total = _pubmed_search_page(
      client,
      common,
      term=term,
      offset=0,
      page_size=page_size,
      interval=interval,
    )
    if total <= PUBMED_RESULT_CAP:
      return exhaust(term, first, total), total
    if lower >= upper:
      raise HttpRequestError(
        f"PubMed UID {lower} unexpectedly contains {total} results"
      )
    midpoint = (lower + upper) // 2
    left, left_total = partition(lower, midpoint)
    right, right_total = partition(midpoint + 1, upper)
    return left | right, left_total + right_total

  values, partition_total = partition(1, uid_max)
  if partition_total != root_total or len(values) != root_total:
    raise HttpRequestError(
      "PubMed UID partitions did not reproduce the complete result count "
      f"({partition_total} partitioned, {len(values)} unique, {root_total} expected)",
      retryable=True,
    )
  return values


def fetch_pubmed(
  window: FetchWindow,
  client: HttpClientProtocol,
  *,
  contact_email: str = "",
  api_key: str = "",
  known_pubmed_ids: Iterable[str] = (),
  search_page_size: int = 5_000,
  fetch_batch_size: int = 200,
) -> SourceResult:
  result = SourceResult("pubmed")
  managed_ids = {
    value
    for raw_value in known_pubmed_ids
    if (value := str(raw_value).strip()).isdigit()
  }
  ids = set(managed_ids)
  interval = 0.11 if api_key else 0.34
  common: dict[str, Any] = {"db": "pubmed", "tool": "SKM-paperbot"}
  if contact_email:
    common["email"] = contact_email
  if api_key:
    common["api_key"] = api_key
  for day in _calendar_days(window.logical_since.date(), window.query_end_date):
    stamp = day.strftime("%Y/%m/%d")
    # CRDT represents first addition to PubMed. Global LR queries also include
    # routine indexing edits to older records and make a daily discovery run
    # unnecessarily enormous. Revisions are checked through ``managed_ids``.
    term = f'"{stamp}"[CRDT] AND hasabstract'
    try:
      ids.update(
        _pubmed_collect_term_ids(
          client,
          common,
          base_term=term,
          page_size=search_page_size,
          interval=interval,
        )
      )
    except Exception as error:
      result.errors.append(_failure("pubmed", f"search CRDT {day.isoformat()}", error))
  ordered_ids = sorted(ids, key=int)
  for start in range(0, len(ordered_ids), fetch_batch_size):
    batch = ordered_ids[start : start + fetch_batch_size]
    try:
      payload = client.get_bytes(
        PUBMED_EFETCH,
        params={**common, "retmode": "xml", "id": ",".join(batch)},
        min_interval=interval,
      )
      parsed = parse_pubmed_xml(payload)
      returned_ids = _pubmed_payload_pmids(payload)
    except Exception as error:
      result.errors.append(_failure("pubmed", f"fetch IDs {batch[0]}..{batch[-1]}", error))
      continue
    missing_ids = set(batch) - returned_ids
    unexpected_ids = returned_ids - set(batch)
    unparsed_ids = returned_ids.intersection(batch) - {record.pmid for record in parsed}
    if missing_ids or unexpected_ids or unparsed_ids:
      details: list[str] = []
      if missing_ids:
        details.append(f"{len(missing_ids)} IDs absent from EFetch")
      if unexpected_ids:
        details.append(f"{len(unexpected_ids)} unexpected IDs returned by EFetch")
      if unparsed_ids:
        details.append(f"{len(unparsed_ids)} returned records could not be normalized")
      result.errors.append(
        SourceFailure(
          "pubmed",
          f"fetch IDs {batch[0]}..{batch[-1]}",
          "; ".join(details),
          retryable=True,
        )
      )
    for record in parsed:
      if record.pmid not in batch:
        result.skipped += 1
        continue
      if record.pmid in managed_ids or window.includes_logical_timestamp(record.created_at):
        result.records.append(record)
      else:
        result.skipped += 1
  result.records = deduplicate_records(result.records)
  return result


def parse_arxiv_atom(payload: bytes) -> tuple[list[PaperRecord], int]:
  root = ET.fromstring(payload)
  total_text = _xml_text(root.find(f"{OPENSEARCH}totalResults"))
  total = int(total_text or 0)
  records: list[PaperRecord] = []
  for entry in root.findall(f"{ATOM}entry"):
    raw_id = _xml_text(entry.find(f"{ATOM}id"))
    arxiv_id = normalize_arxiv_id(raw_id)
    if not arxiv_id:
      continue
    title = _xml_text(entry.find(f"{ATOM}title"))
    abstract = _xml_text(entry.find(f"{ATOM}summary"))
    if not title or not abstract:
      continue
    authors = tuple(
      _xml_text(author.find(f"{ATOM}name"))
      for author in entry.findall(f"{ATOM}author")
      if _xml_text(author.find(f"{ATOM}name"))
    )
    primary = entry.find(f"{ARXIV}primary_category")
    categories = tuple(
      node.attrib.get("term", "")
      for node in entry.findall(f"{ATOM}category")
      if node.attrib.get("term")
    )
    doi = normalize_doi(_xml_text(entry.find(f"{ARXIV}doi")))
    records.append(
      PaperRecord(
        source="arxiv",
        source_id=arxiv_id,
        title=title,
        abstract=abstract,
        authors=authors,
        venue=_xml_text(entry.find(f"{ARXIV}journal_ref")) or "arXiv",
        created_at=ensure_utc(_xml_text(entry.find(f"{ATOM}published"))),
        updated_at=ensure_utc(_xml_text(entry.find(f"{ATOM}updated"))),
        url=f"https://arxiv.org/abs/{arxiv_id}",
        doi=doi,
        arxiv_id=arxiv_id,
        version=arxiv_version(raw_id),
        categories=categories,
        metadata={
          "primary_category": primary.attrib.get("term", "") if primary is not None else "",
          "timestamp_precision": "second",
        },
      )
    )
  return records, total


def fetch_arxiv(
  window: FetchWindow,
  client: HttpClientProtocol,
  *,
  page_size: int = ARXIV_PAGE_SIZE,
  categories: Sequence[str] = ARXIV_CATEGORY_FAMILIES,
) -> SourceResult:
  # arXiv permits slices of up to 2,000 results. A moderate default keeps
  # responses bounded while avoiding five requests where one is sufficient
  # for a typical recovery window, reducing exposure to shared-IP throttling.
  page_size = min(max(1, page_size), 1_000)
  result = SourceResult("arxiv")
  category_query = " OR ".join(f"cat:{category}" for category in categories)
  start_stamp = window.query_since.strftime("%Y%m%d%H%M")
  end_stamp = (window.until - timedelta(microseconds=1)).strftime("%Y%m%d%H%M")
  query = f"({category_query}) AND lastUpdatedDate:[{start_stamp} TO {end_stamp}]"
  offset = 0
  total = math.inf
  page_fingerprints: set[tuple[str, str, int]] = set()
  while offset < total:
    try:
      payload = client.get_bytes(
        ARXIV_API,
        params={
          "search_query": query,
          "start": offset,
          "max_results": page_size,
          "sortBy": "lastUpdatedDate",
          "sortOrder": "ascending",
        },
        min_interval=3.1,
      )
      records, page_total = parse_arxiv_atom(payload)
      entries = ET.fromstring(payload).findall(f"{ATOM}entry")
      entry_count = len(entries)
    except Exception as error:
      result.errors.append(_failure("arxiv", f"page at {offset}", error))
      break
    if math.isinf(total):
      total = page_total
    elif page_total != total:
      result.errors.append(
        SourceFailure(
          "arxiv",
          f"page at {offset}",
          f"arXiv result count changed during pagination ({int(total)} to {page_total})",
          retryable=True,
        )
      )
      break
    if not entry_count:
      if offset < total:
        result.errors.append(
          SourceFailure(
            "arxiv",
            f"page at {offset}",
            f"arXiv pagination ended at {offset} of {int(total)} records",
            retryable=True,
          )
        )
      break
    raw_ids = [_xml_text(entry.find(f"{ATOM}id")) for entry in entries]
    fingerprint = (raw_ids[0], raw_ids[-1], entry_count)
    if fingerprint in page_fingerprints:
      result.errors.append(
        SourceFailure(
          "arxiv",
          f"page at {offset}",
          "arXiv repeated a result page",
          retryable=True,
        )
      )
      break
    page_fingerprints.add(fingerprint)
    for record in records:
      if window.includes_query_timestamp(record.updated_at or record.created_at):
        result.records.append(record)
      else:
        result.skipped += 1
    result.skipped += entry_count - len(records)
    offset += entry_count
  result.records = deduplicate_records(result.records)
  return result


def _authors(value: Any) -> tuple[str, ...]:
  if isinstance(value, list):
    names: list[str] = []
    for author in value:
      if isinstance(author, Mapping):
        given = author.get("firstName") or author.get("given") or ""
        family = author.get("lastName") or author.get("family") or ""
        name = clean_text(f"{given} {family}")
      else:
        name = clean_text(author)
      if name:
        names.append(name)
    return tuple(names)
  text = clean_text(value)
  return tuple(clean_text(item) for item in text.split(";") if clean_text(item))


def parse_rxiv_item(item: Mapping[str, Any], server: str, *, publication: bool = False) -> PaperRecord:
  if server not in {"biorxiv", "medrxiv"}:
    raise ValueError(f"unsupported Rxiv server: {server}")
  published: datetime | None = None
  if publication:
    preprint_doi = normalize_doi(item.get("preprint_doi") or item.get("biorxiv_doi"))
    published_doi = normalize_doi(item.get("published_doi"))
    doi = published_doi or preprint_doi
    title = clean_text(item.get("preprint_title"))
    abstract = clean_text(item.get("preprint_abstract"))
    created = ensure_utc(item.get("preprint_date"))
    published = ensure_utc(item.get("published_date"))
    updated = published or created
    authors = _authors(item.get("preprint_authors"))
    category = clean_text(item.get("preprint_category"))
    venue = clean_text(item.get("published_journal")) or server
    related = (f"doi:{preprint_doi}",) if preprint_doi and preprint_doi != doi else ()
    version = ""
    license_name = ""
    kind = "publication-relation"
  else:
    preprint_doi = normalize_doi(item.get("doi"))
    published_doi = normalize_doi(item.get("published"))
    doi = published_doi or preprint_doi
    title = clean_text(item.get("title"))
    abstract = clean_text(item.get("abstract"))
    created = ensure_utc(item.get("date"))
    updated = created
    authors = _authors(item.get("authors"))
    category = clean_text(item.get("category"))
    venue = server
    related = (f"doi:{preprint_doi}",) if published_doi and preprint_doi else ()
    version = clean_text(item.get("version"))
    license_name = clean_text(item.get("license"))
    kind = "preprint-version"
  if not doi:
    raise ValueError(f"{server} item has no DOI")
  suffix = f"v{version}" if version and version.isdigit() else ""
  source_id = preprint_doi
  url = (
    f"https://doi.org/{doi}"
    if published_doi
    else f"https://www.{server}.org/content/{source_id}{suffix}"
  )
  return PaperRecord(
    source=server,
    source_id=source_id,
    title=title,
    abstract=abstract,
    authors=authors,
    venue=venue,
    created_at=created,
    updated_at=updated,
    url=url,
    doi=doi,
    version=version,
    categories=(category,) if category else (),
    related_ids=related,
    license=license_name,
    metadata={
      "record_kind": kind,
      "timestamp_precision": "day",
      **(
        {
          "publication_year": updated.year,
          "preprint_date": created.date().isoformat(),
          **({"publication_date": published.date().isoformat()} if published else {}),
        }
        if publication and updated and created
        else (
          {
            "publication_year": updated.year,
            **({"publication_date": published.date().isoformat()} if published else {}),
          }
          if publication and updated
          else {}
        )
      ),
    },
  )


def _rxiv_pages(
  result: SourceResult,
  window: FetchWindow,
  client: HttpClientProtocol,
  *,
  server: str,
  endpoint: str,
  publication: bool,
) -> None:
  start = window.query_since.date().isoformat()
  end = window.query_end_date.isoformat()
  cursor = 0
  expected_total: int | None = None
  page_fingerprints: set[str] = set()
  while True:
    try:
      payload = client.get_json(
        f"{RXIV_API}/{endpoint}/{server}/{start}/{end}/{cursor}", min_interval=0.1
      )
      collection = payload.get("collection", [])
      messages = payload.get("messages", [])
    except Exception as error:
      result.errors.append(_failure(server, f"{endpoint} page at {cursor}", error))
      return
    total = 0
    if messages:
      message = messages[0] if isinstance(messages, list) else messages
      try:
        total = int(message.get("total", message.get("count", 0)))
      except (AttributeError, TypeError, ValueError):
        total = 0
    if total:
      if expected_total is None:
        expected_total = total
      elif total != expected_total:
        result.errors.append(
          SourceFailure(
            server,
            f"{endpoint} page at {cursor}",
            f"{server} result count changed during pagination "
            f"({expected_total} to {total})",
            retryable=True,
          )
        )
        return
    if not collection:
      if expected_total is not None and cursor < expected_total:
        result.errors.append(
          SourceFailure(
            server,
            f"{endpoint} page at {cursor}",
            f"{server} pagination ended at {cursor} of {expected_total} records",
            retryable=True,
          )
        )
      return
    fingerprint = hashlib.sha256(
      json.dumps(collection, sort_keys=True, ensure_ascii=False, default=str).encode()
    ).hexdigest()
    if fingerprint in page_fingerprints:
      result.errors.append(
        SourceFailure(
          server,
          f"{endpoint} page at {cursor}",
          f"{server} repeated a result page",
          retryable=True,
        )
      )
      return
    page_fingerprints.add(fingerprint)
    for item in collection:
      try:
        record = parse_rxiv_item(item, server, publication=publication)
      except (TypeError, ValueError) as error:
        result.errors.append(_failure(server, f"parse {endpoint} record", error))
        continue
      if not record.abstract:
        result.skipped += 1
      elif window.includes_query_date(record.updated_at or record.created_at):
        result.records.append(record)
      else:
        result.skipped += 1
    cursor += len(collection)
    if expected_total is not None and cursor >= expected_total:
      return


def fetch_rxiv(
  window: FetchWindow,
  client: HttpClientProtocol,
  *,
  server: str,
  include_publications: bool = True,
) -> SourceResult:
  result = SourceResult(server)
  _rxiv_pages(
    result, window, client, server=server, endpoint="details", publication=False
  )
  if include_publications:
    _rxiv_pages(result, window, client, server=server, endpoint="pubs", publication=True)
  result.records = deduplicate_records(result.records)
  return result


def parse_chemrxiv_item(value: Mapping[str, Any]) -> PaperRecord:
  item = value.get("item", value)
  if not isinstance(item, Mapping):
    raise ValueError("ChemRxiv item is not an object")
  item_id = clean_text(item.get("id"))
  preprint_doi = normalize_doi(item.get("doi"))
  authors = _authors(item.get("authors", []))
  category_names: list[str] = []
  for category in item.get("categories") or []:
    name = (
      clean_text(category.get("name")) if isinstance(category, Mapping) else clean_text(category)
    )
    if name:
      category_names.append(name)
  related: list[str] = []
  vor = item.get("vor") or {}
  published_doi = ""
  published_url = ""
  if isinstance(vor, Mapping):
    published_doi = normalize_doi(vor.get("vorDoi") or vor.get("doi"))
    published_url = clean_text(vor.get("url"))
    if published_doi:
      related.append(f"doi:{preprint_doi}")
  doi = published_doi or preprint_doi
  for version_ref in item.get("versionRefs") or []:
    if isinstance(version_ref, Mapping) and version_ref.get("itemId"):
      related.append(f"chemrxiv:{clean_text(version_ref['itemId'])}")
  license_value = item.get("license") or {}
  license_name = (
    clean_text(license_value.get("name") or license_value.get("url"))
    if isinstance(license_value, Mapping)
    else clean_text(license_value)
  )
  origin = clean_text(item.get("origin"))
  return PaperRecord(
    source="chemrxiv",
    source_id=item_id or preprint_doi,
    title=clean_text(item.get("title")),
    abstract=clean_text(item.get("abstract")),
    authors=authors,
    venue="ChemRxiv",
    created_at=ensure_utc(item.get("submittedDate") or item.get("publishedDate")),
    updated_at=ensure_utc(
      item.get("statusDate") or item.get("publishedDate") or item.get("approvedDate")
    ),
    url=(published_url or f"https://doi.org/{published_doi}")
    if published_doi
    else f"https://chemrxiv.org/engage/chemrxiv/article-details/{item_id}",
    doi=doi,
    version=clean_text(item.get("version")) or chemrxiv_version(preprint_doi),
    categories=tuple(category_names),
    related_ids=tuple(related),
    license=license_name,
    metadata={
      "origin": origin,
      "timestamp_precision": "millisecond",
      "record_kind": "publication-relation" if published_doi else "preprint-version",
      "preprint_doi": preprint_doi,
    },
  )


def _crossref_date(value: Any) -> datetime | None:
  if not isinstance(value, Mapping):
    return None
  if value.get("date-time"):
    return ensure_utc(str(value["date-time"]))
  parts = value.get("date-parts") or []
  if not parts or not isinstance(parts[0], Sequence) or not parts[0]:
    return None
  values = list(parts[0])
  try:
    year = int(values[0])
    month = int(values[1]) if len(values) > 1 else 1
    day = int(values[2]) if len(values) > 2 else 1
    return datetime(year, month, day, tzinfo=UTC)
  except (TypeError, ValueError):
    return None


def parse_crossref_chemrxiv_item(item: Mapping[str, Any]) -> PaperRecord:
  """Normalize a ChemRxiv Crossref deposit when Open Engage blocks listing."""

  preprint_doi = normalize_doi(item.get("DOI"))
  if not preprint_doi or not preprint_doi.startswith("10.26434/"):
    raise ValueError("Crossref item is not a ChemRxiv DOI")
  title_values = item.get("title") or []
  title = clean_text(title_values[0] if isinstance(title_values, list) and title_values else title_values)
  authors = _authors(item.get("author") or [])
  relation = item.get("relation") or {}
  published_doi = ""
  if isinstance(relation, Mapping):
    for relation_name in ("is-preprint-of", "is-version-of"):
      candidates = relation.get(relation_name) or []
      if isinstance(candidates, Mapping):
        candidates = [candidates]
      for candidate in candidates:
        if not isinstance(candidate, Mapping):
          continue
        candidate_doi = normalize_doi(candidate.get("id"))
        if candidate_doi and not candidate_doi.startswith("10.26434/"):
          published_doi = candidate_doi
          break
      if published_doi:
        break
  doi = published_doi or preprint_doi
  created = (
    _crossref_date(item.get("posted"))
    or _crossref_date(item.get("created"))
    or _crossref_date(item.get("issued"))
  )
  updated = _crossref_date(item.get("deposited")) or _crossref_date(item.get("indexed")) or created
  resource = item.get("resource") or {}
  primary_url = ""
  if isinstance(resource, Mapping) and isinstance(resource.get("primary"), Mapping):
    primary_url = clean_text(resource["primary"].get("URL"))
  licenses = item.get("license") or []
  license_value = ""
  if isinstance(licenses, list) and licenses and isinstance(licenses[0], Mapping):
    license_value = clean_text(licenses[0].get("URL"))
  return PaperRecord(
    source="chemrxiv",
    source_id=preprint_doi,
    title=title,
    abstract=clean_text(item.get("abstract")),
    authors=authors,
    venue="ChemRxiv",
    created_at=created,
    updated_at=updated,
    url=f"https://doi.org/{published_doi}" if published_doi else primary_url or f"https://doi.org/{preprint_doi}",
    doi=doi,
    version=chemrxiv_version(preprint_doi),
    related_ids=(f"doi:{preprint_doi}",) if published_doi else (),
    license=license_value,
    metadata={
      "record_kind": "publication-relation" if published_doi else "preprint-version",
      "timestamp_precision": "second" if updated and updated.time() else "day",
      "preprint_doi": preprint_doi,
      "crossref_indexed": (_crossref_date(item.get("indexed")) or updated).isoformat()
      if (_crossref_date(item.get("indexed")) or updated)
      else "",
    },
  )


def _fetch_chemrxiv_crossref(
  window: FetchWindow,
  client: HttpClientProtocol,
  *,
  rows: int = 1_000,
) -> SourceResult:
  result = SourceResult("chemrxiv")
  cursor = "*"
  processed = 0
  total = math.inf
  fingerprints: set[tuple[str, str, int]] = set()
  while processed < total:
    try:
      payload = client.get_json(
        CHEMRXIV_CROSSREF_API,
        params={
          "filter": ",".join(
            (
              "prefix:10.26434",
              "type:posted-content",
              f"from-update-date:{window.query_since.date().isoformat()}",
              f"until-update-date:{window.query_end_date.isoformat()}",
            )
          ),
          "rows": min(max(1, rows), 1_000),
          "cursor": cursor,
        },
        headers={"Accept": "application/json"},
        min_interval=0.1,
      )
      message = payload.get("message", {})
      items = message.get("items", [])
      page_total = int(message.get("total-results", len(items)))
      next_cursor = clean_text(message.get("next-cursor"))
    except Exception as error:
      result.errors.append(_failure("chemrxiv", f"Crossref page after {processed}", error))
      break
    if math.isinf(total):
      total = page_total
    elif page_total != total:
      result.errors.append(
        SourceFailure(
          "chemrxiv",
          f"Crossref page after {processed}",
          f"Crossref result count changed during pagination ({int(total)} to {page_total})",
          retryable=True,
        )
      )
      break
    if not items:
      if processed < total:
        result.errors.append(
          SourceFailure(
            "chemrxiv",
            "Crossref pagination",
            f"Crossref ended at {processed} of {total} ChemRxiv updates",
            retryable=True,
          )
        )
      break
    first_doi = normalize_doi(items[0].get("DOI")) if isinstance(items[0], Mapping) else ""
    last_doi = normalize_doi(items[-1].get("DOI")) if isinstance(items[-1], Mapping) else ""
    fingerprint = (first_doi, last_doi, len(items))
    if fingerprint in fingerprints:
      result.errors.append(
        SourceFailure(
          "chemrxiv", "Crossref pagination", "Crossref repeated a ChemRxiv cursor page", True
        )
      )
      break
    fingerprints.add(fingerprint)
    for item in items:
      try:
        record = parse_crossref_chemrxiv_item(item)
        if not record.abstract:
          detail_url = f"{CHEMRXIV_DETAIL_API}/{urllib.parse.quote(record.metadata['preprint_doi'], safe='/')}"
          try:
            detail = client.get_json(
              detail_url,
              headers={"Accept": "application/json", "Accept-Encoding": "identity"},
              min_interval=0.1,
            )
          except HttpRequestError as error:
            # Crossref retains deposits for withdrawn and legacy versions that
            # Open Engage no longer exposes.  They cannot be embedded without
            # an abstract, but their permanent absence does not make the
            # successfully paginated Crossref feed incomplete.
            if error.status in {404, 410}:
              result.skipped += 1
              continue
            raise
          record = parse_chemrxiv_item(detail)
      except Exception as error:
        result.errors.append(_failure("chemrxiv", "parse/hydrate Crossref record", error))
        continue
      if record.abstract:
        # Crossref's update-date filter selected this record. Retain the stable
        # provider timestamps in the record so overlap reruns remain no-ops.
        result.records.append(record)
      else:
        result.skipped += 1
    processed += len(items)
    if processed >= total:
      break
    if not next_cursor:
      result.errors.append(
        SourceFailure(
          "chemrxiv",
          "Crossref pagination",
          f"Crossref omitted a cursor at {processed} of {total} records",
          retryable=True,
        )
      )
      break
    cursor = next_cursor
  result.records = deduplicate_records(result.records)
  return result


def _fetch_chemrxiv_endpoint(
  window: FetchWindow,
  client: HttpClientProtocol,
  *,
  base_url: str,
  require_origin: bool,
  page_size: int,
) -> SourceResult:
  result = SourceResult("chemrxiv")
  offset = 0
  total = math.inf
  page_fingerprints: set[str] = set()
  while offset < total:
    try:
      payload = client.get_json(
        base_url,
        params={
          "limit": page_size,
          "skip": offset,
          "searchDateFrom": window.query_since.date().isoformat(),
          "searchDateTo": window.query_end_date.isoformat(),
          "sort": "PUBLISHED_DATE_ASC",
        },
        headers={"Accept": "application/json", "Accept-Encoding": "identity"},
        min_interval=0.1,
      )
      hits = payload.get("itemHits", [])
      page_total = int(payload.get("totalCount", len(hits)))
    except Exception as error:
      result.errors.append(_failure("chemrxiv", f"page at {offset}", error))
      break
    if math.isinf(total):
      total = page_total
    elif page_total != total:
      result.errors.append(
        SourceFailure(
          "chemrxiv",
          f"page at {offset}",
          f"ChemRxiv result count changed during pagination ({int(total)} to {page_total})",
          retryable=True,
        )
      )
      break
    if not hits:
      if offset < total:
        result.errors.append(
          SourceFailure(
            "chemrxiv",
            f"page at {offset}",
            f"ChemRxiv pagination ended at {offset} of {int(total)} records",
            retryable=True,
          )
        )
      break
    fingerprint = hashlib.sha256(
      json.dumps(hits, sort_keys=True, ensure_ascii=False, default=str).encode()
    ).hexdigest()
    if fingerprint in page_fingerprints:
      result.errors.append(
        SourceFailure(
          "chemrxiv",
          f"page at {offset}",
          "ChemRxiv repeated a result page",
          retryable=True,
        )
      )
      break
    page_fingerprints.add(fingerprint)
    for hit in hits:
      raw = hit.get("item", hit) if isinstance(hit, Mapping) else {}
      origin = clean_text(raw.get("origin")) if isinstance(raw, Mapping) else ""
      if require_origin and origin.casefold() != "chemrxiv":
        result.skipped += 1
        continue
      try:
        record = parse_chemrxiv_item(hit)
      except (TypeError, ValueError) as error:
        result.errors.append(_failure("chemrxiv", "parse record", error))
        continue
      if not record.abstract:
        result.skipped += 1
      elif window.includes_query_timestamp(record.updated_at or record.created_at):
        result.records.append(record)
      else:
        result.skipped += 1
    offset += len(hits)
  result.records = deduplicate_records(result.records)
  return result


def fetch_chemrxiv(
  window: FetchWindow, client: HttpClientProtocol, *, page_size: int = 50
) -> SourceResult:
  page_size = min(max(1, page_size), 50)
  primary = _fetch_chemrxiv_endpoint(
    window, client, base_url=CHEMRXIV_API, require_origin=False, page_size=page_size
  )
  if not primary.errors:
    return primary
  fallback = _fetch_chemrxiv_crossref(window, client)
  if fallback.ok and (fallback.records or not primary.records):
    return SourceResult(
      "chemrxiv",
      records=deduplicate_records([*primary.records, *fallback.records]),
      skipped=primary.skipped + fallback.skipped,
    )
  return SourceResult(
    "chemrxiv",
    records=deduplicate_records([*primary.records, *fallback.records]),
    errors=[*primary.errors, *fallback.errors],
    skipped=primary.skipped + fallback.skipped,
  )


Fetcher = Callable[[FetchWindow, HttpClientProtocol], SourceResult]


def _fetch_source(
  name: str,
  fetcher: Fetcher,
  window: FetchWindow,
  client: HttpClientProtocol,
) -> SourceResult:
  try:
    return fetcher(window, client)
  except Exception as error:
    return SourceResult(name, errors=[_failure(name, "fetch", error)])


def fetch_all_sources(
  window: FetchWindow,
  *,
  client: HttpClientProtocol | None = None,
  contact_email: str = "",
  ncbi_api_key: str = "",
  known_pubmed_ids: Iterable[str] = (),
  fetchers: Mapping[str, Fetcher] | None = None,
  provider_retry_delays: Sequence[float] = PROVIDER_RETRY_DELAYS,
  sleep: Callable[[float], None] = time.sleep,
) -> FetchReport:
  """Fetch every feed independently and retry transient provider failures."""

  if any(delay < 0 for delay in provider_retry_delays):
    raise ValueError("provider retry delays cannot be negative")

  http = client or HttpClient(
    user_agent=f"SKM-paperbot/1.0 ({contact_email or 'https://github.com/delalamo/SKM'})"
  )
  providers: Mapping[str, Fetcher] = fetchers or {
    "pubmed": lambda fetch_window, fetch_client: fetch_pubmed(
      fetch_window,
      fetch_client,
      contact_email=contact_email,
      api_key=ncbi_api_key,
      known_pubmed_ids=known_pubmed_ids,
    ),
    "arxiv": fetch_arxiv,
    "biorxiv": lambda fetch_window, fetch_client: fetch_rxiv(
      fetch_window, fetch_client, server="biorxiv"
    ),
    "medrxiv": lambda fetch_window, fetch_client: fetch_rxiv(
      fetch_window, fetch_client, server="medrxiv"
    ),
    "chemrxiv": fetch_chemrxiv,
  }
  results: list[SourceResult] = []
  for name, fetcher in providers.items():
    print(f"paperbot: fetching {name}", flush=True)
    source_result = _fetch_source(name, fetcher, window, http)
    print(
      f"paperbot: completed {name}: {len(source_result.records)} records, "
      f"{len(source_result.errors)} errors",
      flush=True,
    )
    for retry_number, delay in enumerate(provider_retry_delays, start=1):
      if not any(error.retryable for error in source_result.errors):
        break
      print(
        f"paperbot: retrying {name} in {delay:g} seconds "
        f"(retry {retry_number}/{len(provider_retry_delays)})",
        flush=True,
      )
      sleep(delay)
      retried = _fetch_source(name, fetcher, window, http)
      source_result = SourceResult(
        name,
        records=deduplicate_records([*source_result.records, *retried.records]),
        errors=retried.errors,
        skipped=source_result.skipped + retried.skipped,
      )
      print(
        f"paperbot: completed {name} retry {retry_number}: "
        f"{len(source_result.records)} records, {len(source_result.errors)} errors",
        flush=True,
      )
    results.append(source_result)
  records = deduplicate_records(
    record for source_result in results for record in source_result.records
  )
  return FetchReport(
    window=window,
    records=tuple(records),
    errors=tuple(error for source_result in results for error in source_result.errors),
    source_counts={source_result.source: len(source_result.records) for source_result in results},
  )


fetch_daily_candidates = fetch_all_sources


__all__ = [
  "ARXIV_API",
  "CHEMRXIV_API",
  "FetchReport",
  "FetchWindow",
  "HttpClient",
  "HttpRequestError",
  "HttpResponse",
  "SourceFailure",
  "SourceResult",
  "fetch_all_sources",
  "fetch_arxiv",
  "fetch_chemrxiv",
  "fetch_daily_candidates",
  "fetch_pubmed",
  "fetch_rxiv",
  "parse_arxiv_atom",
  "parse_chemrxiv_item",
  "parse_pubmed_xml",
  "parse_rxiv_item",
]
