---
tags:
  - protein-folding/misc
created: "2025-12-22T11:49:01"
modified: "2026-04-10T14:02:57"
---

#### Summary

**Biomolecular diffusion models cannot reproduce the equilibrium dynamics of the simulations they are trained on** [^plainer2025], and do not always recover the ground states [^sarma2025]. This is due to undersampling at low-$t$ to avoid exploding errors resulting from low variance. A workaround is to use Fokker-Planck regularization during training.

#### Figures

\![[Pasted-image-20251114122946.png]]

*Figure from [^plainer2025]*

[^plainer2025]: Plainer et al. (2025) "Consistent Sampling and Simulation: Molecular Dynamics with Energy-Based Diffusion Models." https://doi.org/10.48550/ARXIV.2506.17139
[^sarma2025]: Sarma et al. (2025) "Can We Extract Physics-like Energies from Generative Protein Diffusion Models?." https://doi.org/10.1101/2025.11.28.690021
