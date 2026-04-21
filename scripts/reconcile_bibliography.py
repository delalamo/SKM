#!/usr/bin/env python3
from __future__ import annotations

import argparse
import html
import json
import re
import sys
import time
import unicodedata
import urllib.parse
import urllib.request
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from utils import REPO_ROOT

CONTENT_DIR = REPO_ROOT / "content"
BIB_PATH = REPO_ROOT / "bibliography.bib"
CACHE_PATH = Path("/tmp/skm-citation-metadata-cache.json")
USER_AGENT = "SKM Citation Reconciler/1.0 (mailto:codex@example.com)"

RAW_DOI_RE = re.compile(r"(?:https?://)?doi\.org/(10\.[^\s\]>*]+)", re.IGNORECASE)
BARE_DOI_RE = re.compile(r"(?<![@\w])(10\.\d{4,9}/[^\s\]>*]+)", re.IGNORECASE)
FOOTNOTE_DEF_RE = re.compile(r"^\[\^(?P<key>[A-Za-z0-9_-]+)\]:(?P<body>.*)$", re.MULTILINE)
WIKILINK_RE = re.compile(r"\[\[([^\]|]+)\|([^\]]*?\b(?:19|20)\d{2}[a-z]?[^\]]*)\]\]")
PANDOC_CITE_RE = re.compile(r"@([A-Za-z0-9_-]+)")
OPENREVIEW_ID_RE = re.compile(r"^[A-Za-z0-9_-]{10,}$")
ACL_ID_RE = re.compile(r"^\d{4}\.[A-Za-z0-9.-]+$")


@dataclass
class LegacyTarget:
  aliases: Counter[str] = field(default_factory=Counter)
  footnote_keys: Counter[str] = field(default_factory=Counter)
  kinds: Counter[str] = field(default_factory=Counter)
  files: set[str] = field(default_factory=set)


@dataclass
class BibEntry:
  entry_type: str
  key: str
  fields: dict[str, str]

  @property
  def identity(self) -> str:
    return canonical_identity(self.fields.get("doi"), self.fields.get("url"))


@dataclass
class Metadata:
  entry_type: str
  title: str
  authors: list[str]
  year: str
  journal: str = ""
  booktitle: str = ""
  publisher: str = ""
  volume: str = ""
  number: str = ""
  pages: str = ""
  doi: str = ""
  url: str = ""


