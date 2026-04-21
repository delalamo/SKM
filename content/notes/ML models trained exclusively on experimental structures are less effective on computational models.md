---
tags:
  - inverse-folding/training
  - protein-language-models/training
created: 2025-07-22T11:37:28
modified: "2026-04-21T07:03:26"
---

#### Summary

**ML models trained exclusively on experimental structures are less effective on computational models** [@huang2024; @su2023]. [@huang2024] attributed this to "structure embedding bias", hypothesize that improvements in structure prediction are not predicted to remove this bias, and address it using [[tags/contrastive-learning|contrastive learning]]. [@su2023] observe this in a version of SaProt which is trained on [[Foldseek]] tokens derived from PDB structures rather than [[tags/alphafold2|AlphaFold2]] models.

#### See also

* [[Training inverse folding and diffusion models exclusively on predicted protein structures worsens performance due to how locally perfect they are]]
* [[Contrastive fine-tuning PLMs on inverse folding embeddings of experimental structures but not computational models improves downstream tasks]]
