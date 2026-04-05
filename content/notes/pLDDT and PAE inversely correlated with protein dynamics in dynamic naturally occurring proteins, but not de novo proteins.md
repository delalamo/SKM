---
tags:
  - protein-folding/misc
---

#### Summary

**The [[pLDDT]] and [[Predicted aligned error|PAE]] of [[AlphaFold|AlphaFold2]] predictions is inversely correlated with RMSD between conformations observed experimentally** (Saldaño et al 2022[^saldao2022] and Chakravarty and Porter 2022[^chakravarty2022]) **and from [[MD simulations]]** (Jussupow & Kaila 2023[^jussupow2023], Gavalda-Garcia et al 2024[^gavaldagarcia2024]). Low pLDDT is also predictive of intrinsic disorder. However, in *de novo* proteins, pLDDT predictions do not correlate with flexibility, based on studies with [[NMR]] (Müntener et al 2026[^mntener2026]). This is a form of [[Uncertainty quantification|aleotoric uncertainty]] in the neural network's confidence prediction module.

#### Figures

![](/assets/Pasted-Graphic-2-2.png)

*Figure from Jussupow & Kaila 2023[^jussupow2023]*

![](/assets/Pasted-image-20240722081109.png)

*Figure from Gavalda-Garcia et al 2024[^gavaldagarcia2024]*

![](/assets/Pasted-image-20260220181048.png)

*Figure from Müntener et al 2026[^mntener2026]*

[^saldao2022]: Saldaño et al. (2022) "Impact of protein conformational diversity on AlphaFold predictions." *Bioinformatics*. https://doi.org/10.1093/bioinformatics/btac202
[^chakravarty2022]: Chakravarty & Porter (2022) "AlphaFold2
                    fails to predict protein fold switching." *Protein Science*. https://doi.org/10.1002/pro.4353
[^jussupow2023]: Jussupow & Kaila (2023) "Effective Molecular Dynamics from Neural Network-Based Structure Prediction Models." *Journal of Chemical Theory and Computation*. https://doi.org/10.1021/acs.jctc.2c01027
[^gavaldagarcia2024]: Gavalda-Garcia et al. (2024) "Gradations in protein dynamics captured by experimental NMR are not well represented by AlphaFold2 models and other computational metrics." https://doi.org/10.1101/2024.07.17.603933
[^mntener2026]: Müntener et al. (2026) "Large-scale exploration of protein space by automated NMR." https://doi.org/10.64898/2026.02.16.706194