OPENREVIEW_FALLBACKS: dict[str, Metadata] = {
  "https://openreview.net/forum?id=6t0Kwf8-jrj": Metadata(
    entry_type="inproceedings",
    title="Editing models with task arithmetic",
    authors=[
      "Ilharco, Gabriel",
      "Ribeiro, Marco Tulio",
      "Wortsman, Mitchell",
      "Schmidt, Ludwig",
      "Hajishirzi, Hannaneh",
      "Farhadi, Ali",
    ],
    year="2023",
    booktitle="ICLR 2023",
    url="https://openreview.net/forum?id=6t0Kwf8-jrj",
  ),
  "https://openreview.net/forum?id=8PbTU4exnV": Metadata(
    entry_type="inproceedings",
    title="Combining Structure and Sequence for Superior Fitness Prediction",
    authors=[
      "Paul, Steffanie",
      "Kollasch, Aaron",
      "Notin, Pascal",
      "Marks, Debora",
    ],
    year="2023",
    booktitle="GenBio@NeurIPS2023",
    url="https://openreview.net/forum?id=8PbTU4exnV",
  ),
  "https://openreview.net/forum?id=aloEru2qCG": Metadata(
    entry_type="article",
    title="LoRA Learns Less and Forgets Less",
    authors=[
      "Biderman, Dan",
      "Portes, Jacob",
      "Gonzalez Ortiz, Jose Javier",
      "Paul, Mansheej",
      "Greengard, Philip",
      "Jennings, Connor",
      "King, Daniel",
      "Havens, Sam",
      "Chiley, Vitaliy",
      "Frankle, Jonathan",
      "Blakeney, Cody",
      "Cunningham, John Patrick",
    ],
    year="2024",
    journal="Transactions on Machine Learning Research",
    url="https://openreview.net/forum?id=aloEru2qCG",
  ),
  "https://openreview.net/forum?id=bxZMKHtlL6": Metadata(
    entry_type="inproceedings",
    title="AntiFold: Improved antibody structure design using inverse folding",
    authors=[
      "Hoie, Magnus",
      "Hummer, Alissa",
      "Olsen, Tobias",
      "Nielsen, Morten",
      "Deane, Charlotte",
    ],
    year="2023",
    booktitle="GenBio@NeurIPS2023",
    url="https://openreview.net/forum?id=bxZMKHtlL6",
  ),
  "https://openreview.net/forum?id=C4BikKsgmK": Metadata(
    entry_type="inproceedings",
    title="Str2Str: A Score-based Framework for Zero-shot Protein Conformation Sampling",
    authors=[
      "Lu, Jiarui",
      "Zhong, Bozitao",
      "Zhang, Zuobai",
      "Tang, Jian",
    ],
    year="2024",
    booktitle="ICLR 2024",
    url="https://openreview.net/forum?id=C4BikKsgmK",
  ),
  "https://openreview.net/forum?id=CTkABQvnkm": Metadata(
    entry_type="article",
    title="Decoupled Sequence and Structure Generation for Realistic Antibody Design",
    authors=[
      "Kim, Nayoung",
      "Kim, Minsu",
      "Ahn, Sungsoo",
      "Park, Jinkyoo",
    ],
    year="2025",
    journal="Transactions on Machine Learning Research",
    url="https://openreview.net/forum?id=CTkABQvnkm",
  ),
  "https://openreview.net/forum?id=i80OPhOCVH2": Metadata(
    entry_type="inproceedings",
    title="On the Bottleneck of Graph Neural Networks and its Practical Implications",
    authors=[
      "Alon, Uri",
      "Yahav, Eran",
    ],
    year="2021",
    booktitle="ICLR 2021",
    url="https://openreview.net/forum?id=i80OPhOCVH2",
  ),
  "https://openreview.net/forum?id=kKF8_K-mBbS": Metadata(
    entry_type="inproceedings",
    title="DiffDock: Diffusion Steps, Twists, and Turns for Molecular Docking",
    authors=[
      "Corso, Gabriele",
      "Stark, Hannes",
      "Jing, Bowen",
      "Barzilay, Regina",
      "Jaakkola, Tommi S.",
    ],
    year="2023",
    booktitle="ICLR 2023",
    url="https://openreview.net/forum?id=kKF8_K-mBbS",
  ),
  "https://openreview.net/forum?id=nZeVKeeFYf9": Metadata(
    entry_type="inproceedings",
    title="LoRA: Low-Rank Adaptation of Large Language Models",
    authors=[
      "Hu, Edward J.",
      "Shen, Yelong",
      "Wallis, Phillip",
      "Allen-Zhu, Zeyuan",
      "Li, Yuanzhi",
      "Wang, Shean",
      "Wang, Lu",
      "Chen, Weizhu",
    ],
    year="2022",
    booktitle="ICLR 2022",
    url="https://openreview.net/forum?id=nZeVKeeFYf9",
  ),
  "https://openreview.net/forum?id=sTYuRVrdK3": Metadata(
    entry_type="inproceedings",
    title="Evaluating Representation Learning on the Protein Structure Universe",
    authors=[
      "Jamasb, Arian Rokkum",
      "Morehead, Alex",
      "Joshi, Chaitanya K.",
      "Zhang, Zuobai",
      "Didi, Kieran",
      "Mathis, Simon V.",
      "Harris, Charles",
      "Tang, Jian",
      "Cheng, Jianlin",
      "Lio, Pietro",
      "Blundell, Tom Leon",
    ],
    year="2024",
    booktitle="ICLR 2024",
    url="https://openreview.net/forum?id=sTYuRVrdK3",
  ),
  "https://openreview.net/forum?id=U87XyMPrZp": Metadata(
    entry_type="inproceedings",
    title="Unlocking hidden biomolecular conformational landscapes in diffusion models at inference time",
    authors=[
      "Richman, Daniel D.",
      "Karaguesian, Jessica",
      "Suomivuori, Carl-Mikael",
      "Dror, Ron O.",
    ],
    year="2025",
    booktitle="NeurIPS 2025",
    url="https://openreview.net/forum?id=U87XyMPrZp",
  ),
  "https://openreview.net/forum?id=yQcebEgQfH": Metadata(
    entry_type="inproceedings",
    title="AlphaFold Meets Flow Matching for Generating Protein Ensembles",
    authors=[
      "Jing, Bowen",
      "Berger, Bonnie",
      "Jaakkola, Tommi",
    ],
    year="2023",
    booktitle="GenBio@NeurIPS2023",
    url="https://openreview.net/forum?id=yQcebEgQfH",
  ),
  "https://openreview.net/forum?id=YTrlu38mM4": Metadata(
    entry_type="inproceedings",
    title="Evaluating Zero-Shot Scoring for In Vitro Antibody Binding Prediction with Experimental Validation",
    authors=[
      "Nori, Divya",
      "Mathis, Simon",
      "Shanehsazzadeh, Amir",
    ],
    year="2023",
    booktitle="GenBio@NeurIPS2023",
    url="https://openreview.net/forum?id=YTrlu38mM4",
  ),
}


