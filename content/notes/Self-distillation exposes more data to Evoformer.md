---
tags:
  - structure-prediction
created: "2024-05-10T00:57:20"
modified: "2026-04-11T06:06:39"
---

#### Summary

**The use of [[Distillation]], where synthetic data are generated and supplement the real data during retraining from scratch, improved structure prediction quality when training [[AlphaFold|AlphaFold2]]** [^jumper2021]. It is likely due to exposing more sequence tokens in [[Multiple sequence alignments]] to the [[Evoformer]]. In contrast, it was not as effective when training [[ESMFold]].

#### Figures

\![[Pasted-image-20240418162324.png]]
*Figure from [^jumper2021]*

[^jumper2021]: Jumper et al. (2021) "Highly accurate protein structure prediction with AlphaFold." *Nature*. https://doi.org/10.1038/s41586-021-03819-2
