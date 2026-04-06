---
title: BERT-based inverse folding models generate overly repetitive sequences
tags:
  - protein-design/misc
created: "2025-01-23T05:03:29"
modified: "2026-04-05T23:36:09"
---
#### Summary
 **[[BERT]]-based [[Inverse folding|inverse folding]] models generate overly repetitive sequences** [^kim2024]. This can be avoided by retraining the models with custom losses that look at overall sequence composition.

#### Details
The loss function used to improve repetitive sequences is as follows:
$$
\mathcal{L}_{comp}(\theta) = \mathbb{E}\left(d(\mathbf{s}, \mathbf{\hat{s}})\right)
$$
$$
d(\mathbf{s}, \mathbf{\hat{s}})=-cos(\mathbf{y}, \mathbf{\hat{y}})=-\frac{\mathbf{y}^{T}\mathbf{\hat{y}}}{\|\mathbf{y}\| \|\mathbf{\hat{y}}\|}
$$

#### Figures
![](/assets/Pasted-image-20250123105651.png)
*Figure from [^kim2024]*

[^kim2024]: Kim et al. (2024) "Decoupled Sequence and Structure Generation for Realistic Antibody Design." *arXiv*. https://doi.org/10.48550/ARXIV.2402.05982
