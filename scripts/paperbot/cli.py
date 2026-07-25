"""Command-line interface for the reproducible paperbot pipeline."""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Sequence

from .backfill import (
  PROVENANCE_FILE,
  backfill_bibliography,
  load_abstract_provenance,
)
from .bootstrap import bootstrap_negatives
from .config import DEFAULT_CONFIG_PATH, REPO_ROOT, load_config
from .daily import (
  project_configuration_enabled,
  run_daily,
  sync_project_queue,
  write_project_queue,
)
from .github import GitHubClient
from .model import (
  BASE_MODEL,
  BASE_REVISION,
  CLASSIFICATION_ADAPTER,
  CLASSIFICATION_ADAPTER_REVISION,
  EMBEDDING_DIMENSION,
  MAX_TOKENS,
  NEGATIVE_SEED,
  StaleModelError,
  check_model,
  refresh_model,
)
from .records import ensure_utc
from .sources import FetchWindow


def build_parser() -> argparse.ArgumentParser:
  parser = argparse.ArgumentParser(prog="paperbot")
  parser.add_argument(
    "--repo-root",
    type=Path,
    help="repository whose bibliography and generated artifacts are data",
  )
  parser.add_argument("--config", type=Path, help="paperbot TOML configuration")
  subparsers = parser.add_subparsers(dest="command", required=True)

  backfill = subparsers.add_parser(
    "backfill-bibliography", help="fetch and store missing bibliography abstracts"
  )
  backfill.add_argument("--dry-run", action="store_true")

  negatives = subparsers.add_parser(
    "bootstrap-negatives",
    help="create the frozen PubMed negatives corpus with citation-graph checks",
  )
  negatives.add_argument(
    "--overwrite",
    action="store_true",
    help=(
      "deliberately replace pubmed-negatives-v1; "
      "never use this for routine model refreshes"
    ),
  )

  subparsers.add_parser(
    "sync-issue-negatives",
    help="snapshot closed paperbot issues labeled negative for model training",
  )

  refresh = subparsers.add_parser(
    "refresh-model", help="refresh changed embeddings and refit logistic regression"
  )
  refresh.add_argument(
    "--allow-negative-change",
    action="store_true",
    help="allow an initial or explicit versioned negative-corpus change",
  )

  subparsers.add_parser("check-model", help="verify committed model freshness")

  daily = subparsers.add_parser("daily", help="fetch, rank, and reconcile the reading queue")
  daily.add_argument("--as-of", help="immutable UTC run boundary (ISO 8601)")
  daily.add_argument("--since", help="exact manual backfill start (ISO 8601)")
  daily.add_argument("--until", help="exact manual backfill end (ISO 8601)")
  daily.add_argument("--dry-run", action="store_true")
  daily.add_argument("--report", type=Path, help="write the complete JSON run report")
  daily.add_argument(
    "--project-queue",
    type=Path,
    help="defer Project mutations and write a credential-free queue for a later step",
  )
  daily.add_argument(
    "--sync-project",
    type=Path,
    metavar="QUEUE",
    help="only apply a previously prepared Project queue",
  )
  return parser


