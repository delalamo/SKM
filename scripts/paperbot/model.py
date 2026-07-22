"""Deterministic SPECTER2 embedding and logistic-regression artifacts.

Heavy ML dependencies are imported only when their functionality is invoked.
Freshness checks and metadata inspection therefore remain cheap and usable in
ordinary repository tooling.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import sys
import tempfile
import warnings
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping, Protocol, Sequence

from .bibliography import (
  CanonicalWork,
  canonicalize_entries,
  embedding_input_hash,
  load_bibliography,
  load_title_only_exceptions,
  normalize_abstract,
  normalize_doi,
  require_abstracts,
  semantic_bibliography_hash,
)
from .citation_graph import (
  DEFAULT_MIN_POSITIVE_COVERAGE,
  SEMANTIC_SCHOLAR_PROVIDER,
  SHARED_REFERENCE_REJECTION_THRESHOLD,
)
from .negative_policy import (
  MANUALLY_EXCLUDED_PMIDS,
  NEGATIVE_DATASET,
  NEGATIVE_END_YEAR,
  NEGATIVE_QUOTAS,
  NEGATIVE_SEED,
  NEGATIVE_START_YEAR,
  TARGET_TEXT_RE,
  is_target_topic,
)


BASE_MODEL = "allenai/specter2_base"
BASE_REVISION = "3447645e1def9117997203454fa4495937bfbd83"
CLASSIFICATION_ADAPTER = "allenai/specter2_classification"
CLASSIFICATION_ADAPTER_REVISION = "d843816b414a856d9a5268d5865f188bb589e6e1"
EMBEDDING_DIMENSION = 768
MAX_TOKENS = 512
ARTIFACT_SCHEMA = 1
EMBEDDING_CONFIG = {
  "base_model": BASE_MODEL,
  "base_revision": BASE_REVISION,
  "adapter": CLASSIFICATION_ADAPTER,
  "adapter_revision": CLASSIFICATION_ADAPTER_REVISION,
  "dimension": EMBEDDING_DIMENSION,
  "max_tokens": MAX_TOKENS,
  "input": "title [SEP] abstract",
  "pooling": "first_token_l2_normalized",
  "dtype": "float32",
}

POSITIVE_MATRIX = "positive_embeddings.npy"
POSITIVE_MANIFEST = "positive_manifest.jsonl"
NEGATIVE_MATRIX = "negative_embeddings.npy"
NEGATIVE_MANIFEST = "negative_manifest.jsonl"
NEGATIVE_CORPUS = "pubmed_negatives_v1.jsonl"
NEGATIVE_METADATA = "pubmed_negatives_v1_metadata.json"
CLASSIFIER_FILE = "classifier.npz"
MODEL_MANIFEST = "model_manifest.json"
NEGATIVE_CORPUS_SOURCE = "PubMed/MEDLINE"
NEGATIVE_METADATA_SOURCE = "PubMed/MEDLINE via NCBI E-utilities"
NEGATIVE_MANIFEST_SOURCE = "pubmed"
SHA256_RE = re.compile(r"[0-9a-f]{64}")
# Retained as a public compatibility alias for tests and audit tooling.  The
# PubMed corpus intentionally blocks only explicit target-field phrases; a
# generic mention of a protein or model is useful hard-negative evidence.
NEGATIVE_EXCLUSION_RE = TARGET_TEXT_RE
CLASSIFIER_CONFIG = {
  "kind": "logistic_regression",
  "penalty": "l2",
  "l1_ratio": 0.0,
  "C": 1.0,
  "solver": "lbfgs",
  "fit_intercept": True,
  "class_weight": "balanced",
  "max_iter": 10000,
  "random_state": 0,
}


class EmbeddingBackend(Protocol):
  def embed(self, documents: Sequence[tuple[str, str]]) -> Any:
    """Return a float32 matrix with one normalized row per document."""


class StaleModelError(RuntimeError):
  def __init__(self, errors: Sequence[str]) -> None:
    self.errors = tuple(errors)
    super().__init__("Model artifacts are stale or invalid:\n- " + "\n- ".join(errors))


@dataclass(frozen=True)
class NegativePaper:
  paper_id: str
  title: str
  abstract: str
  primary_category: str
  published_year: int
  metadata: Mapping[str, Any]

  @property
  def category_family(self) -> str:
    return negative_category_family(self.primary_category)


@dataclass(frozen=True)
class LoadedModel:
  coefficients: Any
  intercept: float
  model_hash: str


def _numpy() -> Any:
  try:
    import numpy  # type: ignore
  except ImportError as error:
    raise RuntimeError("paperbot model operations require numpy") from error
  return numpy


def _sklearn_logistic_regression() -> Any:
  try:
    from sklearn.linear_model import LogisticRegression  # type: ignore
  except ImportError as error:
    raise RuntimeError("paperbot model training requires scikit-learn") from error
  return LogisticRegression


class Specter2Encoder:
  """Pinned SPECTER2 classification-adapter encoder."""

  def __init__(self, *, batch_size: int = 16, device: str | None = None) -> None:
    try:
      import torch  # type: ignore
      from adapters import AutoAdapterModel  # type: ignore
      from huggingface_hub import snapshot_download  # type: ignore
      from transformers import AutoTokenizer  # type: ignore
    except ImportError as error:
      raise RuntimeError(
        "SPECTER2 encoding requires torch, transformers, and adapters"
      ) from error

    self._torch = torch
    self.batch_size = batch_size
    self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
    self.tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL, revision=BASE_REVISION)
    self.model = AutoAdapterModel.from_pretrained(BASE_MODEL, revision=BASE_REVISION)
    adapter_path = snapshot_download(
      repo_id=CLASSIFICATION_ADAPTER,
      revision=CLASSIFICATION_ADAPTER_REVISION,
    )
    adapter_name = self.model.load_adapter(
      adapter_path,
      load_as="specter2_classification",
      with_head=False,
      set_active=False,
    )
    # Adapter libraries have changed activation behavior across releases. Make
    # the intended feature extractor explicit and fail closed if it is absent.
    self.model.set_active_adapters(adapter_name)
    active = self.model.active_adapters
    if active is None or adapter_name not in active.flatten():
      raise RuntimeError("SPECTER2 classification adapter failed to activate")
    self.adapter_name = adapter_name
    self.model.to(self.device)
    self.model.eval()

  def embed(self, documents: Sequence[tuple[str, str]]) -> Any:
    np = _numpy()
    if not documents:
      return np.empty((0, EMBEDDING_DIMENSION), dtype=np.float32)
    outputs = []
    separator = self.tokenizer.sep_token or "[SEP]"
    with self._torch.inference_mode():
      for start in range(0, len(documents), self.batch_size):
        batch = documents[start : start + self.batch_size]
        texts = [f"{title.strip()} {separator} {normalize_abstract(abstract)}" for title, abstract in batch]
        tokens = self.tokenizer(
          texts,
          padding=True,
          truncation=True,
          max_length=MAX_TOKENS,
          return_tensors="pt",
        )
        tokens = {name: tensor.to(self.device) for name, tensor in tokens.items()}
        hidden = self.model(**tokens).last_hidden_state[:, 0, :]
        hidden = hidden / hidden.norm(p=2, dim=1, keepdim=True).clamp_min(1e-12)
        outputs.append(hidden.detach().cpu().to(self._torch.float32).numpy())
    matrix = np.concatenate(outputs, axis=0).astype(np.float32, copy=False)
    _validate_matrix(matrix, len(documents), "SPECTER2 output")
    return matrix


def negative_category_family(primary_category: str) -> str:
  category = primary_category.strip().casefold()
  return next(
    (group for group in NEGATIVE_QUOTAS if group.casefold() == category),
    "",
  )


def negative_selection_key(paper: NegativePaper) -> str:
  value = f"{NEGATIVE_SEED}{paper.category_family}{paper.paper_id.casefold()}"
  return hashlib.sha256(value.encode("utf-8")).hexdigest()


def select_negative_corpus(
  candidates: Iterable[NegativePaper],
  quotas: Mapping[str, int] = NEGATIVE_QUOTAS,
) -> list[NegativePaper]:
  """Select the frozen v1-style negative set deterministically."""

  unique: dict[tuple[str, str], NegativePaper] = {}
  for paper in candidates:
    family = paper.category_family
    clean_abstract = normalize_abstract(paper.abstract)
    mesh_headings = paper.metadata.get("mesh_headings", ())
    if not isinstance(mesh_headings, (list, tuple)):
      mesh_headings = ()
    if family not in quotas or not (
      NEGATIVE_START_YEAR <= paper.published_year <= NEGATIVE_END_YEAR
    ):
      continue
    if not clean_abstract or is_target_topic(
      paper.title,
      clean_abstract,
      tuple(str(value) for value in mesh_headings),
    ):
      continue
    key = (paper.paper_id.casefold(), _normalized_negative_title(paper.title))
    unique.setdefault(key, paper)

  selected: list[NegativePaper] = []
  for family, quota in quotas.items():
    available = sorted(
      (paper for paper in unique.values() if paper.category_family == family),
      key=lambda paper: (negative_selection_key(paper), paper.paper_id),
    )
    if len(available) < quota:
      raise ValueError(f"Only {len(available)} eligible negatives for {family}; need {quota}")
    selected.extend(available[:quota])
  return sorted(selected, key=lambda paper: (paper.category_family, negative_selection_key(paper)))


def _normalized_negative_title(title: str) -> str:
  return re.sub(r"[^a-z0-9]+", " ", title.lower()).strip()


def load_negative_corpus(path: Path | str) -> list[NegativePaper]:
  records: list[NegativePaper] = []
  for line_number, line in enumerate(Path(path).read_text(encoding="utf-8").splitlines(), 1):
    if not line.strip():
      continue
    try:
      payload = json.loads(line)
      pmid = str(payload.get("pmid") or "").strip()
      paper_id = str(payload.get("paper_id") or "").strip()
      if not paper_id and pmid:
        paper_id = f"pmid:{pmid}"
      if not paper_id and payload.get("arxiv_id"):
        paper_id = str(payload["arxiv_id"]).strip()
      title = str(payload["title"]).strip()
      abstract = normalize_abstract(str(payload["abstract"]))
      category = str(payload.get("group") or payload.get("primary_category") or "").strip()
      year = int(
        payload.get("published_year")
        or str(payload.get("publication_date") or payload.get("published") or "")[:4]
      )
    except (KeyError, TypeError, ValueError) as error:
      raise ValueError(f"Invalid negative record at {path}:{line_number}") from error
    if not paper_id or not title or not abstract:
      raise ValueError(f"Incomplete negative record at {path}:{line_number}")
    records.append(NegativePaper(paper_id, title, abstract, category, year, payload))
  return records


def validate_negative_corpus(
  papers: Sequence[NegativePaper],
  *,
  quotas: Mapping[str, int] = NEGATIVE_QUOTAS,
) -> list[str]:
  errors: list[str] = []
  ids: set[str] = set()
  titles: set[str] = set()
  counts = {family: 0 for family in quotas}
  for paper in papers:
    versionless_id = paper.paper_id.casefold()
    title = _normalized_negative_title(paper.title)
    if versionless_id in ids:
      errors.append(f"duplicate negative identifier: {paper.paper_id}")
    if title in titles:
      errors.append(f"duplicate negative title: {paper.title}")
    ids.add(versionless_id)
    titles.add(title)
    if paper.category_family not in quotas:
      errors.append(f"unsupported negative category: {paper.primary_category}")
    else:
      counts[paper.category_family] += 1
    if not (NEGATIVE_START_YEAR <= paper.published_year <= NEGATIVE_END_YEAR):
      errors.append(
        f"negative outside {NEGATIVE_START_YEAR}-{NEGATIVE_END_YEAR}: {paper.paper_id}"
      )
    mesh_headings = paper.metadata.get("mesh_headings", ())
    if not isinstance(mesh_headings, (list, tuple)):
      mesh_headings = ()
    if is_target_topic(
      paper.title,
      paper.abstract,
      tuple(str(value) for value in mesh_headings),
    ):
      errors.append(f"negative contains excluded topic: {paper.paper_id}")
    if str(paper.metadata.get("pmid", "")) in MANUALLY_EXCLUDED_PMIDS:
      errors.append(f"negative was excluded by manual audit: {paper.paper_id}")
    if paper.metadata.get("dataset") != NEGATIVE_DATASET:
      errors.append(f"negative has unexpected dataset: {paper.paper_id}")
    if paper.metadata.get("source") != NEGATIVE_CORPUS_SOURCE:
      errors.append(f"negative has unexpected source: {paper.paper_id}")
    graph = paper.metadata.get("academic_graph")
    if not isinstance(graph, Mapping) or not graph.get("accepted"):
      errors.append(f"negative lacks an accepted academic-graph audit: {paper.paper_id}")
    else:
      pmid = str(paper.metadata.get("pmid", ""))
      if paper.paper_id != f"pmid:{pmid}" or str(graph.get("pmid", "")) != pmid:
        errors.append(f"negative graph audit is bound to another paper: {paper.paper_id}")
      max_shared = graph.get("max_shared_reference_count")
      threshold = graph.get("shared_reference_rejection_threshold")
      reference_count = graph.get("reference_count")
      if (
        not isinstance(max_shared, int)
        or isinstance(max_shared, bool)
        or not isinstance(reference_count, int)
        or isinstance(reference_count, bool)
        or reference_count <= 0
        or graph.get("provider") != SEMANTIC_SCHOLAR_PROVIDER
        or graph.get("resolved") is not True
        or graph.get("rejection_reason") is not None
        or threshold != SHARED_REFERENCE_REJECTION_THRESHOLD
        or graph.get("same_positive_work_count") != 0
        or graph.get("direct_positive_work_count") != 0
        or max_shared >= SHARED_REFERENCE_REJECTION_THRESHOLD
        or not graph.get("references_available")
      ):
        errors.append(f"negative is not graph-distant from positives: {paper.paper_id}")
  for family, expected in quotas.items():
    if counts[family] != expected:
      errors.append(f"negative quota for {family} is {counts[family]}, expected {expected}")
  return errors


def validate_positive_negative_overlap(
  works: Sequence[CanonicalWork],
  papers: Sequence[NegativePaper],
) -> list[str]:
  """Reject negatives that subsequently enter the positive bibliography."""

  positive_ids = {
    identifier.casefold()
    for work in works
    for identifier in work.identifiers
    if identifier
  }
  positive_titles = {
    _normalized_negative_title(work.title)
    for work in works
    if _normalized_negative_title(work.title)
  }
  errors: list[str] = []
  for paper in papers:
    negative_ids = {paper.paper_id.casefold()}
    pmid = str(paper.metadata.get("pmid") or "").strip()
    doi = normalize_doi(str(paper.metadata.get("doi") or ""))
    if pmid:
      negative_ids.add(f"pmid:{pmid}".casefold())
    if doi:
      negative_ids.add(f"doi:{doi}".casefold())
    shared_ids = sorted(positive_ids & negative_ids)
    if shared_ids:
      errors.append(
        f"negative overlaps the positive bibliography by identifier: "
        f"{paper.paper_id} ({', '.join(shared_ids)})"
      )
    title = _normalized_negative_title(paper.title)
    if title and title in positive_titles:
      errors.append(
        f"negative overlaps the positive bibliography by title: {paper.paper_id}"
      )
  return errors


def validate_negative_metadata(
  path: Path | str,
  papers: Sequence[NegativePaper],
) -> list[str]:
  """Validate the committed selection and graph-audit provenance summary."""

  metadata_path = Path(path)
  if not metadata_path.exists():
    return [f"missing negative metadata: {metadata_path.name}"]
  try:
    payload = json.loads(metadata_path.read_text(encoding="utf-8"))
  except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
    return [f"could not read negative metadata: {error}"]
  errors: list[str] = []
  if not isinstance(payload, Mapping):
    return ["negative metadata is not a JSON object"]
  if payload.get("dataset") != NEGATIVE_DATASET:
    errors.append("negative metadata dataset is invalid")
  if payload.get("source") != NEGATIVE_METADATA_SOURCE:
    errors.append("negative metadata source is invalid")
  if payload.get("count") != len(papers):
    errors.append("negative metadata count does not match the corpus")
  if payload.get("groups") != NEGATIVE_QUOTAS:
    errors.append("negative metadata group quotas are invalid")
  if payload.get("manually_excluded_pmids") != sorted(MANUALLY_EXCLUDED_PMIDS):
    errors.append("negative metadata manual audit exclusions are invalid")
  if payload.get("graph_filter_applied") is not True:
    errors.append("negative metadata does not attest that the graph filter ran")
  identity_hash = payload.get("audited_bibliography_identity_hash")
  if not isinstance(identity_hash, str) or SHA256_RE.fullmatch(identity_hash) is None:
    errors.append("negative metadata bibliography audit hash is invalid")
  graph = payload.get("academic_graph")
  if not isinstance(graph, Mapping):
    errors.append("negative metadata academic-graph summary is missing")
    return errors
  if graph.get("provider") != SEMANTIC_SCHOLAR_PROVIDER:
    errors.append("negative metadata academic-graph provider is invalid")
  if graph.get("minimum_positive_reference_coverage") != DEFAULT_MIN_POSITIVE_COVERAGE:
    errors.append("negative metadata graph coverage floor is invalid")
  rule = graph.get("rule")
  threshold_phrase = (
    f"sharing at least {SHARED_REFERENCE_REJECTION_THRESHOLD} cited papers"
  )
  if not isinstance(rule, str) or threshold_phrase not in rule:
    errors.append("negative metadata graph rule threshold is invalid")

  coverage = graph.get("coverage")
  positive = coverage.get("positive") if isinstance(coverage, Mapping) else None
  negative = coverage.get("negative") if isinstance(coverage, Mapping) else None
  if not isinstance(positive, Mapping) or not isinstance(negative, Mapping):
    errors.append("negative metadata graph coverage is missing")
    return errors

  def count(section: Mapping[str, Any], key: str) -> int | None:
    value = section.get(key)
    if not isinstance(value, int) or isinstance(value, bool) or value < 0:
      return None
    return value

  def fraction(section: Mapping[str, Any], key: str) -> float | None:
    value = section.get(key)
    if not isinstance(value, (int, float)) or isinstance(value, bool):
      return None
    number = float(value)
    return number if 0.0 <= number <= 1.0 else None

  positive_total = count(positive, "works_total")
  positive_resolved = count(positive, "works_resolved")
  positive_references = count(positive, "works_with_references")
  positive_paper_ids = count(positive, "paper_ids_resolved")
  positive_paper_references = count(positive, "paper_ids_with_references")
  positive_resolution_fraction = fraction(positive, "resolution_fraction")
  positive_reference_fraction = fraction(positive, "reference_fraction")
  if None in (
    positive_total,
    positive_resolved,
    positive_references,
    positive_paper_ids,
    positive_paper_references,
    positive_resolution_fraction,
    positive_reference_fraction,
  ):
    errors.append("negative metadata positive graph coverage is invalid")
  else:
    assert positive_total is not None
    assert positive_resolved is not None
    assert positive_references is not None
    assert positive_paper_ids is not None
    assert positive_paper_references is not None
    assert positive_resolution_fraction is not None
    assert positive_reference_fraction is not None
    expected_resolution = positive_resolved / positive_total if positive_total else 0.0
    expected_references = positive_references / positive_total if positive_total else 0.0
    if (
      positive_references > positive_resolved
      or positive_resolved > positive_total
      or positive_paper_references > positive_paper_ids
      or abs(positive_resolution_fraction - expected_resolution) > 1e-12
      or abs(positive_reference_fraction - expected_references) > 1e-12
    ):
      errors.append("negative metadata positive graph coverage is inconsistent")
    if positive_reference_fraction < DEFAULT_MIN_POSITIVE_COVERAGE:
      errors.append("negative metadata positive graph coverage is below the floor")

  negative_total = count(negative, "works_total")
  negative_resolved = count(negative, "works_resolved")
  negative_references = count(negative, "works_with_references")
  negative_resolution_fraction = fraction(negative, "resolution_fraction")
  negative_reference_fraction = fraction(negative, "reference_fraction")
  if None in (
    negative_total,
    negative_resolved,
    negative_references,
    negative_resolution_fraction,
    negative_reference_fraction,
  ):
    errors.append("negative metadata candidate graph coverage is invalid")
  else:
    assert negative_total is not None
    assert negative_resolved is not None
    assert negative_references is not None
    assert negative_resolution_fraction is not None
    assert negative_reference_fraction is not None
    expected_resolution = negative_resolved / negative_total if negative_total else 0.0
    expected_references = negative_references / negative_total if negative_total else 0.0
    if (
      negative_references > negative_resolved
      or negative_resolved > negative_total
      or abs(negative_resolution_fraction - expected_resolution) > 1e-12
      or abs(negative_reference_fraction - expected_references) > 1e-12
    ):
      errors.append("negative metadata candidate graph coverage is inconsistent")

  accepted = graph.get("accepted")
  rejected = graph.get("rejected")
  if (
    not isinstance(accepted, int)
    or isinstance(accepted, bool)
    or accepted < 0
    or not isinstance(rejected, int)
    or isinstance(rejected, bool)
    or rejected < 0
  ):
    errors.append("negative metadata graph acceptance counts are invalid")
    accepted = rejected = None
  elif accepted < len(papers):
    errors.append("negative metadata graph audit accepted too few candidates")

  allowed_rejections = {
    "direct_citation",
    "references_unavailable",
    "same_work",
    "shared_reference",
    "unresolved",
  }
  raw_rejections = graph.get("rejection_counts")
  if not isinstance(raw_rejections, Mapping) or any(
    key not in allowed_rejections
    or not isinstance(value, int)
    or isinstance(value, bool)
    or value < 0
    for key, value in raw_rejections.items()
  ):
    errors.append("negative metadata graph rejection counts are invalid")
  elif rejected is not None and sum(raw_rejections.values()) != rejected:
    errors.append("negative metadata graph rejection counts are inconsistent")

  if negative_total is not None and accepted is not None and rejected is not None:
    if accepted + rejected != negative_total:
      errors.append("negative metadata graph candidate counts are inconsistent")
    if negative_references is not None and accepted > negative_references:
      errors.append("negative metadata graph accepted count exceeds usable candidates")
  return errors


def refresh_model(
  bibliography_path: Path | str,
  artifacts_dir: Path | str,
  *,
  negatives_path: Path | str | None = None,
  title_only_exceptions_path: Path | str | None = None,
  encoder: EmbeddingBackend | None = None,
  abstract_provenance: Mapping[str, Mapping[str, str]] | None = None,
  strict_negative_quotas: bool = True,
  allow_negative_change: bool = False,
) -> dict[str, Any]:
  """Refresh embeddings and the classifier, retaining stable positive rows."""

  np = _numpy()
  artifacts = Path(artifacts_dir)
  artifacts.mkdir(parents=True, exist_ok=True)
  negative_path = Path(negatives_path) if negatives_path else artifacts / NEGATIVE_CORPUS
  negative_metadata_path = negative_path.with_name(NEGATIVE_METADATA)
  exceptions = load_title_only_exceptions(title_only_exceptions_path)
  works = canonicalize_entries(load_bibliography(bibliography_path))
  require_abstracts(works, exceptions)
  negatives = load_negative_corpus(negative_path)
  negative_corpus_file_hash = _file_hash(negative_path)
  corpus_errors = validate_positive_negative_overlap(works, negatives)
  if strict_negative_quotas:
    corpus_errors.extend(validate_negative_corpus(negatives))
    corpus_errors.extend(validate_negative_metadata(negative_metadata_path, negatives))
  if corpus_errors:
    raise ValueError("Invalid fixed negative corpus:\n- " + "\n- ".join(corpus_errors))
  negative_metadata_file_hash = (
    _file_hash(negative_metadata_path) if negative_metadata_path.exists() else ""
  )
  if len(works) > len(negatives) * 1.25:
    warnings.warn(
      f"Positive corpus ({len(works)}) exceeds fixed negatives ({len(negatives)}) by more than 25%",
      RuntimeWarning,
      stacklevel=2,
    )

  old_model_manifest: dict[str, Any] = {}
  if (artifacts / MODEL_MANIFEST).exists():
    try:
      old_payload = json.loads(
        (artifacts / MODEL_MANIFEST).read_text(encoding="utf-8")
      )
      if isinstance(old_payload, dict):
        old_model_manifest = old_payload
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
      # An invalid old manifest provides no trustworthy embedding provenance.
      # Rebuild every row below instead of interpreting old bytes as current.
      old_model_manifest = {}
  old_corpus_file_hash = old_model_manifest.get("negative_corpus_file_hash")
  if (
    old_corpus_file_hash
    and old_corpus_file_hash != negative_corpus_file_hash
    and not allow_negative_change
  ):
    raise ValueError(
      "The frozen negative JSONL corpus changed; create an explicit new corpus version"
    )
  old_metadata_file_hash = old_model_manifest.get("negative_metadata_file_hash")
  if (
    old_model_manifest
    and old_metadata_file_hash != negative_metadata_file_hash
    and not allow_negative_change
  ):
    raise ValueError(
      "The frozen negative selection metadata changed; "
      "create an explicit new corpus version"
    )
  reuse_embeddings = _verify_reusable_embedding_artifacts(
    artifacts, old_model_manifest
  )

  encoder = encoder or Specter2Encoder()
  positive_items = [_positive_item(work, exceptions, abstract_provenance or {}) for work in works]
  negative_items = [_negative_item(paper) for paper in negatives]
  positive_matrix, positive_manifest = _refresh_embedding_matrix(
    positive_items,
    artifacts / POSITIVE_MATRIX,
    artifacts / POSITIVE_MANIFEST,
    encoder,
    retain_removed=True,
    reuse_existing=reuse_embeddings,
  )

  old_negative_manifest = _read_jsonl(artifacts / NEGATIVE_MANIFEST)
  if old_negative_manifest and not allow_negative_change:
    old_active = [(row.get("paper_id"), row.get("input_hash")) for row in old_negative_manifest if row.get("active", True)]
    new_active = [(row["paper_id"], row["input_hash"]) for row in negative_items]
    if old_active != new_active:
      raise ValueError("The frozen negative corpus changed; create an explicit new corpus version")
  negative_matrix, negative_manifest = _refresh_embedding_matrix(
    negative_items,
    artifacts / NEGATIVE_MATRIX,
    artifacts / NEGATIVE_MANIFEST,
    encoder,
    retain_removed=False,
    reuse_existing=reuse_embeddings,
  )

  positive_active = _active_matrix(positive_matrix, positive_manifest)
  negative_active = _active_matrix(negative_matrix, negative_manifest)
  coefficients, intercept, training = fit_logistic_regression(positive_active, negative_active)

  semantic_hash = semantic_bibliography_hash(works, exceptions)
  classifier_payload = {
    "coef": coefficients,
    "intercept": np.asarray([intercept], dtype=np.float64),
    "classes": np.asarray([0, 1], dtype=np.int64),
  }
  model_hash = _model_hash(
    coefficients,
    intercept,
    semantic_hash,
    negative_corpus_file_hash,
    negative_metadata_file_hash,
  )
  manifest: dict[str, Any] = {
    "schema": ARTIFACT_SCHEMA,
    "embedding": dict(EMBEDDING_CONFIG),
    "classifier": dict(CLASSIFIER_CONFIG),
    "bibliography_hash": semantic_hash,
    "positive_count": len(positive_items),
    "positive_rows": len(positive_manifest),
    "positive_manifest_hash": _records_hash(positive_manifest),
    "positive_matrix_hash": _array_hash(positive_matrix),
    "negative_corpus": negative_path.name,
    "negative_dataset": NEGATIVE_DATASET,
    "negative_source": NEGATIVE_MANIFEST_SOURCE,
    "negative_graph_provider": SEMANTIC_SCHOLAR_PROVIDER,
    "negative_corpus_hash": _records_hash(negative_items),
    "negative_corpus_file_hash": negative_corpus_file_hash,
    "negative_metadata": negative_metadata_path.name,
    "negative_metadata_file_hash": negative_metadata_file_hash,
    "negative_count": len(negative_items),
    "negative_manifest_hash": _records_hash(negative_manifest),
    "negative_matrix_hash": _array_hash(negative_matrix),
    "model_hash": model_hash,
    "training": training,
    "dependencies": _dependency_versions(),
  }
  _atomic_save_npy(artifacts / POSITIVE_MATRIX, positive_matrix)
  _atomic_write_jsonl(artifacts / POSITIVE_MANIFEST, positive_manifest)
  _atomic_save_npy(artifacts / NEGATIVE_MATRIX, negative_matrix)
  _atomic_write_jsonl(artifacts / NEGATIVE_MANIFEST, negative_manifest)
  _atomic_save_npz(artifacts / CLASSIFIER_FILE, classifier_payload)
  _atomic_write_json(artifacts / MODEL_MANIFEST, manifest)
  return manifest


def _positive_item(
  work: CanonicalWork,
  exceptions: Mapping[str, str],
  provenance: Mapping[str, Mapping[str, str]],
) -> dict[str, Any]:
  exception = exceptions.get(work.work_id) or exceptions.get(work.citekey) or next(
    (exceptions[alias] for alias in work.aliases if alias in exceptions), ""
  )
  if work.abstract:
    exception = ""
  source = provenance.get(work.work_id) or provenance.get(work.citekey) or {}
  return {
    "work_id": work.work_id,
    "citekey": work.citekey,
    "aliases": list(work.aliases),
    "title": work.title,
    "abstract_hash": hashlib.sha256(work.abstract.encode("utf-8")).hexdigest(),
    "input_hash": embedding_input_hash(work.title, work.abstract),
    "title_only": not bool(work.abstract),
    "title_only_reason": exception,
    "abstract_source": source.get("source", ""),
    "abstract_source_url": source.get("source_url", ""),
    "abstract_retrieved_at": source.get("retrieved_at", ""),
    "abstract_license": source.get("license", ""),
    "_abstract": work.abstract,
  }


def _negative_item(paper: NegativePaper) -> dict[str, Any]:
  return {
    "paper_id": paper.paper_id,
    "title": paper.title,
    "abstract_hash": hashlib.sha256(paper.abstract.encode("utf-8")).hexdigest(),
    "input_hash": embedding_input_hash(paper.title, paper.abstract),
    "dataset": str(paper.metadata.get("dataset") or ""),
    "source": str(paper.metadata.get("source") or ""),
    "pmid": str(paper.metadata.get("pmid") or ""),
    "group": paper.category_family,
    "published_year": paper.published_year,
    "academic_graph": paper.metadata.get("academic_graph", {}),
    "_abstract": paper.abstract,
  }


def _item_id(item: Mapping[str, Any]) -> str:
  return str(item.get("work_id") or item.get("paper_id"))


def _public_item(item: Mapping[str, Any]) -> dict[str, Any]:
  return {key: value for key, value in item.items() if not key.startswith("_")}


def _refresh_embedding_matrix(
  items: Sequence[Mapping[str, Any]],
  matrix_path: Path,
  manifest_path: Path,
  encoder: EmbeddingBackend,
  *,
  retain_removed: bool,
  reuse_existing: bool = True,
) -> tuple[Any, list[dict[str, Any]]]:
  np = _numpy()
  old_manifest = _read_jsonl(manifest_path) if reuse_existing else []
  old_matrix = (
    _load_npy(matrix_path) if reuse_existing and matrix_path.exists() else None
  )
  usable_old = (
    old_matrix is not None
    and getattr(old_matrix, "ndim", 0) == 2
    and old_matrix.shape == (len(old_manifest), EMBEDDING_DIMENSION)
    and all(row.get("row") == index for index, row in enumerate(old_manifest))
  )
  if not usable_old:
    old_manifest = []
    old_matrix = np.empty((0, EMBEDDING_DIMENSION), dtype=np.float32)

  manifest = [dict(row) for row in old_manifest] if retain_removed else []
  rows = [old_matrix[index].astype(np.float32, copy=True) for index in range(len(old_manifest))] if retain_removed else []
  old_by_id = {_item_id(row): row for row in old_manifest}
  new_by_id = {_item_id(item): item for item in items}
  if len(new_by_id) != len(items):
    raise ValueError("Embedding manifest contains duplicate identifiers")
  if retain_removed:
    for row in manifest:
      row["active"] = _item_id(row) in new_by_id

  pending: list[Mapping[str, Any]] = []
  pending_rows: list[int] = []
  for item in items:
    identifier = _item_id(item)
    previous = old_by_id.get(identifier)
    public_item = _manifest_item(item, previous)
    if previous is not None:
      if retain_removed:
        row_index = int(previous["row"])
        manifest[row_index] = {**public_item, "row": row_index, "active": True}
      else:
        row_index = len(rows)
        rows.append(old_matrix[int(previous["row"])].astype(np.float32, copy=True))
        manifest.append({**public_item, "row": row_index, "active": True})
      if previous.get("input_hash") != item.get("input_hash"):
        pending.append(item)
        pending_rows.append(row_index)
    else:
      row_index = len(rows)
      rows.append(np.zeros(EMBEDDING_DIMENSION, dtype=np.float32))
      manifest.append({**public_item, "row": row_index, "active": True})
      pending.append(item)
      pending_rows.append(row_index)

  if pending:
    embedded = np.asarray(
      encoder.embed([(str(item["title"]), str(item.get("_abstract", ""))) for item in pending]),
      dtype=np.float32,
    )
    _validate_matrix(embedded, len(pending), "embedding backend output")
    for row_index, vector in zip(pending_rows, embedded):
      rows[row_index] = vector
  matrix = np.asarray(rows, dtype=np.float32).reshape((-1, EMBEDDING_DIMENSION))
  _validate_matrix(matrix, len(manifest), "embedding matrix")
  return matrix, manifest


def _manifest_item(item: Mapping[str, Any], previous: Mapping[str, Any] | None) -> dict[str, Any]:
  public = _public_item(item)
  if "work_id" not in public:
    return public
  for field in (
    "abstract_source",
    "abstract_source_url",
    "abstract_retrieved_at",
    "abstract_license",
  ):
    if not public.get(field) and previous and previous.get("input_hash") == item.get("input_hash"):
      public[field] = previous.get(field, "")
  public["abstract_source"] = public.get("abstract_source") or "bibliography"
  public["abstract_license"] = public.get("abstract_license") or "source rights retained"
  return public


def _active_matrix(matrix: Any, manifest: Sequence[Mapping[str, Any]]) -> Any:
  np = _numpy()
  indexes = [int(row["row"]) for row in manifest if row.get("active", True)]
  return np.asarray(matrix[indexes], dtype=np.float32)


def fit_logistic_regression(positive: Any, negative: Any) -> tuple[Any, float, dict[str, Any]]:
  np = _numpy()
  _validate_matrix(positive, len(positive), "positive matrix")
  _validate_matrix(negative, len(negative), "negative matrix")
  if len(positive) == 0 or len(negative) == 0:
    raise ValueError("Logistic regression needs at least one positive and one negative")
  features = np.concatenate([negative, positive], axis=0).astype(np.float64, copy=False)
  labels = np.concatenate([
    np.zeros(len(negative), dtype=np.int64),
    np.ones(len(positive), dtype=np.int64),
  ])
  LogisticRegression = _sklearn_logistic_regression()
  classifier = LogisticRegression(
    l1_ratio=0.0,
    C=1.0,
    solver="lbfgs",
    fit_intercept=True,
    class_weight="balanced",
    max_iter=10000,
    random_state=0,
  )
  classifier.fit(features, labels)
  coefficients = np.asarray(classifier.coef_[0], dtype=np.float64)
  intercept = float(classifier.intercept_[0])
  predictions = classifier.predict(features)
  training = {
    "converged": bool(int(classifier.n_iter_[0]) < 10000),
    "iterations": int(classifier.n_iter_[0]),
    "training_accuracy": float(np.mean(predictions == labels)),
  }
  return coefficients, intercept, training


def check_model(
  bibliography_path: Path | str,
  artifacts_dir: Path | str,
  *,
  negatives_path: Path | str | None = None,
  title_only_exceptions_path: Path | str | None = None,
  strict_negative_quotas: bool = True,
) -> dict[str, Any]:
  errors = model_errors(
    bibliography_path,
    artifacts_dir,
    negatives_path=negatives_path,
    title_only_exceptions_path=title_only_exceptions_path,
    strict_negative_quotas=strict_negative_quotas,
  )
  if errors:
    raise StaleModelError(errors)
  return json.loads((Path(artifacts_dir) / MODEL_MANIFEST).read_text(encoding="utf-8"))


def model_errors(
  bibliography_path: Path | str,
  artifacts_dir: Path | str,
  *,
  negatives_path: Path | str | None = None,
  title_only_exceptions_path: Path | str | None = None,
  strict_negative_quotas: bool = True,
) -> list[str]:
  artifacts = Path(artifacts_dir)
  paths = [
    artifacts / POSITIVE_MATRIX,
    artifacts / POSITIVE_MANIFEST,
    artifacts / NEGATIVE_MATRIX,
    artifacts / NEGATIVE_MANIFEST,
    artifacts / CLASSIFIER_FILE,
    artifacts / MODEL_MANIFEST,
  ]
  missing = [path.name for path in paths if not path.exists()]
  if missing:
    return [f"missing artifact: {name}" for name in missing]
  try:
    np = _numpy()
    manifest = json.loads((artifacts / MODEL_MANIFEST).read_text(encoding="utf-8"))
    positive_manifest = _read_jsonl(artifacts / POSITIVE_MANIFEST)
    negative_manifest = _read_jsonl(artifacts / NEGATIVE_MANIFEST)
    positive_matrix = _load_npy(artifacts / POSITIVE_MATRIX)
    negative_matrix = _load_npy(artifacts / NEGATIVE_MATRIX)
    with np.load(artifacts / CLASSIFIER_FILE, allow_pickle=False) as model:
      coefficients = np.asarray(model["coef"], dtype=np.float64)
      intercept = float(np.asarray(model["intercept"])[0])
      classes = np.asarray(model["classes"])
  except Exception as error:
    return [f"could not safely load artifacts: {error}"]

  errors: list[str] = []
  embedding = manifest.get("embedding", {})
  if embedding != EMBEDDING_CONFIG:
    errors.append("embedding specification does not exactly match the runtime")
  if manifest.get("schema") != ARTIFACT_SCHEMA:
    errors.append(f"artifact schema is {manifest.get('schema')!r}, expected {ARTIFACT_SCHEMA}")
  if manifest.get("classifier") != CLASSIFIER_CONFIG:
    errors.append("classifier hyperparameters do not match the deterministic configuration")
  recorded_dependencies = manifest.get("dependencies")
  runtime_dependencies = _dependency_versions()
  if not isinstance(recorded_dependencies, dict) or recorded_dependencies != runtime_dependencies:
    errors.append("model dependency versions do not exactly match the runtime")
  expected_negative_fields = {
    "negative_corpus": NEGATIVE_CORPUS,
    "negative_dataset": NEGATIVE_DATASET,
    "negative_source": NEGATIVE_MANIFEST_SOURCE,
    "negative_graph_provider": SEMANTIC_SCHOLAR_PROVIDER,
    "negative_metadata": NEGATIVE_METADATA,
  }
  for field, expected in expected_negative_fields.items():
    if manifest.get(field) != expected:
      errors.append(f"model manifest {field} is invalid")
  try:
    _validate_matrix(positive_matrix, len(positive_manifest), "positive matrix")
    _validate_matrix(negative_matrix, len(negative_manifest), "negative matrix")
  except ValueError as error:
    errors.append(str(error))
  if coefficients.shape != (EMBEDDING_DIMENSION,):
    errors.append(f"classifier coefficients have shape {coefficients.shape}")
  if classes.tolist() != [0, 1]:
    errors.append(f"classifier classes are {classes.tolist()}, expected [0, 1]")
  try:
    refit_coefficients, refit_intercept, refit_training = fit_logistic_regression(
      _active_matrix(positive_matrix, positive_manifest),
      _active_matrix(negative_matrix, negative_manifest),
    )
    if not np.allclose(coefficients, refit_coefficients, rtol=1e-10, atol=1e-12):
      errors.append("stored classifier coefficients do not match a deterministic refit")
    if not np.isclose(intercept, refit_intercept, rtol=1e-10, atol=1e-12):
      errors.append("stored classifier intercept does not match a deterministic refit")
    if manifest.get("training") != refit_training:
      errors.append("recorded training metadata does not match a deterministic refit")
  except Exception as error:
    errors.append(f"could not independently refit classifier: {error}")

  exceptions = load_title_only_exceptions(title_only_exceptions_path)
  works = canonicalize_entries(load_bibliography(bibliography_path))
  try:
    require_abstracts(works, exceptions)
  except ValueError as error:
    errors.append(str(error))
  expected_hash = semantic_bibliography_hash(works, exceptions)
  if manifest.get("bibliography_hash") != expected_hash:
    errors.append("bibliography semantic hash changed")
  if manifest.get("positive_count") != len(works):
    errors.append("positive count does not match the canonical bibliography")
  if manifest.get("positive_rows") != len(positive_manifest):
    errors.append("positive row count does not match the row manifest")
  provenance_path = artifacts / "abstract_provenance.jsonl"
  provenance_by_work: dict[str, dict[str, Any]] = {}
  if provenance_path.exists():
    try:
      provenance_rows = _read_jsonl(provenance_path)
      for row in provenance_rows:
        work_id = str(row.get("work_id", ""))
        if row.get("schema_version") != 1:
          errors.append(f"abstract provenance schema is invalid for {work_id or 'unknown work'}")
        if not work_id:
          errors.append("abstract provenance row is missing work_id")
        elif work_id in provenance_by_work:
          errors.append(f"duplicate abstract provenance work_id: {work_id}")
        else:
          provenance_by_work[work_id] = row
    except Exception as error:
      errors.append(f"could not validate abstract provenance: {error}")
  active_positive = {str(row.get("work_id")): row for row in positive_manifest if row.get("active", True)}
  expected_positive = {
    _item_id(item): item
    for item in [_positive_item(work, exceptions, provenance_by_work) for work in works]
  }
  if set(active_positive) != set(expected_positive):
    errors.append("positive manifest work identifiers do not match the bibliography")
  else:
    core_fields = (
      "citekey",
      "aliases",
      "title",
      "abstract_hash",
      "input_hash",
      "title_only",
      "title_only_reason",
    )
    changed = [
      identifier for identifier, item in expected_positive.items()
      if any(active_positive[identifier].get(field) != item.get(field) for field in core_fields)
    ]
    if changed:
      errors.append(f"positive manifest or embeddings are stale for {len(changed)} works")
  if provenance_by_work:
    expected_provenance_ids = {work.work_id for work in works if work.abstract}
    if set(provenance_by_work) != expected_provenance_ids:
      errors.append("abstract provenance work identifiers do not match non-title-only positives")
    for work_id in sorted(set(provenance_by_work) & set(active_positive) & set(expected_positive)):
      row = provenance_by_work[work_id]
      actual = active_positive[work_id]
      expected = expected_positive[work_id]
      if row.get("citekey") != expected.get("citekey") or row.get("aliases") != expected.get("aliases"):
        errors.append(f"abstract provenance aliases do not match {work_id}")
      if row.get("text_sha256") != expected.get("abstract_hash"):
        errors.append(f"abstract provenance text hash does not match {work_id}")
      provenance_fields = (
        "abstract_source",
        "abstract_source_url",
        "abstract_retrieved_at",
        "abstract_license",
      )
      if any(actual.get(field) != expected.get(field) for field in provenance_fields):
        errors.append(f"positive manifest provenance does not match {work_id}")
  elif any(
    row.get("abstract_source") not in {"", "bibliography"}
    for row in active_positive.values()
  ):
    errors.append("abstract provenance file is missing for externally resolved positives")

  negative_path = Path(negatives_path) if negatives_path else artifacts / str(manifest.get("negative_corpus", NEGATIVE_CORPUS))
  negative_metadata_path = negative_path.with_name(
    str(manifest.get("negative_metadata", NEGATIVE_METADATA))
  )
  try:
    negatives = load_negative_corpus(negative_path)
    errors.extend(validate_positive_negative_overlap(works, negatives))
    if strict_negative_quotas:
      errors.extend(validate_negative_corpus(negatives))
      errors.extend(validate_negative_metadata(negative_metadata_path, negatives))
    negative_items = [_negative_item(paper) for paper in negatives]
    negative_corpus_file_hash = _file_hash(negative_path)
    negative_metadata_file_hash = (
      _file_hash(negative_metadata_path) if negative_metadata_path.exists() else ""
    )
    active_negative = [row for row in negative_manifest if row.get("active", True)]
    expected_negative = [(_item_id(item), item["input_hash"]) for item in negative_items]
    actual_negative = [(_item_id(row), row.get("input_hash")) for row in active_negative]
    if actual_negative != expected_negative:
      errors.append("negative embedding rows do not match the frozen corpus")
    if manifest.get("negative_count") != len(negative_items):
      errors.append("negative count does not match the frozen corpus")
    if manifest.get("negative_corpus_hash") != _records_hash(negative_items):
      errors.append("fixed negative corpus hash changed")
    if manifest.get("negative_corpus_file_hash") != negative_corpus_file_hash:
      errors.append("frozen negative JSONL file hash changed")
    if manifest.get("negative_metadata_file_hash") != negative_metadata_file_hash:
      errors.append("frozen negative selection metadata hash changed")
  except Exception as error:
    errors.append(f"could not validate negative corpus: {error}")
    negative_items = []
    negative_corpus_file_hash = ""
    negative_metadata_file_hash = ""

  checks = {
    "positive_manifest_hash": _records_hash(positive_manifest),
    "positive_matrix_hash": _array_hash(positive_matrix),
    "negative_manifest_hash": _records_hash(negative_manifest),
    "negative_matrix_hash": _array_hash(negative_matrix),
  }
  for name, actual in checks.items():
    if manifest.get(name) != actual:
      errors.append(f"{name} does not match its artifact")
  expected_model_hash = _model_hash(
    coefficients,
    intercept,
    expected_hash,
    negative_corpus_file_hash,
    negative_metadata_file_hash,
  )
  if manifest.get("model_hash") != expected_model_hash:
    errors.append("classifier/model hash does not match")
  return errors


def load_model(artifacts_dir: Path | str) -> LoadedModel:
  np = _numpy()
  artifacts = Path(artifacts_dir)
  manifest = json.loads((artifacts / MODEL_MANIFEST).read_text(encoding="utf-8"))
  with np.load(artifacts / CLASSIFIER_FILE, allow_pickle=False) as model:
    coefficients = np.asarray(model["coef"], dtype=np.float64)
    intercept = float(np.asarray(model["intercept"])[0])
    classes = np.asarray(model["classes"])
  if coefficients.shape != (EMBEDDING_DIMENSION,) or classes.tolist() != [0, 1]:
    raise ValueError("Invalid paperbot classifier artifact")
  return LoadedModel(coefficients, intercept, str(manifest["model_hash"]))


def score_embeddings(embeddings: Any, model: LoadedModel) -> Any:
  np = _numpy()
  matrix = np.asarray(embeddings, dtype=np.float64)
  _validate_matrix(matrix, len(matrix), "scoring matrix")
  logits = matrix @ model.coefficients + model.intercept
  # A branch-stable sigmoid avoids overflow for corrupt or extreme inputs.
  scores = np.empty_like(logits, dtype=np.float64)
  positive = logits >= 0
  scores[positive] = 1.0 / (1.0 + np.exp(-logits[positive]))
  negative = ~positive
  exp_logits = np.exp(logits[negative])
  scores[negative] = exp_logits / (1.0 + exp_logits)
  return scores


def score_documents(
  documents: Sequence[tuple[str, str]],
  model: LoadedModel,
  *,
  encoder: EmbeddingBackend | None = None,
) -> Any:
  encoder = encoder or Specter2Encoder()
  return score_embeddings(encoder.embed(documents), model)


def _validate_matrix(matrix: Any, rows: int, label: str) -> None:
  if getattr(matrix, "shape", None) != (rows, EMBEDDING_DIMENSION):
    raise ValueError(f"{label} has shape {getattr(matrix, 'shape', None)}, expected {(rows, EMBEDDING_DIMENSION)}")
  np = _numpy()
  if not np.isfinite(matrix).all():
    raise ValueError(f"{label} contains non-finite values")


def _dependency_versions() -> dict[str, str]:
  versions: dict[str, str] = {"python": f"{sys.version_info.major}.{sys.version_info.minor}"}
  for distribution in (
    "numpy",
    "scipy",
    "scikit-learn",
    "joblib",
    "threadpoolctl",
    "torch",
    "transformers",
    "tokenizers",
    "adapters",
    "huggingface-hub",
    "safetensors",
  ):
    try:
      from importlib.metadata import version

      resolved = version(distribution)
      # PyTorch's Linux CPU wheel adds a local ``+cpu`` build tag. Its model
      # semantics match the pinned public release recorded on macOS.
      versions[distribution] = resolved.split("+", 1)[0] if distribution == "torch" else resolved
    except Exception:
      continue
  return versions


def _records_hash(records: Sequence[Mapping[str, Any]]) -> str:
  public = [_public_item(record) for record in records]
  payload = json.dumps(public, ensure_ascii=False, separators=(",", ":"), sort_keys=True)
  return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _array_hash(array: Any) -> str:
  np = _numpy()
  contiguous = np.ascontiguousarray(array)
  digest = hashlib.sha256()
  digest.update(str(contiguous.dtype).encode("ascii"))
  digest.update(json.dumps(list(contiguous.shape), separators=(",", ":")).encode("ascii"))
  digest.update(contiguous.tobytes(order="C"))
  return digest.hexdigest()


def _file_hash(path: Path) -> str:
  digest = hashlib.sha256()
  with path.open("rb") as handle:
    for chunk in iter(lambda: handle.read(1024 * 1024), b""):
      digest.update(chunk)
  return digest.hexdigest()


def _verify_reusable_embedding_artifacts(
  artifacts: Path,
  old_model_manifest: Mapping[str, Any],
) -> bool:
  """Return whether old embedding rows have complete, current provenance."""

  pairs = (
    ("positive", artifacts / POSITIVE_MATRIX, artifacts / POSITIVE_MANIFEST),
    ("negative", artifacts / NEGATIVE_MATRIX, artifacts / NEGATIVE_MANIFEST),
  )
  hash_names = tuple(
    f"{label}_{kind}_hash"
    for label, _matrix_path, _rows_path in pairs
    for kind in ("matrix", "manifest")
  )
  if (
    old_model_manifest.get("schema") != ARTIFACT_SCHEMA
    or old_model_manifest.get("embedding") != EMBEDDING_CONFIG
    or any(
      not isinstance(old_model_manifest.get(name), str)
      or SHA256_RE.fullmatch(str(old_model_manifest.get(name))) is None
      for name in hash_names
    )
    or any(
      not matrix_path.exists() or not rows_path.exists()
      for _label, matrix_path, rows_path in pairs
    )
  ):
    # Missing or incompatible provenance makes every old row untrusted. The
    # caller re-embeds the complete active corpora with the current encoder.
    return False

  for label, matrix_path, rows_path in pairs:
    expected_matrix_hash = str(old_model_manifest[f"{label}_matrix_hash"])
    expected_manifest_hash = str(old_model_manifest[f"{label}_manifest_hash"])
    try:
      matrix_hash = _array_hash(_load_npy(matrix_path))
      manifest_hash = _records_hash(_read_jsonl(rows_path))
    except Exception as error:
      raise ValueError(f"Cannot safely reuse {label} embedding artifacts: {error}") from error
    if matrix_hash != expected_matrix_hash or manifest_hash != expected_manifest_hash:
      raise ValueError(
        f"Refusing to reuse corrupt {label} embedding artifacts; restore or rebuild them explicitly"
      )
  return True


def _model_hash(
  coefficients: Any,
  intercept: float,
  bibliography_hash: str,
  negative_hash: str,
  negative_metadata_hash: str,
) -> str:
  np = _numpy()
  digest = hashlib.sha256()
  digest.update(np.asarray(coefficients, dtype=np.float64).tobytes(order="C"))
  digest.update(np.asarray([intercept], dtype=np.float64).tobytes(order="C"))
  digest.update(bibliography_hash.encode("ascii"))
  digest.update(negative_hash.encode("ascii"))
  digest.update(negative_metadata_hash.encode("ascii"))
  digest.update(BASE_REVISION.encode("ascii"))
  digest.update(CLASSIFICATION_ADAPTER_REVISION.encode("ascii"))
  digest.update(json.dumps(CLASSIFIER_CONFIG, separators=(",", ":"), sort_keys=True).encode("ascii"))
  return digest.hexdigest()


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
  if not path.exists():
    return []
  records: list[dict[str, Any]] = []
  for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
    if not line.strip():
      continue
    payload = json.loads(line)
    if not isinstance(payload, dict):
      raise ValueError(f"Expected object at {path}:{line_number}")
    records.append(payload)
  return records


def _load_npy(path: Path) -> Any:
  return _numpy().load(path, allow_pickle=False)


def _atomic_write_json(path: Path, payload: Mapping[str, Any]) -> None:
  text = json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
  _atomic_write_text(path, text)


def _atomic_write_jsonl(path: Path, records: Sequence[Mapping[str, Any]]) -> None:
  text = "".join(json.dumps(_public_item(record), ensure_ascii=False, separators=(",", ":"), sort_keys=True) + "\n" for record in records)
  _atomic_write_text(path, text)


def _atomic_write_text(path: Path, text: str) -> None:
  path.parent.mkdir(parents=True, exist_ok=True)
  with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as handle:
    temporary = Path(handle.name)
    handle.write(text)
    handle.flush()
    os.fsync(handle.fileno())
  os.replace(temporary, path)


def _atomic_save_npy(path: Path, array: Any) -> None:
  np = _numpy()
  path.parent.mkdir(parents=True, exist_ok=True)
  with tempfile.NamedTemporaryFile("wb", dir=path.parent, delete=False) as handle:
    temporary = Path(handle.name)
    np.save(handle, array, allow_pickle=False)
    handle.flush()
    os.fsync(handle.fileno())
  os.replace(temporary, path)


def _atomic_save_npz(path: Path, arrays: Mapping[str, Any]) -> None:
  np = _numpy()
  path.parent.mkdir(parents=True, exist_ok=True)
  with tempfile.NamedTemporaryFile("wb", dir=path.parent, delete=False) as handle:
    temporary = Path(handle.name)
    np.savez(handle, **arrays)
    handle.flush()
    os.fsync(handle.fileno())
  os.replace(temporary, path)
