# arXiv recovery

Daily discovery reads retained `paperbot-report-*` artifacts from completed
`paper-discovery.yml` runs on the default branch. An arXiv feed error (including
partial results) keeps that report's arXiv query start pending. Subsequent daily
runs widen only the arXiv window to include pending dates. A clean arXiv run with
no publishing errors retires a gap only when its query covers the entire failed
window. A successful empty arXiv result also counts as complete coverage.

Reports include `arxiv_query_since`; legacy reports use `query_since`. This lets
existing failures, such as HTTP 429 responses from arXiv on a shared GitHub
Actions egress IP, recover without requiring a new failure after deployment.
Repeated failures carry the widened start into each new report, so a continuing
gap survives the expiration of the original artifact. Other feeds keep their
normal overlap and existing error/exit-status behavior.

Explicit `--since`/`--until` backfills keep their exact bounds and neither create
nor clear daily recovery gaps. Dry-run reports and future-dated reports do not
change recovery. Local callers can supply downloaded JSON reports with
`daily --history-dir PATH`; without it, the existing overlap is unchanged.

Recovery requires retained reports: artifacts currently expire after 14 days.
If discovery stops long enough for every report carrying a gap to expire, or
reports are deleted, use an explicit manual backfill. Artifact retrieval errors
fail the workflow before fetching rather than silently losing known history.
