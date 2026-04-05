---
tags:
  - protein-folding/misc
---

#### Summary

**ML models trained exclusively on experimental structures are less effective on computational models** (Huang et al 2023b[^huang2023], Su et al 2023[^su2023]). Huang et al 2023b[^huang2023] attributed this to "structure embedding bias", hypothesize that improvements in structure prediction are not predicted to remove this bias, and address it using [[Contrastive learning|contrastive learning]]. Su et al 2023[^su2023] observe this in a version of SaProt which is trained on [[Foldseek]] tokens derived from PDB structures rather than [[AlphaFold]] models.

#### See also

* [[Training inverse folding and diffusion models exclusively on predicted protein structures worsens performance due to how locally perfect they are]]
* [[Contrastive fine-tuning PLMs on inverse folding embeddings of experimental structures but not computational models improves downstream tasks]]

[^huang2023]: Huang et al. (2023) "Protein 3D Graph Structure Learning for Robust Structure-based Protein Property Prediction." https://doi.org/10.48550/arXiv.2310.11466
[^su2023]: Su et al. (2023) "SaProt: Protein Language Modeling with Structure-aware Vocabulary." https://doi.org/10.1101/2023.10.01.560349
