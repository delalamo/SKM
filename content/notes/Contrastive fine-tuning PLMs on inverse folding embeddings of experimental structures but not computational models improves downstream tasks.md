---
tags:
  - protein-language-models/antibodies
  - contrastive-learning
created: 2025-07-22T11:37:28
modified: "2026-04-20T08:32:20"
---

#### Summary

**Contrastive fine-tuning of protein language models outputs using embeddings from inverse folding models improves downstream classification tasks** [^barton2023][^liu2024][^wang2023]. [^barton2023] used contrastive learning to fine-tune AntiBERTa2, AntiBERTy, and ESM2 to match those of ESM-IF, improving antigen classification; importantly, this only worked on experimental structures, and not computational models. [^liu2024] and [^wang2023] used a similar student-teacher training scheme to fine-tune ESM on structural data, and they also relied on contrastive learning, but they did not train on computational models. [^wang2023] found that family-level classification was the only case where default ESM outperformed the contrastive learning-improved version, and that the use of low-rank adaptation sometimes but not always led to improvements in prediction.

#### Figures

![[including-ab-models-doesnt-improve-property-prediction.png]]

*Ref [^barton2023]*

#### See also

- [[Training inverse folding and diffusion models exclusively on predicted protein structures worsens performance due to how locally perfect they are]]

[^barton2023]: Barton et al. (2024) "Enhancing Antibody Language Models with Structural Information." https://doi.org/10.1101/2023.12.12.569610
[^liu2024]: Liu et al. (2024) "Interpretable antibody-antigen interaction prediction by introducing route and priors guidance." https://doi.org/10.1101/2024.03.09.584264
[^wang2023]: Wang et al. (2025) "S‐PLM: Structure‐Aware Protein Language Model via Contrastive Learning Between Sequence and Structure." Advanced Science. https://doi.org/10.1002/advs.202404212