class MetaTagParser(HTMLParser):
  def __init__(self) -> None:
    super().__init__()
    self.meta: dict[str, list[str]] = defaultdict(list)
    self._title_parts: list[str] = []
    self._capture_title = False

  def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
    attrs_dict = {k.lower(): v for k, v in attrs if v is not None}
    if tag.lower() == "meta":
      key = attrs_dict.get("name") or attrs_dict.get("property") or attrs_dict.get("itemprop")
      content = attrs_dict.get("content")
      if key and content:
        self.meta[key.lower()].append(html.unescape(content.strip()))
    elif tag.lower() == "title":
      self._capture_title = True

  def handle_endtag(self, tag: str) -> None:
    if tag.lower() == "title":
      self._capture_title = False

  def handle_data(self, data: str) -> None:
    if self._capture_title:
      self._title_parts.append(data)

  @property
  def title(self) -> str:
    return " ".join(part.strip() for part in self._title_parts if part.strip())


def slugify_ascii(value: str) -> str:
  normalized = unicodedata.normalize("NFKD", value)
  ascii_value = normalized.encode("ascii", "ignore").decode("ascii")
  return re.sub(r"[^a-z0-9]+", "", ascii_value.lower())


def canonical_doi(value: str) -> str:
  value = urllib.parse.unquote(value.strip())
  value = RAW_DOI_RE.sub(r"\1", value)
  value = value.replace("__", "/")
  value = re.sub(r"\s+", "", value)
  value = value.rstrip(".,;):")
  value = re.sub(r"(10\.1101/[0-9.]+)v\d+$", r"\1", value, flags=re.IGNORECASE)
  value = value.replace("ARXIV.", "arXiv.")
  return value


def normalize_url(url: str) -> str:
  url = url.strip().rstrip("/")
  if not url:
    return ""
  doi_match = RAW_DOI_RE.search(url)
  if doi_match:
    return f"https://doi.org/{canonical_doi(doi_match.group(1))}"
  if url.startswith("http://"):
    url = "https://" + url[len("http://") :]
  neurips_pdf_match = re.match(
    r"https://proceedings\.neurips\.cc/paper_files/paper/(\d{4})/file/([0-9a-f]+)-Paper\.pdf",
    url,
  )
  if neurips_pdf_match:
    year, paper_hash = neurips_pdf_match.groups()
    return f"https://proceedings.neurips.cc/paper/{year}/hash/{paper_hash}-Abstract.html"
  if url.startswith("https://openreview.net/forum?id="):
    note_id = urllib.parse.parse_qs(urllib.parse.urlparse(url).query).get("id", [""])[0]
    return f"https://openreview.net/forum?id={note_id}"
  if url.startswith("https://aclanthology.org/"):
    return url + "/" if not url.endswith("/") else url
  return url


def canonical_identity(doi: str | None, url: str | None) -> str:
  if doi:
    doi_value = canonical_doi(doi)
    if doi_value:
      return f"doi:{doi_value.lower()}"
  if url:
    url_value = normalize_url(url)
    if url_value:
      return f"url:{url_value}"
  return ""


def identity_to_url(identity: str) -> str:
  kind, value = identity.split(":", 1)
  if kind == "doi":
    return f"https://doi.org/{value}"
  return value


def strip_tags(text: str) -> str:
  text = re.sub(r"(?is)<script.*?>.*?</script>", " ", text)
  text = re.sub(r"(?is)<style.*?>.*?</style>", " ", text)
  text = re.sub(r"(?s)<[^>]+>", "\n", text)
  text = html.unescape(text)
  text = text.replace("\xa0", " ")
  return text


