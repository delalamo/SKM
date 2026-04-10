---
title: Guidance sampling of all-atom diffusion
tags:
  - guidance-sampling-of-all-atom-diffusion
created: "2026-04-10T14:30:55"
modified: "2026-04-10T14:30:55"
---

**Sampling guidance in all-atom diffusion** refers to the addition of score terms to the overall [[Diffusion models|diffusion]] process during [[Protein-ligand co-folding|all-atom protein structure prediction]]. It has been used to correct issues with chirality observed in methods like [[AlphaFold|AlphaFold3]] ([[10.1101__2024.11.19.624167|Wohlwend et al 2024]]), to include experimental data during inference ([[10.48550__ARXIV.2506.04490|Raghu et al 2025]], [[10.48550__ARXIV.2602.05285|Li et al 2026]], [[10.48550__arxiv.2502.09372|Maddipatla et al 2025]]), to bias conformational sampling away from specific states ([[U87XyMPrZp|Richman et al 2025]]), and model ensembles ([[10.48550__arxiv.2502.09372|Maddipatla et al 2025]]). In general it uses the Diffusion Posterior Sampling approach.

#### Details

[[10.48550__ARXIV.2602.16634|Xie et al 2026]] outline three types of guidance used by diffusion models:
1. Score guidance, in which gradients from classifiers, constraints, or rewards are used to nudge the diffusion path; this is trivial to implement but does not guarantee sampling of desired end state.
2. Path-integral reweighting, such as Feynman-Kac potentials, which used Sequential Monte Carlo and importance weights to update trajectories. Another example is annealed importance sampling.
3. Invariant correctors, like Metropolis-adjusted Langevin, "that are interleaved with the reverse dynamics to mix within the current biased marginal without changing the FK weights".

<!-- generated -->
