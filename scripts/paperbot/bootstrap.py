"""Build a deterministic, frozen set of biological PubMed negatives."""

from __future__ import annotations

import hashlib
import json
import os
import re
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from datetime import UTC, date, datetime, timedelta
from pathlib import Path
from typing import AbstractSet, Callable, Iterable, Mapping, Sequence

from .bibliography import (
  canonicalize_entries,
  entry_identifiers,
  load_bibliography,
  normalize_abstract,
  normalize_doi,
  normalize_title,
)
from .config import PaperbotConfig
from .citation_graph import (
  SemanticScholarClient,
  audit_negative_graph_distance,
  positive_identifiers_from_works,
)
from .negative_policy import (
  NEGATIVE_DATASET,
  NEGATIVE_END_YEAR,
  NEGATIVE_GROUPS,
  NEGATIVE_START_YEAR,
  MANUALLY_EXCLUDED_PMIDS,
  TARGET_MESH_HEADINGS,
  TARGET_TEXT_PHRASES,
  TARGET_TEXT_RE,
  is_target_topic,
)


PUBMED_ESEARCH = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
PUBMED_EFETCH = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
PUBMED_SEARCH_LIMIT = 9_999
CANDIDATE_POOL_MULTIPLIER = 10
EFETCH_BATCH_SIZE = 200

# Compatibility aliases for corpus-audit callers.  They now express the
# PubMed target-topic policy rather than the retired arXiv category policy.
BLOCKED_TEXT = TARGET_TEXT_RE
BLOCKED_CATEGORY_PREFIXES: tuple[str, ...] = ()


@dataclass(frozen=True)
class PubmedMetadata:
  pmid: str
  doi: str
  title: str
  abstract: str
  authors: tuple[str, ...]
  mesh_headings: tuple[str, ...]
  major_topics: tuple[str, ...]
  publication_types: tuple[str, ...]
  languages: tuple[str, ...]
  published_year: int
  journal: str
  medline_status: str
  url: str


@dataclass(frozen=True)
class BibliographyIdentityIndex:
  identifiers: frozenset[str]
  normalized_titles: frozenset[str]


def _xml_text(node: ET.Element | None) -> str:
  if node is None:
    return ""
  return " ".join("".join(node.itertext()).split())


def _publication_year(article: ET.Element) -> int:
  candidates = (
    article.find("./MedlineCitation/Article/ArticleDate/Year"),
    article.find("./MedlineCitation/Article/Journal/JournalIssue/PubDate/Year"),
    article.find("./MedlineCitation/DateCompleted/Year"),
    article.find("./MedlineCitation/DateCreated/Year"),
  )
  for node in candidates:
    value = _xml_text(node)
    if value.isdigit() and len(value) == 4:
      return int(value)
  medline_date = _xml_text(
    article.find("./MedlineCitation/Article/Journal/JournalIssue/PubDate/MedlineDate")
  )
  match = re.search(r"(?:19|20)\d{2}", medline_date)
  return int(match.group(0)) if match else 0


