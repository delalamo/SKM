# Paper reading queue setup

Daily issue creation needs no user-managed API key. SPECTER2 and the logistic
regression run locally on the Actions runner, and GitHub supplies the temporary
`GITHUB_TOKEN` used to create, label, update, comment on, and reopen issues.
There is no OpenAI client, API call, credit requirement, or secret.

For the issue-only reading queue:

1. Merge the workflow and paperbot files into the default branch.
2. Optionally add `PAPERBOT_CONTACT_EMAIL=<API contact address>` and the
   `NCBI_API_KEY` secret. The key only raises NCBI's request-rate allowance.
3. Create a repository label named `negative`. To mark a paper as irrelevant,
   apply that label and close its paperbot issue. Closed issues without the
   label, and open or reopened issues, do not become negative training examples.
4. Require the **Test paperbot without credentials** status check in the
   `main` branch-protection rule. The check runs the complete paperbot suite for
   relevant PRs, also requires model refresh/verification to succeed, and uses
   a lightweight fail-closed gate for unrelated PRs. Keep **Require branches to
   be up to date before merging** enabled so the tested head cannot lag `main`.
   Keep code-owner review enabled: stored embeddings can be checked for
   consistency and deterministic refitting, but only the paperbot maintainer
   can attest that a direct artifact change came from the pinned SPECTER2
   generator rather than fabricated vectors.

The daily schedule then runs at 00:00 UTC. A manual run defaults to dry-run mode,
and a scheduled or explicitly non-dry manual run creates issues above the
configured relevance cutoff. The workflow refuses to publish when the committed
model is stale.

## Recovering failed discovery runs

Check the failed step before rerunning. The `paperbot-report-<run-id>` artifact
includes `paperbot-model-check.log` even when validation stops discovery before
the JSON fetch report can be created. A failed fetch may still have created or
updated issues from healthy providers; inspect `action_counts`, `source_counts`,
and `blocking_feed_errors` in its JSON report.

If the model is stale, repair the bibliography and all generated artifacts
together on a branch based on current `main`. A generated model-update PR targets
its source PR's branch, so merging it there after the source PR has already
merged does not repair `main`. Reuse its generated commit only after confirming
that it fits the current bibliography with:

```sh
python -m scripts.paperbot check-model
python -m pytest tests/paperbot
```

Manual dispatch of **Refresh paper relevance model** verifies artifacts; it does
not regenerate them. Keep **Test paperbot without credentials** required in the
repository's branch protection settings, as described above. A workflow file
alone cannot make a check required.

After merging a repair, manually dispatch **Daily paper discovery** with
`dry_run: true` and explicit UTC `since`/`until` boundaries for one missed day.
Review the report, then repeat that same interval with `dry_run: false`. Continue
in daily batches through the gap; the normal 72-hour overlap cannot recover a
longer outage. Existing issue identities make these reruns idempotent. For the
September 2026 outage, start at `2026-09-16T00:00:00Z`, the last successful run
boundary, and continue through the recovery boundary.

arXiv discovery uses the documented `lastUpdatedDate` sort, newest first, and
filters update timestamps locally. Using `submittedDate` as the date filter
would omit new revisions of old papers. Pagination stops after crossing the
requested start; a backfill that reaches the API's 30,000-result cap fails
explicitly instead of claiming complete coverage. Older intervals beyond that
cap require a separate metadata-harvesting path. For persistent HTTP 406s, use
the bounded response diagnostic in the report and verify from the Actions
runner; a successful local probe does not prove the runner has recovered.

## Automatic model-update pull requests

No `MODEL_UPDATE_TOKEN` secret is required. For a same-repository pull request
that safely changes `bibliography.bib`, the trusted workflow uses GitHub's
temporary `GITHUB_TOKEN` to create or update a separate model-update branch and
open a pull request from that branch into the source branch. Merge that generated
pull request first; the source pull request then reruns with the refreshed model
artifacts and can pass its required check.

