---
title: Straight-through estimator
aliases:
  - Straight-through trick
  - Straight-through gradient estimator
tags:
  - training/objectives-and-optimization
  - model-design/multimodal
  - inference/guidance
created: "2026-07-19"
modified: "2026-07-19T10:07:27"
---

#### Summary

The **straight-through estimator** (STE, also called straight-through trick) uses both a hard/discrete value and a soft value in the forward pass, thereby allowing gradients to flow through its continuous input during backpropagation: $y = \operatorname{hard}(x) - \operatorname{stopgrad}(x) + x$, where $y=\operatorname{hard}(x)$ is the forward pass, and $\partial y/\partial x \approx 1$ in the backward pass. This allows rounding, `argmax`, quantization, etc., and is practically applied to do discrete sequence optimization in [[Inversion of protein folding neural networks|protein design by hallucination]] and codebook lookups in [[Variational autoencoders|VQ-VAEs]]. 

#### See also

- [[Inversion of protein folding neural networks]]
- [[Variational autoencoders]]
- [[Protein sequence and structure compression using VQ-VAE tokens is prone to codebook collapse]]
- [[Categorical Jacobian method]]
- [[Loss functions]]
