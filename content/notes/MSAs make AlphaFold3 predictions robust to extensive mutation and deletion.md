---
tags:
  - evidence/generalization
  - prediction/structure
  - inference/conditioning
created: "2026-07-19"
modified: "2026-07-20T09:52:04"
---

#### Summary

**[[Multiple sequence alignments|MSAs]] make [[notes/alphafold3|AlphaFold3]] predictions substantially more robust to sequence perturbation.** With evolutionary context, predicted folds can remain stable after roughly 40% of residues are mutated and about 10% are deleted; without an MSA, perturbing approximately 10% of residues can destroy the predicted fold [@feldman2026].

#### See also

- [[Removing MSAs collapses AlphaFold3's latent space]]
- [[MSA-based structure predictions outperform PLM-based methods]]
