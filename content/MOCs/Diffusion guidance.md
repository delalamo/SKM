---
title: Diffusion guidance
tags:
  - diffusion-guidance
  - citation-fix
aliases:
  - Guidance sampling of all-atom diffusion
created: 2026-04-10T14:30:55
modified: "2026-04-20T10:13:23"
---

**Diffusion guidance** refers to inference-time methods that steer a [[Diffusion models|diffusion]] process toward desired properties, constraints, or observations. It is a general concept that applies to both [[Protein backbone design|protein design]], [[Structure prediction|structure prediction]], and sequence-based protein design, of which all-atom diffusion is just one application.

#### Details

Xie et al (doi.org/10.48550/ARXIV.2602.16634) outline three broad types of guidance used by diffusion models:
1. Score guidance, in which gradients from classifiers, constraints, or rewards are used to nudge the diffusion path.
2. Path-integral reweighting, such as [[Feynman-Kac steering|Feynman-Kac]] potentials, which use importance weights to update trajectories.
3. Invariant correctors, such as Metropolis-adjusted Langevin methods, which mix within a biased marginal without changing the trajectory weights.

However, other search algorithms such as [[Beam search]] and [[Monte Carlo Tree Search]] have been used in conjunction with diffusion models (https://doi.org/10.48550/arXiv.2603.27950).

<!-- generated -->

## Protein Design

- [[Guided sequence-only diffusion outperforms autoregressive fine-tuned PLMs on designing high-fitness sequences]]
- [[Inference-time scaling of de novo designed proteins is more effective for harder targets]]
- [[Multimodal sequence-structure guidance outperforms unimodal guidance in cases where both need to be designed]]
- [[Stronger diffusion guidance reduces diversity of generated outputs]]

## Structure Prediction

- [[Confidence metrics for diffusion-based structure prediction methods can be improved with minimal changes to conditioning representations]]
- [[DL structure tools introduce chiral errors such as swapped chiral centers, D-amino acids, and cis-amide bonds]]
- [[Diffusion-based structure prediction can be steered by modifying the conditioning embeddings rather than the latent space, and such embeddings can be used for subsequent iterations]]
- [[Enhanced diffusion with metadynamics-like potentials can sometimes convergence slower than unbiased diffusion]]
- [[Ensembles can be modeled by structure prediction NNs using experimental data via guidance sampling]]
- [[Guidance potentials can be added to diffusion-based structure prediction for enhanced sampling of protein conformations]]
- [[Multistate Bennett acceptance ratio can be used to reweigh one or more samples from a guided diffusion trajectory]]
- [[Protein backbone design diffusion models can be repurposed for fitting structures into electron density]]
