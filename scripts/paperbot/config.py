from __future__ import annotations

import os
import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONFIG_PATH = REPO_ROOT / "paperbot.toml"
DECISION_BACKENDS = ("specter2", "jev")
DEFAULT_JEV_ENDPOINT = "https://api.typesafe.ai/v1/systemone"


@dataclass(frozen=True)
class PaperbotConfig:
  repository: str = "delalamo/SKM"
  bibliography_path: Path = REPO_ROOT / "bibliography.bib"
  artifact_dir: Path = REPO_ROOT / "paper_relevance"
  abstract_exceptions_path: Path = REPO_ROOT / "paper_relevance" / "abstract_exceptions.json"
  relevance_threshold: float = 0.80
  recovery_hours: int = 72
  model_base: str = "allenai/specter2_base"
  model_base_revision: str = "3447645e1def9117997203454fa4495937bfbd83"
  model_adapter: str = "allenai/specter2_classification"
  model_adapter_revision: str = "d843816b414a856d9a5268d5865f188bb589e6e1"
  embedding_dimension: int = 768
  max_model_tokens: int = 512
  negative_seed: str = "skm-pubmed-negatives-v1"
  contact_email: str = ""
  project_owner: str = ""
  project_number: int | None = None
  project_field: str = "Relevance"
  # Which component decides whether a fetched paper becomes an issue.
  decision_backend: str = "specter2"
  jev_model: str = "jev-1.14.0"
  jev_endpoint: str = DEFAULT_JEV_ENDPOINT
  jev_accept_threshold: float = 0.5
  jev_similar_papers: int = 12
  jev_rejected_papers: int = 5
  jev_max_context_tokens: int = 24000
  jev_max_abstract_chars: int = 1500
  jev_max_workers: int = 4
  jev_fetch_missing_abstracts: bool = True

  @property
  def decision_threshold(self) -> float:
    """Strict cutoff a new paper's score must exceed to open an issue."""

    if self.decision_backend == "jev":
      return self.jev_accept_threshold
    return self.relevance_threshold

  @property
  def positive_embeddings_path(self) -> Path:
    return self.artifact_dir / "positive_embeddings.npy"

  @property
  def positive_manifest_path(self) -> Path:
    return self.artifact_dir / "positive_manifest.jsonl"

  @property
  def negative_embeddings_path(self) -> Path:
    return self.artifact_dir / "negative_embeddings.npy"

  @property
  def negative_corpus_path(self) -> Path:
    return self.artifact_dir / "pubmed_negatives_v1.jsonl"

  @property
  def negative_metadata_path(self) -> Path:
    return self.artifact_dir / "pubmed_negatives_v1_metadata.json"

  @property
  def negative_manifest_path(self) -> Path:
    return self.artifact_dir / "negative_manifest.jsonl"

  @property
  def issue_negative_corpus_path(self) -> Path:
    return self.artifact_dir / "issue_negatives.jsonl"

  @property
  def issue_negative_embeddings_path(self) -> Path:
    return self.artifact_dir / "issue_negative_embeddings.npy"

  @property
  def issue_negative_manifest_path(self) -> Path:
    return self.artifact_dir / "issue_negative_manifest.jsonl"

  @property
  def classifier_path(self) -> Path:
    return self.artifact_dir / "classifier.npz"

  @property
  def model_manifest_path(self) -> Path:
    return self.artifact_dir / "model_manifest.json"


def _path(
  value: str | Path,
  root: Path,
  *,
  repository_root: Path | None = None,
) -> Path:
  try:
    path = Path(value)
  except TypeError as error:
    raise ValueError("paperbot data paths must be strings") from error
  resolved = (path if path.is_absolute() else root / path).resolve()
  if repository_root is not None and not resolved.is_relative_to(repository_root):
    raise ValueError(
      f"paperbot data path escapes repository root {repository_root}: {value}"
    )
  return resolved


def _section(raw: dict[str, Any], name: str) -> dict[str, Any]:
  value = raw.get(name, {})
  if not isinstance(value, dict):
    raise ValueError(f"paperbot config section {name!r} must be a table")
  return value


