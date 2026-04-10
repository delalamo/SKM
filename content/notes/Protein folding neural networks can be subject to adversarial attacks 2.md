---
tags:
  - protein-folding/misc
created: "2024-05-08T18:04:24"
modified: "2026-04-10T14:30:55"
---

## Summary

**[[Structure prediction#Methods|Protein folding neural networks]] can be subject to adversarial attacks.** Small, calculated changes in AA sequence via adversarial attacks can lead to huge RMSD changes in [[AlphaFold|AlphaFold2]] and [[RosettaFold]], and there are strategies to identify these ([Jha et al 2021][^jha2021], [Alkhouri et al 2023][^alkhouri2023], [Yuan et al 2023][^yuan2023]). This is compared to adversarial attacks in vision NNs. It is unclear how correlated to weaknesses of these NNs are.

## See also

* [[Inversion of protein folding neural networks]]

[^jha2021]: Jha et al. (2021) "Protein Folding Neural Networks Are Not Robust." https://doi.org/10.48550/arXiv.2109.04460
[^alkhouri2023]: Alkhouri et al. (2023) "On the Robustness of AlphaFold: A COVID-19 Case Study." https://doi.org/10.48550/arXiv.2301.04093
[^yuan2023]: Yuan et al. (2023) "AF2-Mutation: Adversarial Sequence Mutations against AlphaFold2 on Protein Tertiary Structure Prediction." *arXiv*. https://doi.org/10.48550/arXiv.2305.08929
