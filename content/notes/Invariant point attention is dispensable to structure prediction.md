---
tags:
  - structure-prediction/architecture
created: "2024-05-02T17:54:08"
modified: "2026-04-21T07:02:30"
---

#### Summary

The [[Invariant point attention]] module from [[alphafold2|Alphafold2]] is not mandatory for protein structure prediction [@baek2023]. In [@jumper2021], ablation studies show only a small drop in performance, while in RosettaFold, its replacement with an SE3-transformer led to no drop in accuracy. [@jumper2021] found that removing IPA led to very minor decreases in structure prediction quality, unless recycling was also removed. However, [@hu2022] found when IPA was replaced with a single linear layer, the Evoformer lost 80% of its ability to predict secondary structure.

#### Figures

![[Pasted-image-20240418162324.png]]
*Ref [@jumper2021]*