def cleaned_lines(text: str) -> list[str]:
  lines = []
  for raw_line in strip_tags(text).splitlines():
    line = " ".join(raw_line.split()).strip()
    if line:
      lines.append(line)
  return lines


def load_cache() -> dict[str, dict]:
  if CACHE_PATH.exists():
    return json.loads(CACHE_PATH.read_text())
  return {}


def save_cache(cache: dict[str, dict]) -> None:
  CACHE_PATH.write_text(json.dumps(cache, indent=2, sort_keys=True))


def http_get(url: str, accept: str | None = None) -> bytes:
  headers = {"User-Agent": USER_AGENT}
  if accept:
    headers["Accept"] = accept
  req = urllib.request.Request(url, headers=headers)
  with urllib.request.urlopen(req, timeout=25) as response:
    return response.read()


def fetch_csl_metadata(doi: str, cache: dict[str, dict]) -> dict:
  cache_key = f"csl:{doi.lower()}"
  if cache_key in cache:
    return cache[cache_key]

  url = f"https://doi.org/{urllib.parse.quote(doi, safe='/')}"
  try:
    payload = http_get(url, "application/vnd.citationstyles.csl+json")
    record = json.loads(payload)
  except Exception:
    fallback = f"https://api.crossref.org/works/{urllib.parse.quote(doi, safe='/')}"
    try:
      payload = http_get(fallback)
      record = json.loads(payload).get("message", {})
    except Exception as error:
      raise RuntimeError(f"Failed to fetch DOI metadata for {doi}") from error
  cache[cache_key] = record
  save_cache(cache)
  time.sleep(0.15)
  return record


def fetch_html(url: str, cache: dict[str, dict]) -> str:
  cache_key = f"html:{normalize_url(url)}"
  if cache_key in cache:
    return cache[cache_key]["html"]

  text = http_get(url).decode("utf-8", errors="replace")
  cache[cache_key] = {"html": text}
  save_cache(cache)
  time.sleep(0.1)
  return text


def csl_authors(record: dict) -> list[str]:
  authors = []
  for author in record.get("author", []):
    family = author.get("family", "").strip()
    given = author.get("given", "").strip()
    literal = author.get("literal", "").strip()
    if family and given:
      authors.append(f"{family}, {given}")
    elif family:
      authors.append(family)
    elif literal:
      authors.append(literal)
  return authors


def csl_year(record: dict) -> str:
  for field in ("issued", "published-print", "published-online", "published", "created"):
    date_parts = record.get(field, {}).get("date-parts", [])
    if date_parts and date_parts[0]:
      return str(date_parts[0][0])
  return ""


def csl_title(record: dict) -> str:
  title = record.get("title", "")
  if isinstance(title, list):
    title = title[0] if title else ""
  title = re.sub(r"<[^>]+>", "", str(title))
  return title.rstrip(".").strip()


def csl_container(record: dict) -> str:
  container = record.get("container-title", "")
  if isinstance(container, list):
    container = container[0] if container else ""
  return str(container).strip()


def metadata_from_csl(record: dict, fallback_url: str) -> Metadata:
  record_type = record.get("type", "")
  entry_type = "article"
  booktitle = ""
  journal = ""
  if record_type in {"paper-conference", "proceedings-article"}:
    entry_type = "inproceedings"
    booktitle = csl_container(record)
  elif record_type in {"report", "posted-content", "manuscript", "preprint"}:
    entry_type = "misc"
  else:
    journal = csl_container(record)

  if entry_type == "misc" and csl_container(record):
    journal = csl_container(record)

  return Metadata(
    entry_type=entry_type,
    title=csl_title(record),
    authors=csl_authors(record),
    year=csl_year(record),
    journal=journal,
    booktitle=booktitle,
    publisher=str(record.get("publisher", "")).strip(),
    volume=str(record.get("volume", "")).strip(),
    number=str(record.get("issue", "") or record.get("number", "")).strip(),
    pages=str(record.get("page", "")).strip(),
    doi=canonical_doi(record.get("DOI", "") or record.get("doi", "")),
    url=normalize_url(record.get("URL", "") or record.get("url", "") or fallback_url),
  )


def meta_values(parser: MetaTagParser, *names: str) -> list[str]:
  values: list[str] = []
  for name in names:
    values.extend(parser.meta.get(name.lower(), []))
  return [value.strip() for value in values if value.strip()]


