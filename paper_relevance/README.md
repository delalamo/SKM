# Paper relevance artifacts

This directory is the reproducible data boundary for SKM's daily paper queue.
The committed model consists of SPECTER2 document embeddings plus a small,
deterministic logistic-regression head. SPECTER2's encoder weights are pinned in
`paperbot.toml`, downloaded at runtime, and cached by GitHub Actions rather than
stored in Git.

The two float32 matrices contain one 768-dimensional row for every active
bibliography work and every frozen negative. With roughly balanced classes,
the vector data remains about 4 MiB and the complete artifact directory remains
small enough that Git LFS is not needed.

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
`refresh-model`, `check-model`, and `daily`. `bootstrap-negatives` is a
network-backed, deliberate corpus-versioning operation, not part of ordinary
bibliography refreshes. Run any command as
`python -m scripts.paperbot <command> --help` for its narrow options.
