---
tags:
  - protein-language-models/training
  - tm-score
created: "2026-04-05T17:45:40"
modified: "2026-04-21T07:28:09"
---

#### Summary

**For structure prediction methods that using language models such as [[OmegaFold]] and [[ESMFold]], unfreezing the [[protein-language-models|language model]] during fine-tuning improves structure prediction [[tm-score|TM-score]].** This was without an [[Evoformer]] module which may skew results.

#### Figures

| Method | Embedder Status | Trunk | TMscore |
|---|---|---|---|
| variant1 | Freeze | 0 Evoformer | 0.53 |
| variant2 | Trainable | 0 Evoformer | 0.60 |
| variant3 | Freeze | 1 Evoformer | 0.63 |
| variant4 | Trainable | 1 Evoformer | 0.61 |

*Ref [@lee2023solvent]*
