---
tags:
  - protein-folding/misc
created: "2026-04-05T17:27:14"
modified: "2026-04-10T14:30:55"
---

#### Summary

**Concatenating features from ESM-1b and GEARNet was found to be less effective than either cross-attention, ESM-to-GearNet, or even just ESM-1b embeddings alone** [^zhang2023]. Meanwhile, [^detlefsen2022] found that concatenation was outperformed by the use of ResNet as an autoencoder bottleneck.

#### Figures

| Method | F_max | AUPR |
|---|---|---|
| **ESM-1b** | 0.864 | 0.889 |
| **ESM-GearNet** | | |
| - w/ parallel fusion | 0.733 | 0.759 |
| - w/ series fusion | **0.883** | 0.890 |
| - w/ cross fusion | 0.880 | **0.893** |

*Figure from [^zhang2023]*

[^zhang2023]: Zhang et al. (2023) "A Systematic Study of Joint Representation Learning on Protein Sequences and Structures." https://doi.org/10.48550/arXiv.2303.06275
[^detlefsen2022]: Detlefsen et al. (2022) "Learning meaningful representations of protein sequences." *Nature Communications*. https://doi.org/10.1038/s41467-022-29443-w
