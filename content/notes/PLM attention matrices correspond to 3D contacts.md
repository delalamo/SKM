---
tags:
  - protein-folding/misc
created: "2025-09-01T08:38:43"
modified: "2026-04-10T14:15:21"
---

## Summary

**[[Attention (machine learning)|Attention]] matrices of [[Protein language models|PLMs]] correspond to 3D contacts** ([Lin et al 2023][^lin2023], [Rao et al 2020][^rao2020], [Bhattacharya et al 2022][^ref]), **and they can be fine-tuned for contact prediction** ([Verkuil et al 2022][^verkuil2022]). The [[Categorical Jacobian method|categorical Jacobian method]] described by [Zhang et al 2024][^zhang2024] is another way to predict these contacts without fine-tuning. Note that this is not true of [[Antibody language models]] ([Burbach and Briney 2024][^burbach2024]).

## See also

* [[Likelihood of predicted contacts by MSA transformer weakly correlate with dwell time in molecular dynamics simulations]]

[^lin2023]: Lin et al. (2023) "Evolutionary-scale prediction of atomic-level protein structure with a language model." *Science*. https://doi.org/10.1126/science.ade2574
[^rao2020]: Rao et al. (2020) "Transformer protein language models are unsupervised structure learners." https://doi.org/10.1101/2020.12.15.422761
[^ref]: Bhattacharya et al. (2021) "Interpreting Potts and Transformer Protein Models Through the Lens of Simplified Attention." *Biocomputing 2022*. https://doi.org/10.1142/9789811250477_0004
[^verkuil2022]: Verkuil et al. (2022) "Language models generalize beyond natural proteins." https://doi.org/10.1101/2022.12.21.521521
[^zhang2024]: Zhang et al. (2024) "Protein language models learn evolutionary statistics of interacting sequence motifs." *Proceedings of the National Academy of Sciences*. https://doi.org/10.1073/pnas.2406285121
[^burbach2024]: Burbach & Briney (2024) "Improving antibody language models with native pairing." *Patterns*. https://doi.org/10.1016/j.patter.2024.100967
