# Paper relevance artifacts

This directory is the reproducible data boundary for SKM's daily paper queue.
The committed model consists of SPECTER2 document embeddings plus a small,
deterministic logistic-regression head. SPECTER2's encoder weights are pinned in
`paperbot.toml`, downloaded at runtime, and cached by GitHub Actions rather than
stored in Git.

The float32 matrices contain one 768-dimensional row for every active
bibliography work, every frozen negative, and every unique issue-derived
negative encountered over time. Inactive issue rows are retained for audit and
cheap reactivation. The vector data remains small enough that Git LFS is not
needed.

The classifier output is a ranking-oriented relevance score, not a calibrated
probability. New issues use the strict configurable cutoff `score > 0.80`.

Generated files:

- `positive_embeddings.npy` and `positive_manifest.jsonl`: one active row per
  canonical work in `bibliography.bib`; duplicate citation keys are aliases.
- `pubmed_negatives_v1.jsonl` and `negative_embeddings.npy`: a frozen corpus of
  biological PubMed papers outside the target field and its embeddings. Each
  corpus row records its PubMed query group, MeSH evidence, and
  [Semantic Scholar Academic Graph](https://www.semanticscholar.org/product/api)
  audit so the selection can be reproduced and reviewed. The guard rejects
  unresolved papers, Academic Graph identities matching a positive, direct
  citation links in either direction, and papers sharing at least three cited
  works with the same positive bibliography paper.
  The small near-domain strata also receive a complete manual audit; its four
  explicit PMID exclusions are versioned with the selection policy.
- `pubmed_negatives_v1_metadata.json`: the selection seed, per-topic quotas,
  PubMed query provenance, graph-policy version, aggregate graph coverage, and
  rejection counts for the frozen corpus. Generation stops unless at least 60%
  of canonical positive works resolve with usable reference lists.
- `issue_negatives.jsonl`: a deterministic snapshot of closed,
  paperbot-managed GitHub issues carrying the case-insensitive `negative`
  label. Closing an issue without that label does not make it a negative, and
  open or reopened issues are inactive. Each canonical work contributes at
  most once even when duplicate issues, identifier aliases, revisions, or a
  preprint/publication pair refer to it. The snapshot retains all contributing
  issue numbers as provenance.
- `issue_negative_embeddings.npy` and `issue_negative_manifest.jsonl`:
  append-only SPECTER2 rows for issue-derived negatives and their active state.
  Removing the label or reopening an issue deactivates its row on the next
  synchronization; reclosing and relabeling an unchanged paper reuses the
  existing embedding.
- `abstract_provenance.jsonl`: source, retrieval date, text hash, and reported
  licence for every resolved bibliography abstract.
- `abstract_exceptions.json`: reviewed, reasoned title-only exceptions for works
  whose source publishes no author abstract; lookup failures are not exceptions.
- `classifier.npz` and `model_manifest.json`: non-pickle model parameters and
  hashes needed to prove that the model matches the bibliography.

Run `python -m scripts.paperbot check-model` for an offline freshness check.
Network-backed regeneration requires Python 3.12 and the dependencies in
`requirements-paperbot.lock`.

The stable commands are `backfill-bibliography`, `bootstrap-negatives`,
`sync-issue-negatives`, `refresh-model`, `check-model`, and `daily`.
`bootstrap-negatives` is a network-backed, deliberate corpus-versioning
operation, not part of ordinary bibliography refreshes.
`sync-issue-negatives` uses GitHub's paginated Issues API and requires
`GITHUB_TOKEN` with read-only issue access. The trusted bibliography refresh
workflow runs it after abstract backfill and before model fitting.
`refresh-model` refuses to invent an empty feedback snapshot, so a successful
`sync-issue-negatives` run is required even when no issues currently qualify.
Manual dispatch of that workflow is intentionally verification-only: automatic
regeneration and bot pushes are limited to same-repository pull requests whose
diff includes `bibliography.bib` and no sensitive generator or model changes.

Before fitting, issue-derived works are canonicalized against both the frozen
negative corpus and `bibliography.bib`. A duplicate fixed negative receives no
extra training weight. A negative issue matching any canonical bibliography
work is recorded as omitted and does not enter logistic-regression training;
the bibliography remains authoritative for the positive class.

Run any command as `python -m scripts.paperbot <command> --help` for its narrow
options.
