# Paper reading queue setup

## Decision backends

`paperbot.toml` selects who decides whether a fetched paper becomes an issue:

- `[decision] backend = "jev"` (the default on this branch) asks TypeSafe's
  [Jev](https://docs.typesafe.ai/models) decision model one yes/no (`noul`)
  question per paper through `POST https://api.typesafe.ai/v1/systemone`.
  Jev's probability of "yes" is the issue's **Relevance** score, and a new
  issue is opened only when it is strictly above `[jev] accept_threshold`.
  Each request carries context built from `bibliography.bib`: the candidate,
  the most similar bibliography works with (truncated) abstracts, similar
  papers previously rejected through `negative`-labelled issues
  (`issue_negatives.jsonl`), and as many further bibliography titles as fit the
  `max_context_tokens` budget (about 22k tokens for the current bibliography,
  under Jev's 32k per-question default). Similarity is a dependency-free BM25
  ranking. Papers whose feed omits an abstract are first matched to an abstract
  already shown in their issue or bibliography entry, then looked up through
  the same Europe PMC/PubMed/arXiv/bioRxiv/Crossref resolver used by
  `backfill-bibliography`; papers that still have none are decided from their
  title. This backend uses only the Python standard library, so the workflow
  skips PyTorch and the SPECTER2 download. It requires a `TYPESAFE_API_KEY`
  repository secret.
- `backend = "specter2"` uses the locally trained SPECTER2 classifier described
  below and `[discovery] relevance_threshold`. It needs no API key.

`PAPERBOT_DECISION_BACKEND=jev|specter2` overrides the file for local runs.
Managed issues record a decision hash (`jev:<sha256>` for Jev) covering the
pinned Jev model, prompt version, question text, and context settings. The
bibliography is deliberately excluded, so bibliography edits do not re-decide
open issues. Changing the backend, model, prompt, or context settings
re-decides every open issue on the next run. Closed issues are never reopened.
A credential or billing error (HTTP 401/402/403) stops the run before any
issue is written. Other per-paper failures are reported as `decision-failed`,
mark the run as failed, and are retried on the next run.

## SPECTER2 backend

With `backend = "specter2"`, daily issue creation needs no user-managed API
key. SPECTER2 and the logistic regression run locally on the Actions runner,
and GitHub supplies the temporary `GITHUB_TOKEN` used to create, label, update,
comment on, and reopen issues.

For the issue-only reading queue:

1. Merge the workflow and paperbot files into the default branch. For the
   Jev backend, add the `TYPESAFE_API_KEY` repository secret (Settings →
   Secrets and variables → Actions); the workflow fails fast without it.
2. Optionally add `PAPERBOT_CONTACT_EMAIL=<API contact address>` and the
   `NCBI_API_KEY` secret. The key only raises NCBI's request-rate allowance.
3. Create a repository label named `negative`. To mark a paper as irrelevant,
   apply that label and close its paperbot issue. Closed issues without the
   label, and open or reopened issues, do not become negative training examples.
4. Require the **Test paperbot without credentials** status check in the
   `main` branch-protection rule. The check runs the complete paperbot suite for
   relevant code, configuration, or artifact changes and uses a lightweight
   fail-closed gate for unrelated and bibliography-only PRs. It does not require
   model freshness or generate model-update PRs. Keep **Require branches to
   be up to date before merging** enabled so the tested head cannot lag `main`.
   Keep code-owner review enabled: stored embeddings can be checked for
   consistency and deterministic refitting, but only the paperbot maintainer
   can attest that a direct artifact change came from the pinned SPECTER2
   generator rather than fabricated vectors.

The daily schedule then runs at 00:00 UTC. A manual run defaults to dry-run mode,
and a scheduled or explicitly non-dry manual run creates issues above the
configured relevance cutoff. Discovery uses the last trained model, validating
its specification, runtime dependencies, and classifier hash before publishing.
Bibliography edits do not require retraining before discovery can run. The
current bibliography is still used to recognize known papers and citation keys.

## Recovering failed discovery runs

Check the failed step before rerunning. The `paperbot-report-<run-id>` artifact
includes `paperbot-discovery.log` even when model validation stops discovery before
the JSON fetch report can be created. A failed fetch may still have created or
updated issues from healthy providers; inspect `action_counts`, `source_counts`,
and `blocking_feed_errors` in its JSON report.

Bibliography edits do not make the saved model unusable. If its specification,
runtime dependencies, or classifier hash fail validation, repair or manually
refresh the model on a branch based on current `main`. After a manual refresh,
validate the bibliography and generated artifacts together with:

```sh
python -m scripts.paperbot check-model
python -m pytest tests/paperbot
```

Manual dispatch of **Paperbot tests** runs the unit tests; model refreshes use
the commands below. Keep **Test paperbot without credentials** required in the
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

## Manual model refreshes

Refresh the model deliberately when you want new bibliography entries and
closed negative issues to influence relevance scores. With Python 3.12 and
`requirements-paperbot.lock` installed, run:

```sh
python -m scripts.paperbot backfill-bibliography
GITHUB_TOKEN=... python -m scripts.paperbot sync-issue-negatives
python -m scripts.paperbot refresh-model
python -m scripts.paperbot check-model
```

The token needs read-only issue access. Review and commit the bibliography and
artifacts under `paper_relevance/` after the freshness check succeeds. Paperbot
does not create model-update branches or pull requests automatically, and its
workflows do not require permission to create pull requests.

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
