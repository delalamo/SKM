---
tags:
  - structure-prediction/training
created: "2024-05-10T00:57:20"
modified: "2026-04-20T07:46:00"
---

#### Summary

**The use of [[Distillation]], where synthetic data are generated and supplement the real data during retraining from scratch, improved structure prediction quality when training [[AlphaFold2]]** [@jumper2021]. It is likely due to exposing more sequence tokens in [[Multiple sequence alignments]] to the [[Evoformer]]. In contrast, it was not as effective when training [[ESMFold]].

#### Figures

![[Pasted-image-20240418162324.png]]
*Figure from [@jumper2021]*
