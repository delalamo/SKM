---
tags:
  - protein-structure-tokenization
  - variant-effect-prediction
created: 2024-12-10T01:39:37
modified: "2026-08-19T16:32:04"
---

#### Summary

**In one ESM3 setup, [[protein-structure-tokenization|structural tokens]] improved zero-shot [[variant-effect-prediction|variant effect prediction]] only when using the experimental WT structure** [@loux2024]. Computational models obtained using [[Rosetta]] or short [[MD simulations]] substantially lowered the Spearman correlation, despite the resulting embeddings being almost identical. This does not generalize to all structure-aware PLMs: [[SaProt]] is trained largely on [[alphafold2|AlphaFold2]]-derived Foldseek tokens and benefits from them across downstream tasks, while masking tokens from residues with low [[plddt|pLDDT]] [@su2023].

#### Figures

![[Pasted-image-20241210073124.png]]
![[Pasted-image-20241210073131.png]]
*Figures from [@loux2024]*

#### See also

* [[SaProt]]
