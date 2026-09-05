---
tags:
  - evidence/design-validation
  - design/binders
  - inference/ensembling
created: "2026-08-25"
modified: "2026-08-25T13:38:32"
---

#### Summary

**Ensembling ESMFold2, ESMFold2-Fast, and [[notes/alphafold3|Protenix-v2]] [[notes/tm-score|confidence scores]] improves filtering of *de novo* protein-binder designs** [@claudescience2026]. On a public benchmark of 3,532 designs against 13 targets, including 391 experimentally confirmed binders, the per-target z-score ensemble reached a macro-average precision of 0.66, compared with 0.62 for ESMFold2-Fast, 0.61 for ESMFold2, and 0.55 for [[notes/alphafold3|AlphaFold3]]. Adding self-consistency [[DockQ]] at one-quarter the weight of ipSAE did not improve discrimination.

#### See also

- [[Effectiveness of filtering metrics for de novo minibinder design vary by target]]
- [[Protein structure prediction and design confidence metrics do not correlate with binding affinity]]