Enable this once under **Repository Settings > Actions > General > Workflow
permissions** by selecting **Allow GitHub Actions to create and approve pull
requests**. The repository's default workflow permission can remain read-only:
the model-refresh job requests only `contents: write`, `pull-requests: write`,
and `issues: read`. Fork pull requests remain verify-only.

## Optional ranked GitHub Project

Issues work without a Project. To additionally mirror them into a user-owned
ranked queue:

1. Create a GitHub Project named **Paper Reading List**, link it to
   `delalamo/SKM`, and add a Number field named **Relevance**.
2. Save an **Unread papers** table view filtered to open issues with the `paper`
   label and sorted by Relevance descending. Save a **Read papers** view filtered
   to closed `paper` issues and sorted by update date.
3. Copy the URL of the saved **Unread papers** view and replace the temporary
   repository Projects link in `content/index.md` with that exact view URL.
4. Add all three repository variables:
   - `PAPER_PROJECT_OWNER=delalamo`
   - `PAPER_PROJECT_NUMBER=<number from the Project URL>`
   - `PAPER_PROJECT_FIELD=Relevance`
5. Add `PROJECTS_TOKEN`, an expiring classic personal access token with `project`
   and `repo` scopes. It is exposed only to the final Project GraphQL step, after
   fetching, scoring, and issue reconciliation have finished without it.

Abstracts copied into this public repository retain their source rights. See
`NOTICE.md` before changing the abstract-storage policy.

## Rebuilding the frozen negative corpus

This is not a routine maintenance task. `pubmed-negatives-v1` is selected
deterministically from completed, English MEDLINE records with abstracts. It
uses off-topic biological MeSH major headings, retains harder neighboring fields
that help reject plausible false positives, and excludes explicit target-field
concepts. Candidate negatives are then checked against the positive bibliography
through the Semantic Scholar Academic Graph before they can enter the corpus.
The graph check fails closed for an unresolved candidate or unavailable reference
list. It also rejects a candidate when it resolves to the same graph paper as a
positive, cites a positive work, is cited by a positive work, or shares at least
three cited papers with the same positive work.
All available DOI, PMID, and
arXiv aliases of each canonical positive are included. Corpus generation aborts
unless at least 60% of canonical positives resolve with nonempty reference lists,
so an upstream outage cannot quietly make the graph filter permissive.

The v1 quotas deliberately mix 535 clear negatives (107 each from ecology,
plant biology, animal behavior, developmental biology, and environmental
microbiology) with 134 harder negatives from genomics/transcriptomics,
biosensors, microfluidics, biomaterials/drug delivery, clinical genetics, and
signaling/proteomics. The generated metadata records the exact query and count
for every stratum. The complete near-domain review for v1 also records four
explicit PMID exclusions; these prevent known target-field leaks without
broadening the automatic keyword filter and discarding useful boundary cases.

To create a new version, first review the topic quotas, PubMed queries, graph
policy, and seed in the trusted generator. Then run:

```sh
SEMANTIC_SCHOLAR_API_KEY=... \
  python -m scripts.paperbot bootstrap-negatives --overwrite
GITHUB_TOKEN=... python -m scripts.paperbot sync-issue-negatives
python -m scripts.paperbot refresh-model --allow-negative-change
python -m scripts.paperbot check-model
```

The Semantic Scholar key is optional, but authenticated requests are preferable
for a full rebuild; supply it as a local environment variable as shown rather
than as an Actions secret. Review the generated corpus and aggregate metadata
before committing them. Daily discovery and ordinary bibliography/model
refreshes do not require the key. Never use `--overwrite` merely because the
bibliography changed.

The graph client does not create a cache unless one is explicitly requested.
For a resumable rebuild, set `PAPERBOT_SEMANTIC_SCHOLAR_CACHE` to a temporary or
other untracked JSON path. The cache is operational data and must not be added
to the committed model artifacts.
