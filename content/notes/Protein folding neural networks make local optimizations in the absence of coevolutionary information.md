---
tags:
  - structure-prediction/limitations
created: "2024-12-05T07:28:11"
modified: "2026-04-11T07:41:30"
---

## Summary

**[[Structure prediction|Protein folding neural networks]] make local optimizations in the absence of coevolutionary information** ([Gut et al 2024][^gut2024]). This was observed using [[AlphaFold|AlphaFold2]] and includes side chain optimizations and resolution of steric clashes. The observation is consistent with the hypothesis put forth by [Roney & Ovchinnikov][^roney2022] that they learn an energy function but require evolutionary info to traverse the structural space.

## Figures

![[Pasted-image-20241205132400.png]]
*Figure from [Gut et al 2024][^gut2024]*

[^gut2024]: Gut & Lemmin (2024) "Dissecting AlphaFold2’s capabilities with limited sequence information." *Bioinformatics Advances*. https://doi.org/10.1093/bioadv/vbae187
[^roney2022]: Roney & Ovchinnikov (2022) "State-of-the-Art Estimation of Protein Model Accuracy Using AlphaFold." *Physical Review Letters*. https://doi.org/10.1103/PhysRevLett.129.238101
