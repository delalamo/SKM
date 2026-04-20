---
tags:
  - diffusion-models/structure-prediction
  - diffusion-guidance/structure-prediction
  - protein-folding/structure-prediction
  - structure-prediction/sampling
  - conformational-dynamics/modeling
created: "2026-02-20T18:23:36"
modified: "2026-04-20T08:32:20"
---

#### Summary

Guidance potentials can be added to diffusion-based structure prediction methods for enhanced sampling of protein dynamics [^lam2026][^ohnuki2025]. However, the results do not necessarily reproduce the effectiveness of MSA subsampling.

#### Details

![[Pasted-image-20260220182258.png]]
*Ref [^ohnuki2025]*

![[Pasted-image-20260220182329.png]]
*Ref [^lam2026]*

[^lam2026]: Lam et al. (2026) "Metadiffusion: inference-time meta-energy biasing of biomolecular diffusion models." https://doi.org/10.64898/2026.02.10.704873
[^ohnuki2025]: Ohnuki & Okazaki (2025) "Enhanced sampling of protein conformations in AlphaFold3 with repulsive bias in the diffusion generative model." https://doi.org/10.64898/2025.12.17.693105