def parse_pubmed_feed(payload: bytes) -> list[PubmedMetadata]:
  """Parse the PubMed fields needed to audit and reproduce the corpus."""

  root = ET.fromstring(payload)
  records: list[PubmedMetadata] = []
  for item in root.findall("./PubmedArticle"):
    citation = item.find("./MedlineCitation")
    if citation is None:
      continue
    pmid = re.sub(r"\D", "", _xml_text(citation.find("./PMID")))
    title = _xml_text(citation.find("./Article/ArticleTitle"))
    abstract_parts: list[str] = []
    abstract_nodes = citation.findall("./Article/Abstract/AbstractText")
    if not abstract_nodes:
      abstract_nodes = citation.findall("./OtherAbstract/AbstractText")
    for node in abstract_nodes:
      value = _xml_text(node)
      label = " ".join(
        (node.attrib.get("Label") or node.attrib.get("NlmCategory") or "").split()
      )
      if value:
        abstract_parts.append(
          f"{label}: {value}" if label and not value.startswith(f"{label}:") else value
        )
    abstract = normalize_abstract(" ".join(abstract_parts))

    authors: list[str] = []
    for author in citation.findall("./Article/AuthorList/Author"):
      collective = _xml_text(author.find("./CollectiveName"))
      if collective:
        authors.append(collective)
        continue
      family = _xml_text(author.find("./LastName"))
      given = _xml_text(author.find("./ForeName")) or _xml_text(author.find("./Initials"))
      name = ", ".join(value for value in (family, given) if value)
      if name:
        authors.append(name)

    doi = ""
    for identifier in item.findall("./PubmedData/ArticleIdList/ArticleId"):
      if identifier.attrib.get("IdType", "").casefold() == "doi":
        doi = normalize_doi(_xml_text(identifier))
        if doi:
          break

    mesh_headings: list[str] = []
    major_topics: list[str] = []
    for heading in citation.findall("./MeshHeadingList/MeshHeading"):
      descriptor = heading.find("./DescriptorName")
      name = _xml_text(descriptor)
      if not name:
        continue
      mesh_headings.append(name)
      if descriptor is not None and descriptor.attrib.get("MajorTopicYN", "N") == "Y":
        major_topics.append(name)

    publication_types = tuple(
      value
      for value in (
        _xml_text(node)
        for node in citation.findall("./Article/PublicationTypeList/PublicationType")
      )
      if value
    )
    languages = tuple(
      value.casefold()
      for value in (_xml_text(node) for node in citation.findall("./Article/Language"))
      if value
    )
    records.append(
      PubmedMetadata(
        pmid=pmid,
        doi=doi,
        title=title,
        abstract=abstract,
        authors=tuple(authors),
        mesh_headings=tuple(mesh_headings),
        major_topics=tuple(major_topics),
        publication_types=publication_types,
        languages=languages,
        published_year=_publication_year(item),
        journal=_xml_text(citation.find("./Article/Journal/Title")),
        medline_status=citation.attrib.get("Status", ""),
        url=f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/" if pmid else "",
      )
    )
  return records


def _request_bytes(url: str, user_agent: str, attempts: int = 5) -> bytes:
  for attempt in range(attempts):
    request = urllib.request.Request(url, headers={"User-Agent": user_agent})
    try:
      with urllib.request.urlopen(request, timeout=60) as response:
        return response.read()
    except urllib.error.HTTPError as error:
      if error.code != 429 and error.code < 500:
        raise
      if attempt == attempts - 1:
        raise
      retry_after = error.headers.get("Retry-After")
      delay = float(retry_after) if retry_after else min(60.0, 2.0**attempt)
    except (TimeoutError, urllib.error.URLError):
      if attempt == attempts - 1:
        raise
      delay = min(60.0, 2.0**attempt)
    time.sleep(delay)
  raise RuntimeError(f"failed to fetch {url}")


def _quoted(term: str, field: str) -> str:
  escaped = term.replace('"', r'\"')
  return f'"{escaped}"[{field}]'


def build_pubmed_query(
  major_topics: Sequence[str],
  *,
  start: date = date(NEGATIVE_START_YEAR, 1, 1),
  end: date = date(NEGATIVE_END_YEAR, 12, 31),
) -> str:
  """Return the explicit MEDLINE query used for one negative stratum."""

  if not major_topics:
    raise ValueError("a PubMed negative stratum must have a MeSH major topic")
  topic_query = " OR ".join(_quoted(topic, "majr") for topic in major_topics)
  target_mesh = " OR ".join(_quoted(topic, "mh") for topic in TARGET_MESH_HEADINGS)
  target_text = " OR ".join(_quoted(term, "tiab") for term in TARGET_TEXT_PHRASES)
  date_query = f'"{start:%Y/%m/%d}"[dp] : "{end:%Y/%m/%d}"[dp]'
  return (
    "medline[sb] AND english[la] AND hasabstract AND "
    '"Journal Article"[pt] AND '
    f"({topic_query}) AND ({date_query}) NOT ({target_mesh} OR {target_text})"
  )


def _eutils_url(endpoint: str, params: Mapping[str, object]) -> str:
  return f"{endpoint}?{urllib.parse.urlencode(params)}"


def _search_payload(payload: bytes) -> tuple[int, list[str]]:
  try:
    result = json.loads(payload).get("esearchresult", {})
    count = int(result["count"])
    ids = [str(value) for value in result.get("idlist", []) if str(value).isdigit()]
  except (AttributeError, KeyError, TypeError, ValueError, json.JSONDecodeError) as error:
    raise RuntimeError("PubMed ESearch returned an invalid response") from error
  return count, ids


