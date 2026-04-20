---
tags:
  - alphafold3
  - structure-prediction/training
  - plddt
created: "2024-05-11T20:04:05"
modified: "2026-04-20T07:46:00"
---

#### Summary

**[[AlphaFold3]] uses [[Distillation|cross-distillation]] from AlphaFold2 to avoid modeling low-[[pLDDT]] regions that are likely disordered as helices** [@abramson2024]. The authors claim that earlier versions of the method without this check done tended to hallucinate disordered regions as helices, despite low pLDDT.

#### Figures

![[Pasted-Graphic-3-1.png]]

*Figure from [@abramson2024]*
