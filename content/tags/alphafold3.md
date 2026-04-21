---
title: Alphafold3
aliases:
  - Alphafold3
created: "2026-04-11T06:06:39"
modified: "2026-04-20T10:13:23"
---

**AlphaFold3** is a [[diffusion-models|diffusion]]-based all-atom [[structure-prediction|structure prediction]] method that is widely seen as state-of-the-art.

![[Pasted-Graphic-4.png]]
_Architecture of AlphaFold3 from Abramson et al. [@abramson2024]_

#### Architectural and ML contributions

- PairFormer
- PDE: predicted distance error (replacing frame aligned point error)
- Non-equivariant per-atom prediction, which leads to [[DL structure tools introduce chiral errors such as swapped chiral centers, D-amino acids, and cis-amide bonds|occasional errors when predicting chirality]]
- [[Distillation|Cross-distillation]] from [[alphafold2|AlphaFold2]]-Multimer v2.3 to avoid hallucination of low-[[plddt|pLDDT]] regions
