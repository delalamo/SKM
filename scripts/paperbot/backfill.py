"""Abstract backfill orchestration for the bibliography training corpus."""

from __future__ import annotations

import hashlib
import json
import os
import tempfile
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping

from .bibliography import (
  BibliographyEntry,
  canonicalize_entries,
  load_bibliography,
  load_title_only_exceptions,
  missing_abstracts,
  normalize_abstract,
  render_bibtex,
)
from .config import PaperbotConfig
from .enrichment import AbstractResolver, ResolvedAbstract


PROVENANCE_FILE = "abstract_provenance.jsonl"


@dataclass(frozen=True)
class BackfillResult:
  canonical_works: int
  bibliography_entries: int
  abstracts_added: int
  aliases_filled: int
  unresolved: tuple[str, ...]
  changed: bool

  def to_dict(self) -> dict[str, Any]:
    return {
      "canonical_works": self.canonical_works,
      "bibliography_entries": self.bibliography_entries,
      "abstracts_added": self.abstracts_added,
      "aliases_filled": self.aliases_filled,
      "unresolved": list(self.unresolved),
      "changed": self.changed,
    }


def load_abstract_provenance(path: Path | str) -> dict[str, dict[str, str]]:
  result: dict[str, dict[str, str]] = {}
  provenance_path = Path(path)
  if not provenance_path.exists():
    return result
  for line_number, line in enumerate(
    provenance_path.read_text(encoding="utf-8").splitlines(), 1
  ):
    if not line.strip():
      continue
    payload = json.loads(line)
    if not isinstance(payload, dict) or not payload.get("work_id"):
      raise ValueError(f"invalid abstract provenance at {provenance_path}:{line_number}")
    public = {key: str(value) for key, value in payload.items() if key != "aliases"}
    aliases = [str(value) for value in payload.get("aliases", [])]
    result[public["work_id"]] = public
    for alias in aliases:
      result[alias] = public
  return result


def backfill_bibliography(
  config: PaperbotConfig,
  *,
  dry_run: bool = False,
  resolver: AbstractResolver | None = None,
  as_of: datetime | None = None,
) -> BackfillResult:
  """Fetch every missing abstract, propagating it across duplicate aliases.

  Successful lookups are written even if other entries remain unresolved. This
  makes a long backfill safely resumable; unresolved article/preprint entries
  still cause the command to fail after it reports their exact citation keys.
  """

  entries = load_bibliography(config.bibliography_path)
  works = canonicalize_entries(entries)
  resolver = resolver or AbstractResolver(contact_email=config.contact_email)
  exceptions = load_title_only_exceptions(config.abstract_exceptions_path)
  retrieved_at = (as_of or datetime.now(UTC)).astimezone(UTC).isoformat()
  old_text = config.bibliography_path.read_text(encoding="utf-8")
  old_provenance = load_abstract_provenance(config.artifact_dir / PROVENANCE_FILE)

  abstracts: dict[str, str] = {}
  provenance_rows: list[dict[str, Any]] = []
  fetched_count = 0
  aliases_filled = 0
  for work in works:
    resolved: ResolvedAbstract | None
    reported_license = (
      work.fields.get("license", "").strip()
      or work.fields.get("copyright", "").strip()
    )
    if work.abstract:
      resolved = ResolvedAbstract(
        normalize_abstract(work.abstract),
        "bibliography",
        work.fields.get("url", ""),
        reported_license or "source rights retained",
      )
    elif (
      work.work_id in exceptions
      or work.citekey in exceptions
      or any(alias in exceptions for alias in work.aliases)
    ):
      # A reviewed title-only exception is already a terminal resolution. Do
      # not repeatedly contact providers for works known not to have an
      # author-supplied abstract.
      resolved = None
    else:
      resolved = resolver.resolve(work.fields)
      if resolved:
        fetched_count += 1
    if not resolved or not resolved.text:
      continue

    abstract = normalize_abstract(resolved.text)
    for alias in work.aliases:
      abstracts[alias] = abstract
    aliases_filled += sum(
      1
      for entry in entries
      if entry.key in work.aliases and not normalize_abstract(entry.fields.get("abstract", ""))
    )
    previous = old_provenance.get(work.work_id, {})
    source = resolved.source
    source_url = resolved.source_url
    license_value = resolved.license
    observed_at = retrieved_at
    if source == "bibliography" and previous.get("text_sha256") == _sha256(abstract):
      source = previous.get("source", source)
      source_url = previous.get("source_url", source_url)
      license_value = reported_license or previous.get("license", license_value)
      observed_at = previous.get("retrieved_at", observed_at)
    provenance_rows.append(
      {
        "schema_version": 1,
        "work_id": work.work_id,
        "citekey": work.citekey,
        "aliases": list(work.aliases),
        "source": source,
        "source_url": source_url,
        "retrieved_at": observed_at,
        "text_sha256": _sha256(abstract),
        "license": license_value or "unknown",
      }
    )

  updated_entries = [
    BibliographyEntry(
      entry.entry_type,
      entry.key,
      {
        **entry.fields,
        **({"abstract": abstracts[entry.key]} if entry.key in abstracts else {}),
      },
    )
    for entry in entries
  ]
  updated_works = canonicalize_entries(updated_entries)
  unresolved = tuple(work.citekey for work in missing_abstracts(updated_works, exceptions))
  new_text = render_bibtex(updated_entries)
  changed = new_text != old_text

  if not dry_run:
    if changed:
      _atomic_write_text(config.bibliography_path, new_text)
    _atomic_write_jsonl(config.artifact_dir / PROVENANCE_FILE, provenance_rows)

  return BackfillResult(
    canonical_works=len(works),
    bibliography_entries=len(entries),
    abstracts_added=fetched_count,
    aliases_filled=aliases_filled,
    unresolved=unresolved,
    changed=changed,
  )


def _sha256(value: str) -> str:
  return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _atomic_write_text(path: Path, value: str) -> None:
  path.parent.mkdir(parents=True, exist_ok=True)
  with tempfile.NamedTemporaryFile(
    "w", encoding="utf-8", dir=path.parent, delete=False
  ) as handle:
    temporary = Path(handle.name)
    handle.write(value)
    handle.flush()
    os.fsync(handle.fileno())
  os.replace(temporary, path)


def _atomic_write_jsonl(path: Path, values: list[Mapping[str, Any]]) -> None:
  text = "".join(
    json.dumps(value, ensure_ascii=False, sort_keys=True) + "\n"
    for value in sorted(values, key=lambda item: str(item["work_id"]))
  )
  _atomic_write_text(path, text)


__all__ = [
  "BackfillResult",
  "PROVENANCE_FILE",
  "backfill_bibliography",
  "load_abstract_provenance",
]
