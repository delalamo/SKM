---
title: ESM-IF
tags:
  - esm-if
created: "2026-04-10T14:02:57"
modified: "2026-04-13T11:11:20"
---

**ESM-IF** is an [[Inverse folding]] method that uses twelve million [[AlphaFold|AlphaFold2]] structures during training, in addition to PDB. It uses an encoder-decoder [[Transformer]] architecture with a [[Geometric Vector Perceptrons|GVP]] as well as fixed-order decoding (autoregressive).

![[ESM-IF.png]]
*Figure from [^hsu2022]* 

<!-- generated -->

[^hsu2022]: Hsu et al. (2022) "Learning inverse folding from millions of predicted structures." https://doi.org/10.1101/2022.04.10.487779