def metadata_from_meta_tags(url: str, parser: MetaTagParser) -> Metadata | None:
  title = next(iter(meta_values(parser, "citation_title", "dc.title", "og:title")), "").strip()
  authors = meta_values(parser, "citation_author", "dc.creator")
  doi = next(iter(meta_values(parser, "citation_doi")), "")
  journal = next(iter(meta_values(parser, "citation_journal_title")), "")
  booktitle = next(
    iter(meta_values(parser, "citation_conference_title", "citation_book_title", "citation_inbook_title")),
    "",
  )
  publisher = next(iter(meta_values(parser, "citation_publisher")), "")
  volume = next(iter(meta_values(parser, "citation_volume")), "")
  number = next(iter(meta_values(parser, "citation_issue")), "")
  first_page = next(iter(meta_values(parser, "citation_firstpage")), "")
  last_page = next(iter(meta_values(parser, "citation_lastpage")), "")
  pages = "--".join([part for part in [first_page, last_page] if part])
  publication_date = next(
    iter(meta_values(parser, "citation_publication_date", "citation_date", "dc.date", "article:published_time")),
    "",
  )
  year_match = re.search(r"(19|20)\d{2}", publication_date)
  year = year_match.group(0) if year_match else ""

  if not title and not parser.title:
    return None

  entry_type = "article"
  if booktitle and not journal:
    entry_type = "inproceedings"
  elif not journal:
    entry_type = "misc"

  return Metadata(
    entry_type=entry_type,
    title=(title or parser.title).split(" | ")[0].rstrip(".").strip(),
    authors=authors,
    year=year,
    journal=journal,
    booktitle=booktitle,
    publisher=publisher,
    volume=volume,
    number=number,
    pages=pages,
    doi=canonical_doi(doi),
    url=normalize_url(url),
  )


def parse_openreview_metadata(url: str, html_text: str) -> Metadata | None:
  lines = cleaned_lines(html_text)
  published_index = next((idx for idx, line in enumerate(lines) if line.startswith("Published:")), -1)
  if published_index == -1:
    return None

  ignored = {
    "Toggle navigation",
    "OpenReview .net",
    "Login",
    "Loading",
  }

  def previous_content_line(start: int) -> str:
    for index in range(start, -1, -1):
      line = lines[index]
      if line in ignored:
        continue
      if line.startswith("Go to ") or "Download PDF" in line:
        continue
      return line
    return ""

  authors_line = previous_content_line(published_index - 1)
  title_line = previous_content_line(lines.index(authors_line) - 1) if authors_line else ""
  if not title_line:
    title_line = previous_content_line(published_index - 2)

  authors = [author.strip() for author in authors_line.split(",") if author.strip()]
  published_line = lines[published_index]
  year_match = re.search(r"(19|20)\d{2}", published_line)
  year = year_match.group(0) if year_match else ""
  venue_text = published_line
  venue_text = re.sub(r"^Published:\s*\d{1,2}\s+\w+\s+\d{4},\s+Last Modified:\s*\d{1,2}\s+\w+\s+\d{4}\s*", "", venue_text)
  venue_text = re.sub(r"\s+(Poster|Spotlight|Oral|Everyone|Revisions|BibTeX).*", "", venue_text).strip()
  entry_type = "inproceedings" if venue_text else "misc"
  return Metadata(
    entry_type=entry_type,
    title=title_line.rstrip(".").strip(),
    authors=authors,
    year=year,
    booktitle=venue_text if entry_type == "inproceedings" else "",
    journal="",
    url=normalize_url(url),
  )


def parse_acl_metadata(url: str, html_text: str) -> Metadata | None:
  match = re.search(
    r"@(?P<entry_type>\w+)\{[^,]+,\s*"
    r"title = \"(?P<title>[^\"]+)\",\s*"
    r"author = \{(?P<authors>.*?)\},\s*"
    r"(?:editor = \{.*?\},\s*)?"
    r"booktitle = \"(?P<booktitle>[^\"]+)\",\s*"
    r".*?year = \"(?P<year>\d{4})\".*?"
    r"(?:publisher = \"(?P<publisher>[^\"]+)\",\s*)?"
    r"url = \"(?P<entry_url>[^\"]+)\""
    r"(?:,\s*pages = \"(?P<pages>[^\"]+)\")?",
    html_text,
    re.DOTALL,
  )
  if not match:
    return None

  authors_raw = re.sub(r"\s+", " ", match.group("authors"))
  authors = [
    author.strip()
    for author in re.split(r"\s+and\s+", authors_raw)
    if author.strip()
  ]
  return Metadata(
    entry_type=match.group("entry_type").lower(),
    title=match.group("title").strip(),
    authors=authors,
    year=match.group("year"),
    booktitle=match.group("booktitle").strip(),
    publisher=(match.group("publisher") or "").strip(),
    pages=(match.group("pages") or "").strip(),
    url=normalize_url(match.group("entry_url") or url),
  )


