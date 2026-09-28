---
title: Diffusion guidance
aliases:
  - "notes/diffusion-guidance"
  - "Guidance sampling of all-atom diffusion"
  - "Diffusion guidance"
  - "tags/diffusion-guidance"
created: 2026-04-10T14:30:55
modified: "2026-09-25"
tags:
  - inference/guidance
---

**Diffusion guidance** refers to inference-time methods that steer a [[notes/Diffusion models|diffusion]] process toward desired properties, constraints, or observations. It is a general concept that applies to both [[notes/Protein backbone design|protein design]], [[notes/Structure prediction|structure prediction]], and sequence-based protein design, of which all-atom diffusion is just one application.

#### Details

Xie et al [@xie2026] outline three broad types of guidance used by diffusion models:

1. Score guidance, in which gradients from classifiers, constraints, or rewards are used to nudge the diffusion path.
2. Path-integral reweighting, such as [[Feynman-Kac steering|Feynman-Kac]] potentials, which use importance weights to update trajectories.
3. Invariant correctors, such as Metropolis-adjusted Langevin methods, which mix within a biased marginal without changing the trajectory weights.

However, other search algorithms such as [[Beam search]] and [[Monte Carlo Tree Search]] have been used in conjunction with diffusion models [@didi2026a].

#### Conformational sampling

[[Guidance potentials can enhance conformational sampling in protein diffusion models|Guidance can promote alternative conformations]] in prediction and supply candidate multistate backbones for design. History-dependent collective-variable biases provide one such strategy [@omidi2026].
