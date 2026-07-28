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

`MODEL_UPDATE_TOKEN` is separate and is needed only if the optional trusted-PR
workflow should commit refreshed bibliography/model artifacts back to a branch.
It should be a fine-grained token limited to SKM Contents read/write.
Only configure it when every account and automation allowed to push branches
inside SKM is trusted: GitHub makes repository secrets available to
same-repository pull-request workflows. Fork pull requests remain verify-only
and receive neither this token nor the NCBI key.

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
