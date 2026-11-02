"""Jev-backed accept/reject decisions for newly discovered papers.

Each candidate paper is sent to TypeSafe's Jev decision model together with
context drawn from ``bibliography.bib``: the most lexically similar works the
curator has already collected (with abstracts), similar papers the curator
previously rejected through ``negative``-labelled issues, and as many further
bibliography titles as fit the context budget.  Jev answers one yes/no
(``noul``) question, and its probability of "yes" becomes the paper's score.

This module uses only the Python standard library so the daily workflow runs
on a stock GitHub-hosted runner without PyTorch or model downloads.
"""

from __future__ import annotations

import hashlib
import json
import math
import re
import time
import urllib.error
import urllib.request
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field, replace
from pathlib import Path
from typing import Any, Callable, Mapping, Sequence

from .bibliography import CanonicalWork, canonicalize_entries, load_bibliography
from .config import PaperbotConfig
from .records import PaperRecord


# Bump whenever the question, criteria, or context layout changes; the decision
# hash then changes and open issues are re-decided on the next run.
PROMPT_VERSION = "skm-jev-v1"
QUESTION_NAME = "add_to_reading_list"
QUESTION_INSTRUCTIONS = (
  "The state describes a personal research knowledge base (its bibliography) "
  "and one newly published candidate paper. Should the candidate paper be "
  "added to this knowledge base's reading queue?"
)
QUESTION_CRITERIA = {
  "true": (
    "The candidate's topic, methods, or findings clearly fall within the "
    "research interests shown by the bibliography (for example, it extends, "
    "benchmarks, applies, or competes with methods the bibliography already "
    "collects), and a curator of this bibliography would likely want to read "
    "and cite it."
  ),
  "false": (
    "The candidate is outside the bibliography's research interests, only "
    "shares generic keywords with it, resembles papers the curator previously "
    "rejected, or is too tangential to be worth reading for this knowledge base."
  ),
}
TASK_DESCRIPTION = (
  "Decide whether the candidate paper belongs in the curator's reading queue. "
  "'similar_bibliography_papers' are papers the curator already collected that "
  "are closest to the candidate; 'previously_rejected_papers' were explicitly "
  "rejected by the curator; 'other_bibliography_titles' show the breadth of "
  "the curator's interests."
)
RETRYABLE_STATUS = {408, 409, 425, 429, 500, 502, 503, 504}
TOKEN_RE = re.compile(r"[a-z0-9]+")
STOPWORDS = frozenset(
  """a about above after again against all also an and any are as at be been
  being between both but by can could did do does doing during each few for
  from further had has have having here how i if in into is it its itself just
  more most no nor not of off on once only or other our out over own same
  should so some such than that the their them then there these they this
  those through to too under until up very via was we were what when where
  which while who whom why will with within without would you your using use
  used based new show shows shown study results result approach method methods
  paper propose proposed present here two one however well""".split()
)


class JevError(RuntimeError):
  """Raised when Jev cannot return a usable decision."""

  def __init__(self, message: str, *, status: int | None = None) -> None:
    super().__init__(message)
    self.status = status


def _tokens(text: str) -> list[str]:
  return [
    token
    for token in TOKEN_RE.findall(text.casefold())
    if len(token) > 1 and token not in STOPWORDS and not token.isdigit()
  ]


def _approx_tokens(value: Any) -> int:
  text = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False)
  return math.ceil(len(text) / 4)


def _truncate(text: str, limit: int) -> str:
  text = " ".join(text.split())
  if limit <= 0 or len(text) <= limit:
    return text
  cut = text[:limit].rsplit(" ", 1)[0]
  return cut + " …"


@dataclass(frozen=True)
class ContextDocument:
  title: str
  abstract: str
  year: str = ""


class BM25Index:
  """A small Okapi BM25 index; deterministic and dependency-free."""

  def __init__(self, documents: Sequence[ContextDocument], *, k1: float = 1.5, b: float = 0.75):
    self.documents = list(documents)
    self.k1 = k1
    self.b = b
    self._term_counts: list[Counter[str]] = []
    self._lengths: list[int] = []
    document_frequency: Counter[str] = Counter()
    for document in self.documents:
      # Titles are short but highly informative, so count them twice.
      tokens = _tokens(document.title) * 2 + _tokens(document.abstract)
      counts = Counter(tokens)
      self._term_counts.append(counts)
      self._lengths.append(len(tokens))
      document_frequency.update(counts.keys())
    count = len(self.documents)
    self._average_length = (sum(self._lengths) / count) if count else 0.0
    self._idf = {
      term: math.log(1.0 + (count - frequency + 0.5) / (frequency + 0.5))
      for term, frequency in document_frequency.items()
    }

  def rank(self, query: str) -> list[tuple[int, float]]:
    """Return ``(document index, score)`` pairs, best first, ties by index."""

    terms = Counter(_tokens(query))
    scores: list[tuple[int, float]] = []
    for index, counts in enumerate(self._term_counts):
      score = 0.0
      length_ratio = (
        self._lengths[index] / self._average_length if self._average_length else 0.0
      )
      for term, query_count in terms.items():
        frequency = counts.get(term)
        if not frequency:
          continue
        numerator = frequency * (self.k1 + 1)
        denominator = frequency + self.k1 * (1 - self.b + self.b * length_ratio)
        score += self._idf.get(term, 0.0) * numerator / denominator * query_count
      scores.append((index, score))
    scores.sort(key=lambda item: (-item[1], item[0]))
    return scores


