---
tags:
  - structure-prediction/sampling
  - conformational-dynamics/modeling
  - plddt
  - pae
created: "2026-02-20T18:11:03"
modified: "2026-04-20T08:16:13"
---

#### Summary

**The [[pLDDT]] and [[Predicted aligned error|PAE]] of [[AlphaFold2]] predictions is inversely correlated with RMSD between conformations observed experimentally** ([^saldao2022] and Chakravarty and [^chakravarty2022]) **and from [[MD simulations]]** [^jussupow2023][^gavaldagarcia2024]. Low pLDDT is also predictive of intrinsic disorder. However, in *de novo* proteins, pLDDT predictions do not correlate with flexibility, based on studies with [[NMR]] [^mntener2026]. This is a form of [[Uncertainty quantification|aleotoric uncertainty]] in the neural network's confidence prediction module.

#### Figures

![[Pasted-Graphic-2-2.png]]

*Ref [^jussupow2023]*

![[Pasted-image-20240722081109.png]]

*Ref [^gavaldagarcia2024]*

![[Pasted-image-20260220181048.png]]

*Ref [^mntener2026]*

[^saldao2022]: Saldaño et al. (2022) "Impact of protein conformational diversity on AlphaFold predictions." *Bioinformatics*. https://doi.org/10.1093/bioinformatics/btac202
[^chakravarty2022]: Chakravarty & Porter (2022) "AlphaFold2
                    fails to predict protein fold switching." *Protein Science*. https://doi.org/10.1002/pro.4353
[^jussupow2023]: Jussupow & Kaila (2023) "Effective Molecular Dynamics from Neural Network-Based Structure Prediction Models." *Journal of Chemical Theory and Computation*. https://doi.org/10.1021/acs.jctc.2c01027
[^gavaldagarcia2024]: Gavalda-Garcia et al. (2025) "Gradations in protein dynamics captured by experimental NMR are not well represented by AlphaFold2 models and other computational metrics." Journal of Molecular Biology. https://doi.org/10.1016/j.jmb.2024.168900
[^mntener2026]: Müntener et al. (2026) "Large-scale exploration of protein space by automated NMR." https://doi.org/10.64898/2026.02.16.706194
