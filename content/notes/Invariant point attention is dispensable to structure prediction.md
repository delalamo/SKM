---
tags:
  - structure-prediction
created: "2024-05-02T17:54:08"
modified: "2026-04-11T06:06:39"
---

#### Summary

The invariant point attention is not mandatory for protein structure prediction ([10.1101__2023.05.24.542179|Baek et al 2023]). In [10.1038__s41586-021-03819-2|Jumper et al 2021], ablation studies show only a small drop in performance, while in RosettaFold, its replacement with an SE3-transformer led to no drop in accuracy. [10.1038__s41586-021-03819-2|Jumper et al 2021] found that removing IPA led to very minor decreases in structure prediction quality, unless recycling was also removed. However, [10.48550__arXiv.2206.06583|Hu et al 2022] found when IPA was replaced with a single linear layer, the Evoformer lost 80% of its ability to predict secondary structure.

#### Figures

\![[Pasted-image-20240418162324.png]]
*Figure from [10.1038__s41586-021-03819-2|Jumper et al 2021]*
