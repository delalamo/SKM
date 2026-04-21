---
title: BERT-based inverse folding models generate overly repetitive sequences
tags:
  - inverse-folding/evaluation
created: "2025-01-23T05:03:29"
modified: "2026-04-21T07:28:09"
---
#### Summary
 **[[BERT]]-based [[inverse-folding|inverse folding]] models generate overly repetitive sequences** [@kim2024]. This can be avoided by retraining the models with custom losses that look at overall sequence composition.

#### Details
The loss function used to improve repetitive sequences is as follows:
$$
\mathcal{L}_{comp}(\theta) = \mathbb{E}\left(d(\mathbf{s}, \mathbf{\hat{s}})\right)
$$
$$
d(\mathbf{s}, \mathbf{\hat{s}})=-cos(\mathbf{y}, \mathbf{\hat{y}})=-\frac{\mathbf{y}^{T}\mathbf{\hat{y}}}{\|\mathbf{y}\| \|\mathbf{\hat{y}}\|}
$$

#### Figures
![[Pasted-image-20250123105651.png]]
*Ref [@kim2024]*
