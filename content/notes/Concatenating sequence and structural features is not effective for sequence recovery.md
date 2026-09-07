---
tags:
  - model-design/multimodal
  - inference/feature-extraction
title: Naive concatenation can underperform learned sequence-structure fusion
created: 2026-04-05T17:27:14
modified: "2026-08-19T16:32:04"
---

#### Summary

**Naively concatenating sequence and structural embeddings can underperform learned fusion mechanisms or sequence embeddings alone.** Concatenating [[ESM|ESM-1b]] and GEARNet features was less effective than cross-attention, ESM-to-GEARNet, or ESM-1b alone [@zhang2023]. [@detlefsen2022] similarly found that concatenation was outperformed by a ResNet autoencoder bottleneck. This does not imply that the modalities are inherently redundant: SPDesign obtained synergistic [[notes/Inverse folding|inverse-folding]] gains by combining structural sequence profiles, pretrained structural knowledge, and geometric features [@wang2024spdesign].

#### Figures

| Method | F_max | AUPR |
|---|---|---|
| **ESM-1b** | 0.864 | 0.889 |
| **ESM-GearNet** | | |
| - w/ parallel fusion | 0.733 | 0.759 |
| - w/ series fusion | **0.883** | 0.890 |
| - w/ cross fusion | 0.880 | **0.893** |

*Ref [@zhang2023]*

#### See also

* [[The effect of including both sequence and structural features can be synergistic]]
