---
title: Diffusion guidance
aliases:
  - Guidance sampling of all-atom diffusion
  - Diffusion guidance
created: 2026-04-10T14:30:55
modified: "2026-04-20T10:13:23"
---

**Diffusion guidance** refers to inference-time methods that steer a [[tags/diffusion-models|diffusion]] process toward desired properties, constraints, or observations. It is a general concept that applies to both [[tags/protein-backbone-design|protein design]], [[tags/structure-prediction|structure prediction]], and sequence-based protein design, of which all-atom diffusion is just one application.

#### Details

Xie et al [@xie2026] outline three broad types of guidance used by diffusion models:

1. Score guidance, in which gradients from classifiers, constraints, or rewards are used to nudge the diffusion path.
2. Path-integral reweighting, such as [[Feynman-Kac steering|Feynman-Kac]] potentials, which use importance weights to update trajectories.
3. Invariant correctors, such as Metropolis-adjusted Langevin methods, which mix within a biased marginal without changing the trajectory weights.

However, other search algorithms such as [[Beam search]] and [[Monte Carlo Tree Search]] have been used in conjunction with diffusion models [@didi2026a].
