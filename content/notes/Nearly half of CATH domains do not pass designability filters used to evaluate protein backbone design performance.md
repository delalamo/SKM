---
tags:
  - evidence/design-validation
  - design/backbones
created: "2025-01-20T06:38:07"
modified: "2026-04-21T07:28:09"
---

#### Summary

**Nearly half (43.7%) of CATH domains do not pass designability filters used to evaluate whether [[notes/protein-backbone-design|protein backbone design]] methods work or not** [@lu2025]. Designability here refers to designing a sequence onto the structure using [[notes/inverse-folding|inverse folding]], followed by forward folding using a [[notes/structure-prediction|protein structure prediction model]]. This finding is true even when using the native sequence with [[ESMFold]]; with [[notes/alphafold2|AlphaFold2]] in single-sequence mode, the number drops to 1.34% for native sequences.
