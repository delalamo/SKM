---
tags:
  - structure-prediction/limitations
  - alphafold2
created: "2024-05-08T18:04:24"
modified: "2026-04-20T07:46:00"
---

## Summary

**[[Structure prediction#Methods|Protein folding neural networks]] can be subject to adversarial attacks.** Small, calculated changes in AA sequence via adversarial attacks can lead to huge RMSD changes in [[AlphaFold2]] and [[RosettaFold]], and there are strategies to identify these (Jha et al 2021 [@jha2021], Alkhouri et al 2023 [@alkhouri2023], Yuan et al 2023 [@yuan2023]). This is compared to adversarial attacks in vision NNs. It is unclear how correlated to weaknesses of these NNs are.

## See also

* [[Inversion of protein folding neural networks]]
