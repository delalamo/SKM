---
tags:
  - protein-folding/misc
created: "2026-04-05T17:45:40"
modified: "2026-04-10T14:30:55"
---

#### Summary

**For structure prediction methods that using language models such as [[OmegaFold]] and [[ESMFold]], unfreezing the [[Protein language models|language model]] during fine-tuning improves structure prediction [[TM-score]].** This was without an [[Evoformer]] module which may skew results.

#### Figures

| Method | Embedder Status | Trunk | TMscore |
|---|---|---|---|
| variant1 | Freeze | 0 Evoformer | 0.53 |
| variant2 | Trainable | 0 Evoformer | 0.60 |
| variant3 | Freeze | 1 Evoformer | 0.63 |
| variant4 | Trainable | 1 Evoformer | 0.61 |

*Figure from [^lee2023]*

[^lee2023]: Lee et al. (2023) "Solvent: A Framework for Protein Folding." https://doi.org/10.48550/arXiv.2307.04603