def fetch_url_metadata(url: str, cache: dict[str, dict]) -> Metadata:
  normalized = normalize_url(url)
  if normalized in OPENREVIEW_FALLBACKS:
    return OPENREVIEW_FALLBACKS[normalized]

  html_text = fetch_html(url, cache)
  parser = MetaTagParser()
  parser.feed(html_text)

  meta_record = metadata_from_meta_tags(url, parser)
  if meta_record and meta_record.doi:
    return metadata_from_csl(fetch_csl_metadata(meta_record.doi, cache), meta_record.url or url)
  if meta_record and meta_record.authors and meta_record.year:
    return meta_record

  if "openreview.net/forum?id=" in normalized:
    record = parse_openreview_metadata(normalized, html_text)
    if record:
      return record
  if "aclanthology.org/" in normalized:
    record = parse_acl_metadata(normalized, html_text)
    if record:
      return record

  if meta_record:
    return meta_record
  raise RuntimeError(f"Could not parse citation metadata from {url}")


def metadata_for_identity(identity: str, cache: dict[str, dict]) -> Metadata:
  kind, value = identity.split(":", 1)
  if kind == "doi":
    return metadata_from_csl(fetch_csl_metadata(value, cache), f"https://doi.org/{value}")
  return fetch_url_metadata(value, cache)


def escape_bibtex(value: str) -> str:
  return value.replace("\\", "\\\\").replace("{", "\\{").replace("}", "\\}")


def format_bibtex_value(value: str) -> str:
  return "{" + escape_bibtex(value).strip() + "}"


def render_entry(entry: BibEntry) -> str:
  order = ["title", "author", "year", "journal", "booktitle", "publisher", "volume", "number", "pages", "doi", "url"]
  lines = [f"@{entry.entry_type}{{{entry.key},"]
  for field_name in order:
    value = entry.fields.get(field_name, "").strip()
    if value:
      lines.append(f"  {field_name} = {format_bibtex_value(value)},")
  lines.append("}")
  return "\n".join(lines)


def parse_bib_entries(text: str) -> list[BibEntry]:
  entries: list[BibEntry] = []
  index = 0
  while True:
    start = text.find("@", index)
    if start == -1:
      break
    brace = text.find("{", start)
    comma = text.find(",", brace)
    entry_type = text[start + 1 : brace].strip()
    key = text[brace + 1 : comma].strip()
    depth = 1
    cursor = comma + 1
    while cursor < len(text) and depth > 0:
      char = text[cursor]
      if char == "{":
        depth += 1
      elif char == "}":
        depth -= 1
      cursor += 1
    body = text[comma + 1 : cursor - 1]
    fields = parse_bib_fields(body)
    entries.append(BibEntry(entry_type=entry_type, key=key, fields=fields))
    index = cursor
  return entries


def parse_bib_fields(body: str) -> dict[str, str]:
  fields: dict[str, str] = {}
  index = 0
  length = len(body)
  while index < length:
    while index < length and body[index] in " \t\r\n,":
      index += 1
    if index >= length:
      break

    start = index
    while index < length and re.match(r"[A-Za-z0-9_-]", body[index]):
      index += 1
    field_name = body[start:index].lower()

    while index < length and body[index] in " \t\r\n":
      index += 1
    if index >= length or body[index] != "=":
      break
    index += 1
    while index < length and body[index] in " \t\r\n":
      index += 1

    if index >= length:
      break

    delimiter = body[index]
    if delimiter == "{":
      depth = 1
      index += 1
      start = index
      while index < length and depth > 0:
        char = body[index]
        if char == "{":
          depth += 1
        elif char == "}":
          depth -= 1
        index += 1
      value = body[start : index - 1]
    elif delimiter == "\"":
      index += 1
      start = index
      while index < length and body[index] != "\"":
        if body[index] == "\\":
          index += 2
          continue
        index += 1
      value = body[start:index]
      index += 1
    else:
      start = index
      while index < length and body[index] not in ",\n":
        index += 1
      value = body[start:index]

    fields[field_name] = html.unescape(value).strip()
  return fields


