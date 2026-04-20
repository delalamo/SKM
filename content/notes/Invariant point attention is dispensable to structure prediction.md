---
tags:
  - structure-prediction/architecture
created: "2024-05-02T17:54:08"
modified: "2026-04-20T08:32:20"
---

#### Summary

The invariant point attention is not mandatory for protein structure prediction [^baek2023]. In [^jumper2021], ablation studies show only a small drop in performance, while in RosettaFold, its replacement with an SE3-transformer led to no drop in accuracy. [^jumper2021] found that removing IPA led to very minor decreases in structure prediction quality, unless recycling was also removed. However, [^hu2022] found when IPA was replaced with a single linear layer, the Evoformer lost 80% of its ability to predict secondary structure.

#### Figures

![[Pasted-image-20240418162324.png]]
*Ref [^jumper2021]*

[^baek2023]: Baek et al. (2023) "Efficient and accurate prediction of protein structure using RoseTTAFold2." https://doi.org/10.1101/2023.05.24.542179
[^hu2022]: Hu et al. (2022) "Exploring evolution-aware & -free protein language models as protein function predictors." NeurIPS. http://papers.nips.cc/paper_files/paper/2022/hash/fe066022bab2a6c6a3c57032a1623c70-Abstract-Conference.html
[^jumper2021]: Jumper et al. (2021) "Highly accurate protein structure prediction with AlphaFold." *Nature*. https://doi.org/10.1038/s41586-021-03819-2
