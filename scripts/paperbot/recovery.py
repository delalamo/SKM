"""Recover arXiv gaps from retained daily report artifacts, including legacy reports."""

from __future__ import annotations

import io
import json
import subprocess
import sys
import zipfile
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable, Mapping

from .sources import FetchWindow


def arxiv_recovery_window(
  window: FetchWindow, reports: Iterable[Mapping[str, Any]],
) -> FetchWindow:
  """Widen only automatic windows; only complete coverage retires a failed window."""

  if window.query_since == window.logical_since:
    return window
  pending: list[tuple[datetime, datetime]] = []
  for report in sorted(reports, key=lambda item: datetime.fromisoformat(item["as_of"])):
    until = datetime.fromisoformat(report["as_of"])
    if report.get("dry_run") or until > window.until:
      continue
    # Exact manual backfills neither create nor retire automatic recovery debt.
    if report["query_since"] == report["logical_since"]:
      continue
    since = datetime.fromisoformat(report.get("arxiv_query_since", report["query_since"]))
    if any(error.get("source") == "arxiv" for error in report["feed_errors"]):
      pending.append((since, until))
    elif "arxiv" in report["source_counts"] and not report.get("publish_errors"):
      pending = [(start, end) for start, end in pending if not (since <= start and until >= end)]
  return FetchWindow(
    window.logical_since,
    min([window.query_since, *(start for start, _ in pending)]),
    window.until,
  )


def download_reports(repository: str, branch: str, destination: Path) -> None:
  """Read only this workflow's completed default-branch runs using the runner's gh."""

  def api(path: str) -> bytes:
    return subprocess.run(["gh", "api", path], check=True, capture_output=True).stdout

  destination.mkdir(parents=True, exist_ok=True)
  # Artifact retention bounds the available history. New failed reports carry
  # their widened start forward, keeping an ongoing gap alive across retention.
  page = 1
  while True:
    artifacts = json.loads(api(f"repos/{repository}/actions/artifacts?per_page=100&page={page}"))["artifacts"]
    if not artifacts:
      break
    for artifact in artifacts:
      run_id = artifact["workflow_run"]["id"]
      if artifact["expired"] or artifact["name"] != f"paperbot-report-{run_id}":
        continue
      if artifact["workflow_run"]["head_branch"] != branch:
        continue
      run = json.loads(api(f"repos/{repository}/actions/runs/{run_id}"))
      if run["status"] != "completed" or run["path"] != ".github/workflows/paper-discovery.yml":
        continue
      archive = api(f"repos/{repository}/actions/artifacts/{artifact['id']}/zip")
      with zipfile.ZipFile(io.BytesIO(archive)) as bundle:
        if "paperbot-report.json" in bundle.namelist():
          (destination / f"{run_id}.json").write_bytes(bundle.read("paperbot-report.json"))
    page += 1


if __name__ == "__main__":
  download_reports(sys.argv[1], sys.argv[2], Path(sys.argv[3]))
