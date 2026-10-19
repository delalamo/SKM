from datetime import UTC, datetime
import io
import json
from types import SimpleNamespace
import zipfile

import pytest

from scripts.paperbot.recovery import arxiv_recovery_window, download_reports
from scripts.paperbot.sources import FetchWindow, SourceFailure, SourceResult, fetch_all_sources


def window(day):
  return FetchWindow.ending_at(datetime(2026, 10, day, tzinfo=UTC))


def report(day, *, failed=False, start=None, **extra):
  value = window(day)
  return {
    "as_of": value.until.isoformat(),
    "logical_since": value.logical_since.isoformat(),
    "query_since": value.query_since.isoformat(),
    "source_counts": {"arxiv": 0 if failed else 10},
    "feed_errors": [{"source": "arxiv", "status": 429}] if failed else [],
    "dry_run": False,
    "publish_errors": [],
    **({"arxiv_query_since": start.isoformat()} if start else {}),
    **extra,
  }


def test_legacy_failure_widens_only_arxiv_including_retries():
  normal = window(25)
  recovered = arxiv_recovery_window(normal, [report(19, failed=True)])
  assert recovered.query_since == window(19).query_since
  seen = {"arxiv": [], "pubmed": []}

  def fetch(name):
    def run(value, client):
      seen[name].append(value)
      return SourceResult(name, errors=(
        [SourceFailure(name, "fetch", "429", retryable=True)]
        if name == "arxiv" and len(seen[name]) == 1 else []
      ))
    return run

  fetch_all_sources(normal, arxiv_window=recovered,
                    fetchers={name: fetch(name) for name in seen},
                    provider_retry_delays=(0,), sleep=lambda _: None)
  assert seen == {"arxiv": [recovered, recovered], "pubmed": [normal]}


def test_successes_and_other_feed_failures_do_not_widen():
  normal = window(25)
  assert arxiv_recovery_window(normal, [report(19)]) == normal
  assert arxiv_recovery_window(normal, [report(19, feed_errors=[{"source": "pubmed"}])]) == normal


def test_recovery_clears_gap_only_after_full_successful_coverage():
  failure = report(19, failed=True)
  start = window(19).query_since
  # An old implementation's successful 72h run cannot erase an older gap.
  assert arxiv_recovery_window(window(26), [failure, report(25)]).query_since == start
  success = report(25, start=start)
  assert arxiv_recovery_window(window(26), [success, failure]) == window(26)
  # A failed widened report carries the debt even after the first artifact expires.
  assert arxiv_recovery_window(window(27), [report(25, failed=True, start=start)]).query_since == start
  # Partial arXiv results are still incomplete.
  assert arxiv_recovery_window(window(26), [report(19, failed=True, source_counts={"arxiv": 2})]).query_since == start


def test_manual_backfills_are_exact_and_do_not_change_daily_recovery():
  manual = FetchWindow.between(window(20).until, window(25).until)
  assert arxiv_recovery_window(manual, [report(19, failed=True)]) == manual
  manual_report = report(25, logical_since=manual.query_since.isoformat(),
                         query_since=manual.query_since.isoformat())
  assert arxiv_recovery_window(window(26), [manual_report]) == window(26)
  assert arxiv_recovery_window(window(26), [report(19, failed=True), manual_report]).query_since == window(19).query_since


@pytest.mark.parametrize("extra", [{"dry_run": True}, {"as_of": window(28).until.isoformat()}])
def test_dry_run_and_future_reports_do_not_create_debt(extra):
  assert arxiv_recovery_window(window(25), [report(19, failed=True, **extra)]) == window(25)


def test_download_reports_filters_and_paginates(monkeypatch, tmp_path):
  buffer = io.BytesIO()
  with zipfile.ZipFile(buffer, "w") as archive:
    archive.writestr("paperbot-report.json", json.dumps(report(19, failed=True)))
  artifacts = [
    {"id": n, "name": f"paperbot-report-{n}", "expired": n == 2,
     "workflow_run": {"id": n, "head_branch": "feature" if n == 3 else "main"}}
    for n in range(1, 6)
  ]
  calls = []

  def run(args, **kwargs):
    path = args[-1]
    calls.append(path)
    if "artifacts?" in path:
      value = {"artifacts": artifacts if path.endswith("&page=1") else []}
    elif "/runs/" in path:
      value = {"status": "in_progress" if path.endswith("4") else "completed",
               "path": "other.yml" if path.endswith("5") else ".github/workflows/paper-discovery.yml"}
    else:
      assert path.endswith("/artifacts/1/zip")
      return SimpleNamespace(stdout=buffer.getvalue())
    return SimpleNamespace(stdout=json.dumps(value).encode())

  monkeypatch.setattr("scripts.paperbot.recovery.subprocess.run", run)
  download_reports("owner/repo", "main", tmp_path)
  assert [p.name for p in tmp_path.iterdir()] == ["1.json"]
  assert json.loads((tmp_path / "1.json").read_text())["feed_errors"][0]["status"] == 429
  assert calls[-1].endswith("page=2")
