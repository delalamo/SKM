---
title: Diffusion guidance
tags:
  - diffusion-models
created: "2026-07-19"
modified: "2026-07-20T09:52:04"
---

#### Summary

**Diffusion guidance** modifies a [[diffusion-models|diffusion model's]] denoising trajectory to favor samples with desired properties. Classifier guidance adds gradients from an external predictor, whereas classifier-free guidance combines conditional and unconditional model predictions without a separate classifier [@dieleman2023].

Guidance improves control but changes the sampled distribution and can reduce diversity when weighted too strongly.

#### See also

- [[Stronger diffusion guidance reduces diversity of generated outputs]]
- [[Feynman-Kac steering]]
- [[Guidance potentials can be added to diffusion-based structure prediction for enhanced sampling of protein conformations]]