def main(argv: Sequence[str] | None = None) -> int:
  parser = build_parser()
  args = parser.parse_args(argv)
  root = (args.repo_root or REPO_ROOT).resolve()
  config_path = args.config
  if config_path is None:
    config_path = root / DEFAULT_CONFIG_PATH.name
  elif not config_path.is_absolute():
    config_path = root / config_path
  try:
    config = load_config(config_path)
    _validate_pins(config)
    if args.command == "backfill-bibliography":
      result = backfill_bibliography(config, dry_run=args.dry_run)
      _print_json(result.to_dict())
      if result.unresolved:
        print(
          "Unresolved bibliography abstracts: " + ", ".join(result.unresolved),
          file=sys.stderr,
        )
        return 1
      return 0

    if args.command == "bootstrap-negatives":
      records = bootstrap_negatives(config, overwrite=args.overwrite)
      _print_json(
        {
          "dataset": "pubmed-negatives-v1",
          "count": len(records),
          "path": str(config.negative_corpus_path),
          "metadata_path": str(config.negative_metadata_path),
        }
      )
      return 0

    if args.command == "sync-issue-negatives":
      token = os.getenv("GITHUB_TOKEN", "")
      if not token:
        parser.error("GITHUB_TOKEN is required to synchronize issue negatives")
      # Import lazily so offline commands and model checks do not load the
      # network-backed issue collector.
      from .issue_negatives import sync_issue_negatives

      result = sync_issue_negatives(config, github_token=token)
      _print_json(result)
      return 0

    if args.command == "refresh-model":
      provenance = load_abstract_provenance(config.artifact_dir / PROVENANCE_FILE)
      manifest = refresh_model(
        config.bibliography_path,
        config.artifact_dir,
        negatives_path=config.negative_corpus_path,
        title_only_exceptions_path=config.abstract_exceptions_path,
        abstract_provenance=provenance,
        allow_negative_change=args.allow_negative_change,
      )
      _print_json(manifest)
      return 0

    if args.command == "check-model":
      manifest = _check(config)
      _print_json(
        {
          "ok": True,
          "model_hash": manifest["model_hash"],
          "positive_count": manifest["positive_count"],
          "negative_count": manifest["negative_count"],
        }
      )
      return 0

    if args.command == "daily":
      if args.sync_project:
        if args.as_of or args.since or args.until or args.dry_run or args.project_queue:
          parser.error("--sync-project cannot be combined with fetch/window options")
        manifest = _check(config)
        count = sync_project_queue(
          config,
          _resolve_output(root, args.sync_project),
          projects_token=os.getenv("PROJECTS_TOKEN", ""),
          expected_model_hash=str(manifest["model_hash"]),
        )
        _print_json({"ok": True, "project_items_synced": count})
        return 0

      if args.project_queue and args.dry_run:
        parser.error("--project-queue is only meaningful for a publishing run")
      project_enabled = project_configuration_enabled(config)
      window = _window(args, parser, recovery_hours=config.recovery_hours)
      token = os.getenv("GITHUB_TOKEN", "")
      if not token and not args.dry_run:
        parser.error("GITHUB_TOKEN is required for issue publishing")
      client = GitHubClient(config.repository, token)
      result = run_daily(
        config,
        window,
        dry_run=args.dry_run,
        github_token=token,
        projects_token=os.getenv("PROJECTS_TOKEN", ""),
        ncbi_api_key=os.getenv("NCBI_API_KEY", ""),
        github_client=client,
        defer_project=bool(args.project_queue and project_enabled),
      )
      payload = result.to_dict()
      if args.project_queue and project_enabled:
        queue = write_project_queue(
          client,
          _resolve_output(root, args.project_queue),
          repository=config.repository,
          model_hash=result.model_hash,
        )
        payload["project_queue_items"] = len(queue["items"])
      if args.report:
        report_path = _resolve_output(root, args.report)
        _write_json(report_path, payload)
        console_payload = {
          key: value for key, value in payload.items() if key != "candidates"
        }
        console_payload["candidate_count"] = len(payload["candidates"])
        console_payload["report"] = str(report_path)
        _print_json(console_payload)
      else:
        _print_json(payload)
      return 0 if result.ok else 1

  except StaleModelError as error:
    print(str(error), file=sys.stderr)
    return 1
  except (OSError, RuntimeError, ValueError) as error:
    print(f"paperbot: {error}", file=sys.stderr)
    return 1
  parser.error(f"unsupported command: {args.command}")
  return 2


def _check(config: Any) -> dict[str, Any]:
  return check_model(
    config.bibliography_path,
    config.artifact_dir,
    negatives_path=config.negative_corpus_path,
    title_only_exceptions_path=config.abstract_exceptions_path,
  )


def _validate_pins(config: Any) -> None:
  configured = (
    config.model_base,
    config.model_base_revision,
    config.model_adapter,
    config.model_adapter_revision,
    config.embedding_dimension,
    config.max_model_tokens,
    config.negative_seed,
  )
  runtime = (
    BASE_MODEL,
    BASE_REVISION,
    CLASSIFICATION_ADAPTER,
    CLASSIFICATION_ADAPTER_REVISION,
    EMBEDDING_DIMENSION,
    MAX_TOKENS,
    NEGATIVE_SEED,
  )
  if configured != runtime:
    raise ValueError(
      "paperbot.toml model pins do not match the trusted generator runtime"
    )


def _window(
  args: argparse.Namespace,
  parser: argparse.ArgumentParser,
  *,
  recovery_hours: int = 72,
) -> FetchWindow:
  if bool(args.since) != bool(args.until):
    parser.error("--since and --until must be supplied together")
  if args.as_of and args.since:
    parser.error("--as-of cannot be combined with --since/--until")
  if args.since:
    return FetchWindow.between(_timestamp(args.since), _timestamp(args.until))
  boundary = _timestamp(args.as_of) if args.as_of else datetime.now(UTC)
  return FetchWindow.ending_at(boundary, recovery_hours=recovery_hours)


def _timestamp(value: str) -> datetime:
  parsed = ensure_utc(value)
  if parsed is None:
    raise ValueError(f"invalid empty timestamp: {value!r}")
  return parsed


def _resolve_output(root: Path, path: Path) -> Path:
  return path if path.is_absolute() else root / path


def _write_json(path: Path, value: Any) -> None:
  path.parent.mkdir(parents=True, exist_ok=True)
  path.write_text(
    json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
    encoding="utf-8",
  )


def _print_json(value: Any) -> None:
  print(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True))


__all__ = ["build_parser", "main"]
