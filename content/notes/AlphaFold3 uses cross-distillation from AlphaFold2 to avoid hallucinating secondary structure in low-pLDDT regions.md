---
tags:
  - protein-folding/misc
---

#### Summary

**[[AlphaFold|AlphaFold3]] uses [[Distillation|cross-distillation]] from AlphaFold2 to avoid modeling low-[[pLDDT]] regions that are likely disordered as helices** (Abramson et al 2024[^abramson2024]). The authors claim that earlier versions of the method without this check done tended to hallucinate disordered regions as helices, despite low pLDDT.

#### Figures

![](/assets/Pasted-Graphic-3-1.png)

*Figure from Abramson et al 2024[^abramson2024]*

[^abramson2024]: Abramson et al. (2024) "Accurate structure prediction of biomolecular interactions with AlphaFold 3." *Nature*. https://doi.org/10.1038/s41586-024-07487-w