def load_config(
  path: Path | str = DEFAULT_CONFIG_PATH,
  *,
  repository_root: Path | str | None = None,
) -> PaperbotConfig:
  requested_config_path = Path(path)
  config_path = requested_config_path.resolve()
  confined_root = Path(repository_root).resolve() if repository_root is not None else None
  if confined_root is not None:
    if not confined_root.is_dir():
      raise ValueError(f"paperbot repository root is not a directory: {confined_root}")
    if not config_path.is_relative_to(confined_root):
      raise ValueError(
        f"paperbot config must be inside repository root {confined_root}: {config_path}"
      )
    if requested_config_path.is_symlink() or not config_path.is_file():
      raise ValueError(
        f"paperbot config must be a regular, non-symlink file: {config_path}"
      )
  raw: dict[str, Any] = {}
  if config_path.exists():
    with config_path.open("rb") as handle:
      raw = tomllib.load(handle)

  root = config_path.parent
  project = _section(raw, "project")
  model = _section(raw, "model")
  discovery = _section(raw, "discovery")
  paths = _section(raw, "paths")
  decision = _section(raw, "decision")
  jev = _section(raw, "jev")

  backend = os.getenv(
    "PAPERBOT_DECISION_BACKEND", str(decision.get("backend", "specter2"))
  ).strip().casefold()
  if backend not in DECISION_BACKENDS:
    raise ValueError(
      f"decision backend must be one of {', '.join(DECISION_BACKENDS)}: {backend!r}"
    )
  jev_threshold = float(jev.get("accept_threshold", 0.5))
  if not 0.0 <= jev_threshold < 1.0:
    raise ValueError("jev accept_threshold must be in [0, 1)")
  jev_endpoint = str(jev.get("endpoint", DEFAULT_JEV_ENDPOINT)).strip()
  if not jev_endpoint.startswith("https://"):
    raise ValueError("jev endpoint must use https")
  jev_counts = {
    name: int(jev.get(name, default))
    for name, default in (
      ("similar_papers", 12),
      ("rejected_papers", 5),
      ("max_context_tokens", 24000),
      ("max_abstract_chars", 1500),
      ("max_workers", 4),
    )
  }
  if any(value < 0 for value in jev_counts.values()) or jev_counts["max_workers"] < 1:
    raise ValueError("jev context sizes must be non-negative and max_workers positive")

  owner = os.getenv("PAPER_PROJECT_OWNER", str(project.get("owner", "")))
  number_text = os.getenv("PAPER_PROJECT_NUMBER", str(project.get("number", ""))).strip()
  project_number = int(number_text) if number_text else None

  threshold = float(discovery.get("relevance_threshold", 0.80))
  if not 0.0 <= threshold <= 1.0:
    raise ValueError("relevance_threshold must be between zero and one")

  return PaperbotConfig(
    repository=str(raw.get("repository", "delalamo/SKM")),
    bibliography_path=_path(
      paths.get("bibliography", "bibliography.bib"),
      root,
      repository_root=confined_root,
    ),
    artifact_dir=_path(
      paths.get("artifacts", "paper_relevance"),
      root,
      repository_root=confined_root,
    ),
    abstract_exceptions_path=_path(
      paths.get("abstract_exceptions", "paper_relevance/abstract_exceptions.json"),
      root,
      repository_root=confined_root,
    ),
    relevance_threshold=threshold,
    recovery_hours=int(discovery.get("recovery_hours", 72)),
    model_base=str(model.get("base", "allenai/specter2_base")),
    model_base_revision=str(
      model.get("base_revision", "3447645e1def9117997203454fa4495937bfbd83")
    ),
    model_adapter=str(model.get("adapter", "allenai/specter2_classification")),
    model_adapter_revision=str(
      model.get("adapter_revision", "d843816b414a856d9a5268d5865f188bb589e6e1")
    ),
    embedding_dimension=int(model.get("embedding_dimension", 768)),
    max_model_tokens=int(model.get("max_tokens", 512)),
    negative_seed=str(model.get("negative_seed", "skm-pubmed-negatives-v1")),
    contact_email=os.getenv("PAPERBOT_CONTACT_EMAIL", str(raw.get("contact_email", ""))),
    project_owner=owner,
    project_number=project_number,
    project_field=os.getenv(
      "PAPER_PROJECT_FIELD", str(project.get("relevance_field", "Relevance"))
    ),
    decision_backend=backend,
    jev_model=str(jev.get("model", "jev-1.14.0")).strip(),
    jev_endpoint=jev_endpoint,
    jev_accept_threshold=jev_threshold,
    jev_similar_papers=jev_counts["similar_papers"],
    jev_rejected_papers=jev_counts["rejected_papers"],
    jev_max_context_tokens=jev_counts["max_context_tokens"],
    jev_max_abstract_chars=jev_counts["max_abstract_chars"],
    jev_max_workers=jev_counts["max_workers"],
    jev_fetch_missing_abstracts=bool(jev.get("fetch_missing_abstracts", True)),
  )