def _work_document(work: CanonicalWork) -> ContextDocument:
  return ContextDocument(work.title, work.abstract, work.year)


def load_rejected_documents(path: Path) -> list[ContextDocument]:
  """Load active issue-derived negatives written by ``sync-issue-negatives``."""

  if not path.is_file():
    return []
  documents: list[ContextDocument] = []
  for line in path.read_text(encoding="utf-8").splitlines():
    if not line.strip():
      continue
    row = json.loads(line)
    if row.get("active") is False:
      continue
    title = str(row.get("title") or "").strip()
    if title:
      documents.append(ContextDocument(title, str(row.get("abstract") or "")))
  return documents


@dataclass
class BibliographyContext:
  """Builds the per-candidate ``state`` sent to Jev."""

  accepted: list[ContextDocument]
  rejected: list[ContextDocument] = field(default_factory=list)
  similar_papers: int = 12
  rejected_papers: int = 5
  max_context_tokens: int = 24000
  max_abstract_chars: int = 1500

  def __post_init__(self) -> None:
    self._accepted_index = BM25Index(self.accepted)
    self._rejected_index = BM25Index(self.rejected)

  @classmethod
  def from_config(cls, config: PaperbotConfig) -> "BibliographyContext":
    works = canonicalize_entries(load_bibliography(config.bibliography_path))
    accepted = [_work_document(work) for work in works if work.title]
    rejected = load_rejected_documents(config.issue_negative_corpus_path)
    return cls(
      accepted,
      rejected,
      similar_papers=config.jev_similar_papers,
      rejected_papers=config.jev_rejected_papers,
      max_context_tokens=config.jev_max_context_tokens,
      max_abstract_chars=config.jev_max_abstract_chars,
    )

  def _paper(self, document: ContextDocument) -> dict[str, str]:
    value = {"title": document.title}
    if document.year:
      value["year"] = document.year
    if document.abstract:
      value["abstract"] = _truncate(document.abstract, self.max_abstract_chars)
    return value

  def state(self, candidate: Mapping[str, Any]) -> dict[str, Any]:
    query = f"{candidate.get('title', '')} {candidate.get('abstract', '')}"
    state: dict[str, Any] = {
      "task": TASK_DESCRIPTION,
      "candidate_paper": dict(candidate),
      "bibliography_size": len(self.accepted),
      "similar_bibliography_papers": [],
      "previously_rejected_papers": [],
      "other_bibliography_titles": [],
    }
    budget = self.max_context_tokens - _approx_tokens(state)

    ranked = self._accepted_index.rank(query)
    used: set[int] = set()
    for index, score in ranked[: self.similar_papers]:
      if score <= 0:
        break
      paper = self._paper(self.accepted[index])
      cost = _approx_tokens(paper) + 2
      if cost > budget:
        break
      state["similar_bibliography_papers"].append(paper)
      used.add(index)
      budget -= cost

    for index, score in self._rejected_index.rank(query)[: self.rejected_papers]:
      if score <= 0:
        break
      paper = self._paper(self.rejected[index])
      cost = _approx_tokens(paper) + 2
      if cost > budget:
        break
      state["previously_rejected_papers"].append(paper)
      budget -= cost

    # Remaining titles in similarity order convey the breadth of interests.
    for index, _score in ranked:
      if index in used:
        continue
      title = self.accepted[index].title
      cost = _approx_tokens(title) + 2
      if cost > budget:
        break
      state["other_bibliography_titles"].append(title)
      budget -= cost
    return state