def extract_author_surname(author: str) -> str:
  author = author.strip().strip("{}")
  if "," in author:
    return author.split(",", 1)[0].strip()
  return author.split()[-1].strip()


def year_suffixes(aliases: Counter[str], footnote_keys: Counter[str]) -> list[str]:
  suffixes: list[str] = []
  for alias in aliases:
    match = re.search(r"(19|20)\d{2}([a-z])\b", alias)
    if match:
      suffixes.append(match.group(2))
  for key in footnote_keys:
    match = re.search(r"(19|20)\d{2}([a-z])$", key)
    if match:
      suffixes.append(match.group(2))
  return suffixes


def choose_new_key(
  metadata: Metadata,
  citekey_usage: Counter[str],
  footnote_keys: Counter[str],
  aliases: Counter[str],
  taken: set[str],
) -> str:
  if footnote_keys:
    for suggestion, _count in footnote_keys.most_common():
      if suggestion not in taken:
        return suggestion

  if not metadata.authors or not metadata.year:
    raise RuntimeError(f"Cannot mint citekey for {metadata.url or metadata.doi}: missing authors/year")

  surname = slugify_ascii(extract_author_surname(metadata.authors[0])) or "citation"
  base = f"{surname}{metadata.year}"
  if base not in taken:
    return base

  for suffix in sorted(set(year_suffixes(aliases, footnote_keys))):
    candidate = f"{base}{suffix}"
    if candidate not in taken:
      return candidate

  suffix_ord = ord("b")
  while True:
    candidate = f"{base}{chr(suffix_ord)}"
    if candidate not in taken:
      return candidate
    suffix_ord += 1


def extract_legacy_inventory() -> tuple[dict[str, LegacyTarget], Counter[str]]:
  identities: dict[str, LegacyTarget] = {}
  citekey_usage: Counter[str] = Counter()

  for path in sorted(CONTENT_DIR.rglob("*.md")):
    text = path.read_text()
    for key in PANDOC_CITE_RE.findall(text):
      citekey_usage[key] += 1

    for match in FOOTNOTE_DEF_RE.finditer(text):
      key = match.group("key")
      body = match.group("body").strip()
      doi_match = RAW_DOI_RE.search(body) or BARE_DOI_RE.search(body)
      url_match = re.search(r"https?://[^\s)]+", body)
      identity = ""
      if doi_match:
        identity = canonical_identity(doi_match.group(1), "")
      elif url_match:
        identity = canonical_identity("", url_match.group(0))
      if not identity:
        continue
      target = identities.setdefault(identity, LegacyTarget())
      target.footnote_keys[key] += 1
      target.kinds["footnote"] += 1
      target.files.add(str(path))

    for target_value, alias in WIKILINK_RE.findall(text):
      identity = normalize_target_to_identity(target_value)
      if not identity:
        continue
      target = identities.setdefault(identity, LegacyTarget())
      target.aliases[alias.strip()] += 1
      target.kinds["wikilink"] += 1
      target.files.add(str(path))

    for doi_match in RAW_DOI_RE.findall(text):
      identity = canonical_identity(doi_match, "")
      target = identities.setdefault(identity, LegacyTarget())
      target.kinds["raw-doi-url"] += 1
      target.files.add(str(path))

  return identities, citekey_usage


def normalize_target_to_identity(target: str) -> str:
  value = target.strip()
  if value.startswith("http://") or value.startswith("https://"):
    return canonical_identity("", value)
  if value.startswith("10."):
    return canonical_identity(canonical_doi(value), "")
  if "__" in value and value.startswith("10."):
    return canonical_identity(canonical_doi(value), "")
  if OPENREVIEW_ID_RE.fullmatch(value):
    return canonical_identity("", f"https://openreview.net/forum?id={value}")
  if ACL_ID_RE.fullmatch(value):
    return canonical_identity("", f"https://aclanthology.org/{value}/")
  return ""


