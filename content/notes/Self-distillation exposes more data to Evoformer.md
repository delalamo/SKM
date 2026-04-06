---
tags:
  - protein-folding/misc
created: "2024-05-10T00:57:20"
modified: "2026-04-05T23:14:54"
---

#### Summary

**The use of [[Distillation]], where synthetic data are generated and supplement the real data during retraining from scratch, improved structure prediction quality when training [[AlphaFold|AlphaFold2]]** (Jumper et al 2021[^jumper2021]). It is likely due to exposing more sequence tokens in [[Multiple sequence alignments]] to the [[Evoformer]]. In contrast, it was not as effective when training [[ESMFold]].

#### Figures

![](/assets/Pasted-image-20240418162324.png)
*Figure from Jumper et al 2021[^jumper2021]*

[^jumper2021]: Jumper et al. (2021) "Highly accurate protein structure prediction with AlphaFold." *Nature*. https://doi.org/10.1038/s41586-021-03819-2
