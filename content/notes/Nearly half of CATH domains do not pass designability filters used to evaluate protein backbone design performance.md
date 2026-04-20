---
tags:
  - inverse-folding/evaluation
  - protein-backbone-design/designability
created: "2025-01-20T06:38:07"
modified: "2026-04-20T10:13:23"
---

#### Summary

**Nearly half (43.7%) of CATH domains do not pass designability filters used to evaluate whether [[Protein backbone design|protein backbone design]] methods work or not** [^lu2025]. Designability here refers to designing a sequence onto the structure using [[Inverse folding|inverse folding]], followed by forward folding using a [[Structure prediction|protein structure prediction model]]. This finding is true even when using the native sequence with [[ESMFold]]; with [[AlphaFold2]] in single-sequence mode, the number drops to 1.34% for native sequences.

[^lu2025]: Lu et al. (2025) "Assessing Generative Model Coverage of Protein Structures with SHAPES." https://doi.org/10.1101/2025.01.09.632260