def choose_canonical_existing_key(keys: list[str], metadata: Metadata, citekey_usage: Counter[str]) -> str:
  surname = slugify_ascii(extract_author_surname(metadata.authors[0])) if metadata.authors else ""
  year = metadata.year

  def score(key: str) -> tuple[int, int, int]:
    usage = citekey_usage[key]
    exact = int(bool(surname and year and key == f"{surname}{year}"))
    starts = int(bool(surname and key.startswith(surname)))
    return (usage, exact, starts)

  return max(keys, key=score)


def entry_from_metadata(key: str, metadata: Metadata) -> BibEntry:
  fields = {
    "title": metadata.title,
    "author": " and ".join(metadata.authors),
    "year": metadata.year,
    "journal": metadata.journal,
    "booktitle": metadata.booktitle,
    "publisher": metadata.publisher,
    "volume": metadata.volume,
    "number": metadata.number,
    "pages": metadata.pages,
    "doi": metadata.doi,
    "url": metadata.url,
  }
  fields = {name: value for name, value in fields.items() if value}
  return BibEntry(entry_type=metadata.entry_type, key=key, fields=fields)


def main() -> None:
  parser = argparse.ArgumentParser()
  parser.add_argument("--dry-run", action="store_true")
  parser.add_argument("--dump-map", type=Path, help="Write identity-to-citekey map as JSON")
  args = parser.parse_args()

  cache = load_cache()
  legacy_targets, citekey_usage = extract_legacy_inventory()
  existing_entries = parse_bib_entries(BIB_PATH.read_text())

  identity_to_entries: dict[str, list[BibEntry]] = defaultdict(list)
  taken_keys = {entry.key for entry in existing_entries}
  for entry in existing_entries:
    identity = entry.identity
    if identity:
      identity_to_entries[identity].append(entry)

  all_identities = set(identity_to_entries) | set(legacy_targets)
  identity_to_key: dict[str, str] = {}
  key_aliases: dict[str, str] = {}
  next_entries: dict[str, BibEntry] = {}
  failures: list[str] = []

  for identity in sorted(all_identities):
    try:
      metadata = metadata_for_identity(identity, cache)
    except Exception as error:
      failures.append(f"{identity}: {error}")
      continue
    existing_for_identity = identity_to_entries.get(identity, [])
    if existing_for_identity:
      canonical_key = choose_canonical_existing_key(
        [entry.key for entry in existing_for_identity],
        metadata,
        citekey_usage,
      )
      for entry in existing_for_identity:
        if entry.key != canonical_key:
          key_aliases[entry.key] = canonical_key
      identity_to_key[identity] = canonical_key
    else:
      target = legacy_targets.get(identity, LegacyTarget())
      canonical_key = choose_new_key(metadata, citekey_usage, target.footnote_keys, target.aliases, taken_keys)
      identity_to_key[identity] = canonical_key
      taken_keys.add(canonical_key)

    next_entries[identity_to_key[identity]] = entry_from_metadata(identity_to_key[identity], metadata)

  rendered = "\n\n".join(render_entry(entry) for entry in sorted(next_entries.values(), key=lambda item: item.key)) + "\n"

  if args.dump_map:
    payload = {
      "identity_to_key": identity_to_key,
      "key_aliases": key_aliases,
      "legacy_targets": {
        identity: {
          "aliases": dict(target.aliases),
          "footnote_keys": dict(target.footnote_keys),
          "kinds": dict(target.kinds),
          "files": sorted(target.files),
        }
        for identity, target in sorted(legacy_targets.items())
      },
    }
    args.dump_map.write_text(json.dumps(payload, indent=2, sort_keys=True))

  duplicate_identities = [identity for identity, entries in identity_to_entries.items() if len(entries) > 1]
  print(f"legacy identities: {len(legacy_targets)}")
  print(f"existing bibliography entries: {len(existing_entries)}")
  print(f"canonical bibliography entries: {len(next_entries)}")
  print(f"deduplicated identities: {len(duplicate_identities)}")
  print(f"key aliases: {len(key_aliases)}")
  print(f"failures: {len(failures)}")
  if failures:
    for failure in failures:
      print(f"  {failure}")

  if args.dry_run:
    return

  if failures:
    raise RuntimeError("Refusing to rewrite bibliography with unresolved metadata failures")

  BIB_PATH.write_text(rendered)


if __name__ == "__main__":
  main()
