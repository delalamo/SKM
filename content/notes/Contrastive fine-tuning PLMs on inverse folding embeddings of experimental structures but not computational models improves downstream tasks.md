---
tags:
  - protein-language-models/antibodies
  - contrastive-learning
created: 2025-07-22T11:37:28
modified: "2026-04-20T07:46:00"
---

#### Summary

**Contrastive fine-tuning of protein language models outputs using embeddings from inverse folding models improves downstream classification tasks** [@barton2023; @liu2024interpretable; @wang2025]. [@barton2023] used contrastive learning to fine-tune AntiBERTa2, AntiBERTy, and ESM2 to match those of ESM-IF, improving antigen classification; importantly, this only worked on experimental structures, and not computational models. [@liu2024interpretable; @wang2025] used a similar student-teacher training scheme to fine-tune ESM on structural data, and they also relied on contrastive learning, but they did not train on computational models. [@wang2025] found that family-level classification was the only case where default ESM outperformed the contrastive learning-improved version, and that the use of low-rank adaptation sometimes but not always led to improvements in prediction.

#### Figures

![[including-ab-models-doesnt-improve-property-prediction.png]]

*Figure from [@barton2023]*

#### See also

- [[Training inverse folding and diffusion models exclusively on predicted protein structures worsens performance due to how locally perfect they are]]