def decision_hash(config: PaperbotConfig) -> str:
  """Identify the decision procedure in managed issue metadata.

  The bibliography itself is deliberately excluded (as with the SPECTER2
  model) so ordinary bibliography edits do not trigger re-deciding every
  open issue.
  """

  spec = {
    "backend": "jev",
    "prompt_version": PROMPT_VERSION,
    "model": config.jev_model,
    "instructions": QUESTION_INSTRUCTIONS,
    "criteria": QUESTION_CRITERIA,
    "task": TASK_DESCRIPTION,
    "similar_papers": config.jev_similar_papers,
    "rejected_papers": config.jev_rejected_papers,
    "max_context_tokens": config.jev_max_context_tokens,
    "max_abstract_chars": config.jev_max_abstract_chars,
  }
  payload = json.dumps(spec, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
  return "jev:" + hashlib.sha256(payload.encode("utf-8")).hexdigest()


Transport = Callable[[str, bytes, Mapping[str, str], float], tuple[int, bytes, Mapping[str, str]]]


def _urllib_transport(
  url: str, body: bytes, headers: Mapping[str, str], timeout: float
) -> tuple[int, bytes, Mapping[str, str]]:
  request = urllib.request.Request(url, data=body, headers=dict(headers), method="POST")
  try:
    with urllib.request.urlopen(request, timeout=timeout) as response:
      return response.status, response.read(), dict(response.headers)
  except urllib.error.HTTPError as error:
    return error.code, error.read(), dict(error.headers or {})


class JevClient:
  """Minimal client for ``POST /v1/systemone``."""

  def __init__(
    self,
    api_key: str,
    *,
    model: str,
    endpoint: str,
    transport: Transport | None = None,
    attempts: int = 5,
    timeout: float = 60.0,
    sleep: Callable[[float], None] = time.sleep,
  ) -> None:
    if not api_key:
      raise ValueError("TYPESAFE_API_KEY is required for Jev decisions")
    self.api_key = api_key
    self.model = model
    self.endpoint = endpoint
    self.transport = transport or _urllib_transport
    self.attempts = attempts
    self.timeout = timeout
    self.sleep = sleep

  def ask(self, state: Mapping[str, Any], questions: Mapping[str, Any]) -> dict[str, Any]:
    body = json.dumps(
      {"model": self.model, "state": state, "questions": questions},
      ensure_ascii=False,
    ).encode("utf-8")
    headers = {
      "Authorization": f"Bearer {self.api_key}",
      "Content-Type": "application/json",
      "Accept": "application/json",
      "User-Agent": "SKM-Paperbot/1.0 (+https://github.com/delalamo/SKM)",
    }
    last_error: JevError | None = None
    for attempt in range(self.attempts):
      try:
        status, payload, response_headers = self.transport(
          self.endpoint, body, headers, self.timeout
        )
      except (TimeoutError, urllib.error.URLError, OSError) as error:
        last_error = JevError(f"Jev request failed: {error}")
        status, payload, response_headers = 0, b"", {}
      else:
        if 200 <= status < 300:
          try:
            return json.loads(payload)
          except json.JSONDecodeError as error:
            raise JevError(f"Jev returned invalid JSON: {error}") from error
        detail = payload[:500].decode("utf-8", "replace")
        last_error = JevError(f"Jev returned HTTP {status}: {detail}", status=status)
        if status not in RETRYABLE_STATUS:
          raise last_error
      if attempt == self.attempts - 1:
        break
      retry_after = {k.casefold(): v for k, v in response_headers.items()}.get("retry-after")
      try:
        delay = float(retry_after) if retry_after else 2.0 * (2**attempt)
      except ValueError:
        delay = 2.0 * (2**attempt)
      self.sleep(min(60.0, delay))
    assert last_error is not None
    raise last_error


@dataclass(frozen=True)
class JevDecision:
  probability: float
  served_model: str
  input_tokens: int


class JevDecider:
  """Score documents with Jev; ``None`` marks a paper Jev could not decide."""

  def __init__(
    self,
    config: PaperbotConfig,
    client: JevClient,
    context: BibliographyContext,
  ) -> None:
    self.config = config
    self.client = client
    self.context = context
    self.model_hash = decision_hash(config)
    self.errors: list[str] = []
    self.served_models: set[str] = set()
    self.input_tokens = 0

  @classmethod
  def from_config(
    cls, config: PaperbotConfig, *, api_key: str, transport: Transport | None = None
  ) -> "JevDecider":
    client = JevClient(
      api_key, model=config.jev_model, endpoint=config.jev_endpoint, transport=transport
    )
    return cls(config, client, BibliographyContext.from_config(config))

  @staticmethod
  def questions() -> dict[str, Any]:
    return {
      QUESTION_NAME: {
        "type": "noul",
        "instructions": QUESTION_INSTRUCTIONS,
        "criteria": dict(QUESTION_CRITERIA),
      }
    }

  def decide(self, candidate: Mapping[str, Any]) -> JevDecision:
    response = self.client.ask(self.context.state(candidate), self.questions())
    answer = (response.get("answers") or {}).get(QUESTION_NAME) or {}
    value = answer.get("noul")
    if isinstance(value, bool) or not isinstance(value, (int, float)):
      raise JevError(f"Jev response has no numeric {QUESTION_NAME!r} answer")
    probability = float(value)
    if not 0.0 <= probability <= 1.0 or math.isnan(probability):
      raise JevError(f"Jev returned an out-of-range probability: {probability}")
    usage = response.get("usage") or {}
    return JevDecision(
      probability,
      str(response.get("model") or ""),
      int(usage.get("input_tokens") or 0),
    )

  def score(self, documents: Sequence[Mapping[str, Any]]) -> list[float | None]:
    def one(document: Mapping[str, Any]) -> float | None:
      try:
        decision = self.decide(document)
      except JevError as error:
        if error.status in {401, 402, 403}:
          raise  # a credential/billing problem affects every paper: stop early
        self.errors.append(f"{document.get('title', '?')}: {error}")
        return None
      except (ValueError, TypeError) as error:
        self.errors.append(f"{document.get('title', '?')}: {error}")
        return None
      if decision.served_model:
        self.served_models.add(decision.served_model)
      self.input_tokens += decision.input_tokens
      return decision.probability

    if not documents:
      return []
    workers = max(1, min(self.config.jev_max_workers, len(documents)))
    with ThreadPoolExecutor(max_workers=workers) as pool:
      return list(pool.map(one, documents))

  def report(self) -> dict[str, Any]:
    return {
      "backend": "jev",
      "model": self.config.jev_model,
      "served_models": sorted(self.served_models),
      "prompt_version": PROMPT_VERSION,
      "accept_threshold": self.config.jev_accept_threshold,
      "input_tokens": self.input_tokens,
      "errors": list(self.errors),
    }


def candidate_document(record: PaperRecord) -> dict[str, Any]:
  """The candidate description placed in Jev's state."""

  document: dict[str, Any] = {"title": record.title}
  if record.authors:
    authors = list(record.authors[:12])
    if len(record.authors) > 12:
      authors.append("et al.")
    document["authors"] = authors
  if record.venue:
    document["venue"] = record.venue
  if record.year:
    document["year"] = str(record.year)
  if record.categories:
    document["categories"] = list(record.categories)
  document["abstract"] = record.abstract or "(no abstract available; decide from the title)"
  return document


AbstractLookup = Callable[[Mapping[str, str]], str]


def resolver_lookup(contact_email: str = "") -> AbstractLookup:
  """Return a network abstract lookup backed by the bibliography resolver."""

  from .enrichment import AbstractResolver

  resolver = AbstractResolver(contact_email=contact_email)

  def lookup(fields: Mapping[str, str]) -> str:
    result = resolver.resolve(fields)
    return result.text if result else ""

  return lookup


def fill_missing_abstracts(
  records: Sequence[PaperRecord],
  *,
  known_abstract: Callable[[PaperRecord], str],
  lookup: AbstractLookup | None,
) -> tuple[list[PaperRecord], dict[str, int]]:
  """Give every record an abstract when one can be found.

  Abstracts already shown in a managed issue or present in the bibliography
  are reused first, so the issue metadata stays stable across runs; only then
  are the public metadata providers queried.
  """

  stats = {"missing": 0, "reused": 0, "fetched": 0, "unresolved": 0}
  filled: list[PaperRecord] = []
  for record in records:
    if record.abstract:
      filled.append(record)
      continue
    stats["missing"] += 1
    abstract = known_abstract(record)
    if abstract:
      stats["reused"] += 1
    elif lookup is not None:
      fields = {
        "title": record.title,
        "author": " and ".join(record.authors),
        "doi": record.doi,
        "pmid": record.pmid,
        "url": record.url,
        "eprint": record.arxiv_id,
      }
      try:
        abstract = lookup({key: value for key, value in fields.items() if value})
      except Exception:  # metadata lookup is best-effort
        abstract = ""
      if abstract:
        stats["fetched"] += 1
    if abstract:
      filled.append(replace(record, abstract=abstract))
    else:
      stats["unresolved"] += 1
      filled.append(record)
  return filled, stats


__all__ = [
  "BM25Index",
  "BibliographyContext",
  "JevClient",
  "JevDecider",
  "JevError",
  "PROMPT_VERSION",
  "candidate_document",
  "decision_hash",
  "fill_missing_abstracts",
  "resolver_lookup",
]
