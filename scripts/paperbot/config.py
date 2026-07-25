from __future__ import annotations

import os
import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONFIG_PATH = REPO_ROOT / "paperbot.toml"


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


def _path(value: str | Path, root: Path) -> Path:
  path = Path(value)
  return path if path.is_absolute() else root / path


def _section(raw: dict[str, Any], name: str) -> dict[str, Any]:
  value = raw.get(name, {})
  if not isinstance(value, dict):
    raise ValueError(f"paperbot config section {name!r} must be a table")
  return value


def load_config(path: Path | str = DEFAULT_CONFIG_PATH) -> PaperbotConfig:
  config_path = Path(path)
  raw: dict[str, Any] = {}
  if config_path.exists():
    with config_path.open("rb") as handle:
      raw = tomllib.load(handle)

  root = config_path.resolve().parent if config_path.exists() else REPO_ROOT
  project = _section(raw, "project")
  model = _section(raw, "model")
  discovery = _section(raw, "discovery")
  paths = _section(raw, "paths")

  owner = os.getenv("PAPER_PROJECT_OWNER", str(project.get("owner", "")))
  number_text = os.getenv("PAPER_PROJECT_NUMBER", str(project.get("number", ""))).strip()
  project_number = int(number_text) if number_text else None

  threshold = float(discovery.get("relevance_threshold", 0.80))
  if not 0.0 <= threshold <= 1.0:
    raise ValueError("relevance_threshold must be between zero and one")

  return PaperbotConfig(
    repository=str(raw.get("repository", "delalamo/SKM")),
    bibliography_path=_path(paths.get("bibliography", "bibliography.bib"), root),
    artifact_dir=_path(paths.get("artifacts", "paper_relevance"), root),
    abstract_exceptions_path=_path(
      paths.get("abstract_exceptions", "paper_relevance/abstract_exceptions.json"), root
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
  )
