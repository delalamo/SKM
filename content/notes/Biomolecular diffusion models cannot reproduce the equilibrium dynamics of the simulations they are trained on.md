---
tags:
  - diffusion-models/structure-prediction
  - protein-folding/structure-prediction
  - conformational-dynamics/modeling
created: "2025-12-22T11:49:01"
modified: "2026-04-20T07:46:00"
---

#### Summary

**Biomolecular diffusion models cannot reproduce the equilibrium dynamics of the simulations they are trained on** [@plainer2025], and do not always recover the ground states [@sarma2025]. This is due to undersampling at low-$t$ to avoid exploding errors resulting from low variance. A workaround is to use Fokker-Planck regularization during training.

#### Figures

![[Pasted-image-20251114122946.png]]

*Figure from [@plainer2025]*
