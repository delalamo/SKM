---
tags:
  - structure-prediction/limitations
  - alphafold2
created: "2024-05-08T18:04:24"
modified: "2026-04-21T07:28:09"
---

## Summary

**[[structure-prediction#Methods|Protein folding neural networks]] can be subject to adversarial attacks.** Small, calculated changes in AA sequence via adversarial attacks can lead to huge RMSD changes in [[alphafold2|AlphaFold2]] and [[rosettafold|RosettaFold]], and there are strategies to identify these ([@jha2021], [@alkhouri2023], [@yuan2023]). This is compared to adversarial attacks in vision NNs. It is unclear how correlated to weaknesses of these NNs are.

## See also

* [[Inversion of protein folding neural networks]]
