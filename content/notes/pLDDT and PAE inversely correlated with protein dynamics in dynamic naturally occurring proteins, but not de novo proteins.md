---
tags:
  - structure-prediction/sampling
  - conformational-dynamics/modeling
  - plddt
  - pae
created: "2026-02-20T18:11:03"
modified: "2026-04-21T07:03:26"
---

#### Summary

**The [[tags/plddt|pLDDT]] and [[tags/pae|PAE]] of [[tags/alphafold2|AlphaFold2]] predictions is inversely correlated with RMSD between conformations observed experimentally** ([@saldao2022] and Chakravarty and [@chakravarty2022]) **and from [[MD simulations]]** [@jussupow2023; @gavaldagarcia2024]. Low pLDDT is also predictive of intrinsic disorder. However, in *de novo* proteins, pLDDT predictions do not correlate with flexibility, based on studies with [[NMR]] [@mntener2026]. This is a form of [[Uncertainty quantification|aleotoric uncertainty]] in the neural network's confidence prediction module.

#### Figures

![[Pasted-Graphic-2-2.png]]

*Ref [@jussupow2023]*

![[Pasted-image-20240722081109.png]]

*Ref [@gavaldagarcia2024]*

![[Pasted-image-20260220181048.png]]

*Ref [@mntener2026]*
