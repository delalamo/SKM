---
title: Fine-tuned protein language models can struggle to generalize to positions absent from fine-tuning data
modified: "2026-08-19T16:33:06"
created: "2026-04-10T14:16:39"
tags:
  - evidence/generalization
  - training/fine-tuning
  - prediction/variant-effects
---
#### Summary

**Fine-tuned [[notes/Protein language models|protein language models]] generalize poorly to mutations at positions absent from the fine-tuning dataset** [@didi2026]. This is not universal: likelihood-based ranking fine-tuning outperformed embedding-based predictors on positional extrapolation splits, although performance still fell relative to random splits [@hawkinshooker2024].

#### Figures
![[Pasted-image-20260226153311.png]]

*Ref [@didi2026]; blue dots show position-based split*