def fetch_pubmed_ids(
  major_topics: Sequence[str],
  *,
  contact_email: str,
  api_key: str = "",
  request_bytes: Callable[[str, str], bytes] = _request_bytes,
  sleep: Callable[[float], None] = time.sleep,
) -> list[str]:
  """Exhaust a historical PubMed query without crossing its 9,999-ID cap."""

  user_agent = f"SKM-Paperbot/1.0 ({contact_email or 'https://github.com/delalamo/SKM'})"
  interval = 0.11 if api_key else 0.34

  def search(start: date, end: date) -> list[str]:
    params: dict[str, object] = {
      "db": "pubmed",
      "retmode": "json",
      "retmax": PUBMED_SEARCH_LIMIT,
      "term": build_pubmed_query(major_topics, start=start, end=end),
      "tool": "skm-paperbot",
    }
    if contact_email:
      params["email"] = contact_email
    if api_key:
      params["api_key"] = api_key
    count, ids = _search_payload(
      request_bytes(_eutils_url(PUBMED_ESEARCH, params), user_agent)
    )
    sleep(interval)
    if count <= PUBMED_SEARCH_LIMIT:
      if len(ids) != count:
        raise RuntimeError(
          f"PubMed ESearch returned {len(ids)} IDs for a reported {count} records"
        )
      return ids
    if start >= end:
      raise RuntimeError(
        f"PubMed query still exceeds {PUBMED_SEARCH_LIMIT} records on {start.isoformat()}"
      )
    midpoint = start + timedelta(days=(end - start).days // 2)
    return search(start, midpoint) + search(midpoint + timedelta(days=1), end)

  ids = search(date(NEGATIVE_START_YEAR, 1, 1), date(NEGATIVE_END_YEAR, 12, 31))
  # Date partitions are disjoint, but preserve first occurrence defensively.
  return list(dict.fromkeys(ids))


def _selection_hash(seed: str, group: str, pmid: str) -> str:
  return hashlib.sha256(f"{seed}{group}{pmid}".encode("utf-8")).hexdigest()


def fetch_pubmed_stratum(
  group: str,
  major_topics: Sequence[str],
  *,
  seed: str,
  contact_email: str,
  max_candidates: int,
  api_key: str = "",
  batch_size: int = EFETCH_BATCH_SIZE,
  request_bytes: Callable[[str, str], bytes] = _request_bytes,
  sleep: Callable[[float], None] = time.sleep,
) -> list[PubmedMetadata]:
  """Fetch a deterministic hash-ranked candidate pool for one stratum."""

  pmids = fetch_pubmed_ids(
    major_topics,
    contact_email=contact_email,
    api_key=api_key,
    request_bytes=request_bytes,
    sleep=sleep,
  )
  ranked_pmids = sorted(pmids, key=lambda pmid: (_selection_hash(seed, group, pmid), pmid))
  chosen_pmids = ranked_pmids[:max_candidates]
  user_agent = f"SKM-Paperbot/1.0 ({contact_email or 'https://github.com/delalamo/SKM'})"
  interval = 0.11 if api_key else 0.34
  records: list[PubmedMetadata] = []
  for start in range(0, len(chosen_pmids), batch_size):
    batch = chosen_pmids[start : start + batch_size]
    params: dict[str, object] = {
      "db": "pubmed",
      "retmode": "xml",
      "id": ",".join(batch),
      "tool": "skm-paperbot",
    }
    if contact_email:
      params["email"] = contact_email
    if api_key:
      params["api_key"] = api_key
    payload = request_bytes(_eutils_url(PUBMED_EFETCH, params), user_agent)
    records.extend(parse_pubmed_feed(payload))
    sleep(interval)
  by_pmid = {record.pmid: record for record in records}
  # Restore selection order; EFetch is not required to preserve request order.
  return [by_pmid[pmid] for pmid in chosen_pmids if pmid in by_pmid]


def bibliography_identity_index(path: Path | str) -> BibliographyIdentityIndex:
  entries = load_bibliography(path)
  identifiers = set().union(*(entry_identifiers(entry) for entry in entries)) if entries else set()
  titles = {
    normalize_title(work.title)
    for work in canonicalize_entries(entries)
    if normalize_title(work.title)
  }
  return BibliographyIdentityIndex(frozenset(identifiers), frozenset(titles))


def _bibliography_identity_hash(index: BibliographyIdentityIndex) -> str:
  payload = {
    "identifiers": sorted(index.identifiers),
    "titles": sorted(index.normalized_titles),
  }
  return hashlib.sha256(
    json.dumps(payload, ensure_ascii=False, separators=(",", ":"), sort_keys=True).encode(
      "utf-8"
    )
  ).hexdigest()


def _eligible(
  record: PubmedMetadata,
  major_topics: AbstractSet[str],
  bibliography: BibliographyIdentityIndex,
) -> bool:
  if not record.pmid or not record.title or not record.abstract:
    return False
  if record.pmid in MANUALLY_EXCLUDED_PMIDS:
    return False
  if record.medline_status.casefold() != "medline":
    return False
  if "eng" not in record.languages or "journal article" not in {
    value.casefold() for value in record.publication_types
  }:
    return False
  if not NEGATIVE_START_YEAR <= record.published_year <= NEGATIVE_END_YEAR:
    return False
  # PubMed MeSH searches explode a parent descriptor to narrower terms.  The
  # record therefore need not repeat the queried parent descriptor verbatim;
  # its membership in this stratum is established by ESearch.  Still require
  # completed MEDLINE major-topic evidence in the fetched record.
  if not major_topics or not record.major_topics:
    return False
  if is_target_topic(record.title, record.abstract, record.mesh_headings):
    return False
  identities = {f"pmid:{record.pmid}"}
  if record.doi:
    identities.add(f"doi:{normalize_doi(record.doi)}")
  if identities & bibliography.identifiers:
    return False
  title = normalize_title(record.title)
  return bool(title) and title not in bibliography.normalized_titles


def rank_negative_records(
  candidates: Mapping[str, Iterable[PubmedMetadata]],
  seed: str,
  *,
  bibliography: BibliographyIdentityIndex | None = None,
) -> dict[str, list[PubmedMetadata]]:
  """Return every eligible candidate in deterministic per-stratum order."""

  bibliography = bibliography or BibliographyIdentityIndex(frozenset(), frozenset())
  ranked: dict[str, list[PubmedMetadata]] = {}
  for group, (_quota, major_topics) in NEGATIVE_GROUPS.items():
    rows: list[tuple[str, PubmedMetadata, str]] = []
    seen_pmids: set[str] = set()
    seen_titles: set[str] = set()
    for record in candidates.get(group, ()):
      title = normalize_title(record.title)
      if (
        record.pmid in seen_pmids
        or title in seen_titles
        or not _eligible(record, set(major_topics), bibliography)
      ):
        continue
      seen_pmids.add(record.pmid)
      seen_titles.add(title)
      rows.append((_selection_hash(seed, group, record.pmid), record, title))
    rows.sort(key=lambda item: (item[0], item[1].pmid))
    ranked[group] = [record for _digest, record, _title in rows]
  return ranked


def _record_payload(
  record: PubmedMetadata,
  *,
  group: str,
  rank: int,
  seed: str,
  academic_graph: Mapping[str, object] | None = None,
) -> dict[str, object]:
  digest = _selection_hash(seed, group, record.pmid)
  payload: dict[str, object] = {
    "schema_version": 2,
    "dataset": NEGATIVE_DATASET,
    "group": group,
    "rank": rank,
    "selection_hash": digest,
    "paper_id": f"pmid:{record.pmid}",
    "work_id": f"pmid:{record.pmid}",
    "pmid": record.pmid,
    "doi": record.doi,
    "title": record.title,
    "abstract": record.abstract,
    "authors": list(record.authors),
    # Temporary compatibility with the generic model-corpus loader.
    "primary_category": group,
    "mesh_major_topics": list(record.major_topics),
    "mesh_headings": list(record.mesh_headings),
    "publication_types": list(record.publication_types),
    "languages": list(record.languages),
    "published_year": record.published_year,
    "journal": record.journal,
    "url": record.url,
    "abstract_sha256": hashlib.sha256(record.abstract.encode("utf-8")).hexdigest(),
    "source": "PubMed/MEDLINE",
    "abstract_rights": "Source rights retained; see the originating publication.",
  }
  if academic_graph is not None:
    payload["academic_graph"] = dict(academic_graph)
  return payload


def _graph_record(
  graph_audit: Mapping[str, object] | None,
  pmid: str,
) -> Mapping[str, object] | None:
  if graph_audit is None:
    return None
  value = graph_audit.get(f"pmid:{pmid}", graph_audit.get(pmid))
  if value is None:
    raise RuntimeError(f"missing academic-graph audit for accepted PubMed record {pmid}")
  if hasattr(value, "to_dict"):
    value = value.to_dict()  # type: ignore[union-attr]
  if not isinstance(value, Mapping):
    raise TypeError(f"academic-graph audit for PubMed record {pmid} is not a mapping")
  if value.get("accepted") is not True:
    raise RuntimeError(f"academic-graph audit did not accept PubMed record {pmid}")
  if str(value.get("pmid", "")) != pmid:
    raise RuntimeError(f"academic-graph audit is not bound to PubMed record {pmid}")
  if value.get("references_available") is not True or not isinstance(
    value.get("reference_count"), int
  ) or isinstance(value.get("reference_count"), bool) or int(
    value["reference_count"]
  ) <= 0:
    raise RuntimeError(
      f"academic-graph audit has no usable references for PubMed record {pmid}"
    )
  return value


def select_negative_records(
  candidates: Mapping[str, Iterable[PubmedMetadata]],
  seed: str,
  *,
  bibliography: BibliographyIdentityIndex | None = None,
  accepted_pmids: AbstractSet[str] | None = None,
  graph_audit: Mapping[str, object] | None = None,
) -> list[dict[str, object]]:
  """Fill fixed quotas from ranked candidates, optionally after graph audit."""

  if (accepted_pmids is None) != (graph_audit is None):
    raise ValueError(
      "accepted_pmids and graph_audit must either both be supplied or both be omitted"
    )

  ranked = rank_negative_records(candidates, seed, bibliography=bibliography)
  selected: list[dict[str, object]] = []
  used_pmids: set[str] = set()
  used_titles: set[str] = set()
  for group, (quota, _major_topics) in NEGATIVE_GROUPS.items():
    rows: list[PubmedMetadata] = []
    for record in ranked[group]:
      title = normalize_title(record.title)
      if record.pmid in used_pmids or title in used_titles:
        continue
      if (
        accepted_pmids is not None
        and record.pmid not in accepted_pmids
        and f"pmid:{record.pmid}" not in accepted_pmids
      ):
        continue
      rows.append(record)
      if len(rows) == quota:
        break
    if len(rows) < quota:
      qualifier = " graph-accepted" if accepted_pmids is not None else " eligible"
      raise RuntimeError(
        f"negative group {group} has {len(rows)}{qualifier} records; need {quota}"
      )
    used_pmids.update(record.pmid for record in rows)
    used_titles.update(normalize_title(record.title) for record in rows)
    selected.extend(
      _record_payload(
        record,
        group=group,
        rank=rank,
        seed=seed,
        academic_graph=_graph_record(graph_audit, record.pmid),
      )
      for rank, record in enumerate(rows[:quota], start=1)
    )
  return selected


def write_jsonl(path: Path, records: Iterable[dict[str, object]]) -> None:
  path.parent.mkdir(parents=True, exist_ok=True)
  with path.open("w", encoding="utf-8") as handle:
    for record in records:
      handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")


def bootstrap_negatives(
  config: PaperbotConfig,
  *,
  overwrite: bool = False,
  fetch_group: Callable[..., list[PubmedMetadata]] = fetch_pubmed_stratum,
  accepted_pmids: AbstractSet[str] | None = None,
  graph_audit: Mapping[str, object] | None = None,
  graph_metadata: Mapping[str, object] | None = None,
  graph_client: SemanticScholarClient | None = None,
) -> list[dict[str, object]]:
  """Fetch, select, and write the frozen PubMed negative corpus."""

  output = config.negative_corpus_path
  if output.exists() and not overwrite:
    raise FileExistsError(
      f"{output} already exists; {NEGATIVE_DATASET} is frozen (use --overwrite deliberately)"
    )
  bibliography = bibliography_identity_index(config.bibliography_path)
  api_key = os.getenv("NCBI_API_KEY", "")
  candidates: dict[str, list[PubmedMetadata]] = {}
  for group, (quota, major_topics) in NEGATIVE_GROUPS.items():
    candidates[group] = fetch_group(
      group,
      major_topics,
      seed=config.negative_seed,
      contact_email=config.contact_email,
      max_candidates=quota * CANDIDATE_POOL_MULTIPLIER,
      api_key=api_key,
    )
  ranked = rank_negative_records(candidates, config.negative_seed, bibliography=bibliography)
  if (accepted_pmids is None) != (graph_audit is None):
    raise ValueError(
      "accepted_pmids and graph_audit must either both be supplied or both be omitted"
    )
  if accepted_pmids is None:
    cache_value = os.getenv("PAPERBOT_SEMANTIC_SCHOLAR_CACHE", "").strip()
    cache_path = Path(cache_value) if cache_value else None
    semantic_scholar_key = os.getenv("SEMANTIC_SCHOLAR_API_KEY", "")
    client = graph_client or SemanticScholarClient(
      api_key=semantic_scholar_key,
      cache_path=cache_path,
      min_interval=1.05 if semantic_scholar_key else 2.5,
    )
    works = canonicalize_entries(load_bibliography(config.bibliography_path))
    negative_pmids = {
      f"pmid:{record.pmid}": record.pmid
      for rows in ranked.values()
      for record in rows
    }
    audit = audit_negative_graph_distance(
      positive_identifiers_from_works(works),
      negative_pmids,
      client=client,
    )
    accepted_pmids = frozenset(audit.accepted_ids)
    graph_audit = audit.records
    graph_metadata = audit.metadata()
  elif graph_metadata is None:
    graph_metadata = {
      "provider": "injected test audit",
      "accepted": len(accepted_pmids),
    }
  selected = select_negative_records(
    candidates,
    config.negative_seed,
    bibliography=bibliography,
    accepted_pmids=accepted_pmids,
    graph_audit=graph_audit,
  )
  write_jsonl(output, selected)
  metadata_path = config.negative_metadata_path
  metadata_path.write_text(
    json.dumps(
      {
        "schema_version": 2,
        "dataset": NEGATIVE_DATASET,
        "created_at": datetime.now(UTC).isoformat(),
        "seed": config.negative_seed,
        "count": len(selected),
        "groups": {
          name: quota for name, (quota, _major_topics) in NEGATIVE_GROUPS.items()
        },
        "mesh_major_topics": {
          name: list(major_topics)
          for name, (_quota, major_topics) in NEGATIVE_GROUPS.items()
        },
        "candidate_pool_multiplier": CANDIDATE_POOL_MULTIPLIER,
        "fetched_candidates": {
          name: len(records) for name, records in candidates.items()
        },
        "eligible_candidates": {
          name: len(records) for name, records in ranked.items()
        },
        "selection": "SHA256(seed + group + PMID)",
        "queries": {
          name: build_pubmed_query(major_topics)
          for name, (_quota, major_topics) in NEGATIVE_GROUPS.items()
        },
        "graph_filter_applied": True,
        "academic_graph": dict(graph_metadata),
        "target_mesh_exclusions": list(TARGET_MESH_HEADINGS),
        "target_text_exclusions": list(TARGET_TEXT_PHRASES),
        "manually_excluded_pmids": sorted(MANUALLY_EXCLUDED_PMIDS),
        "source": "PubMed/MEDLINE via NCBI E-utilities",
        "source_window": [f"{NEGATIVE_START_YEAR}-01-01", f"{NEGATIVE_END_YEAR}-12-31"],
        "common_query": "medline[sb] AND english[la] AND hasabstract AND Journal Article[pt]",
        "bibliography_identifier_count": len(bibliography.identifiers),
        "bibliography_title_count": len(bibliography.normalized_titles),
        "audited_bibliography_identity_hash": _bibliography_identity_hash(
          bibliography
        ),
        "abstract_rights": "Source rights retained; see the originating publication.",
      },
      indent=2,
      sort_keys=True,
    )
    + "\n",
    encoding="utf-8",
  )
  return selected


def load_negative_records(path: Path) -> list[dict[str, object]]:
  records: list[dict[str, object]] = []
  with path.open(encoding="utf-8") as handle:
    for line in handle:
      if line.strip():
        records.append(json.loads(line))
  return records


__all__ = [
  "BibliographyIdentityIndex",
  "BLOCKED_CATEGORY_PREFIXES",
  "BLOCKED_TEXT",
  "CANDIDATE_POOL_MULTIPLIER",
  "NEGATIVE_GROUPS",
  "PUBMED_EFETCH",
  "PUBMED_ESEARCH",
  "PubmedMetadata",
  "bibliography_identity_index",
  "bootstrap_negatives",
  "build_pubmed_query",
  "fetch_pubmed_ids",
  "fetch_pubmed_stratum",
  "load_negative_records",
  "parse_pubmed_feed",
  "rank_negative_records",
  "select_negative_records",
  "write_jsonl",
]
