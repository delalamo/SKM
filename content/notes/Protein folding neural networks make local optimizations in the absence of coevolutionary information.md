---
tags:
  - structure-prediction/limitations
  - alphafold2
created: "2024-12-05T07:28:11"
modified: "2026-04-21T07:28:09"
---

## Summary

**[[structure-prediction|Protein folding neural networks]] make local optimizations in the absence of coevolutionary information** [@gut2024]. This was observed using [[alphafold2|AlphaFold2]] and includes side chain optimizations and resolution of steric clashes. The observation is consistent with the hypothesis put forth by Roney & Ovchinnikov [@roney2022] that they learn an energy function but require evolutionary info to traverse the structural space.

## Figures

![[Pasted-image-20241205132400.png]]
*Ref [@gut2024]*
