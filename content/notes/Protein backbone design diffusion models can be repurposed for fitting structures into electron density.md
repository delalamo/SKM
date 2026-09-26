---
tags:
  - prediction/ensembles
  - evidence/measurements
  - inference/guidance
created: "2024-12-31T07:33:08"
modified: "2026-09-25"
---

#### Summary

**[[notes/Protein backbone design|Protein backbone design]] methods can be repurposed for modeling [[Protein dynamics|dynamics]] into electron density derived from either [[X-ray-crystallography|crystallography]] or [[cryo-EM]]** [@maddipatla2024]. Here the method [[Chroma]] was used, and fit to electron density was captured as a score that could supplement the score used by the diffusion model. The same kind of guidance does not require experimental density: shape potentials can steer backbone diffusion toward arbitrary user-specified global protein shapes [@qi2026_D].

#### Figures

![[Pasted-image-20241231133007.png]]

*Ref [@maddipatla2024]*

#### Related reconstruction problems

[[Diffusion priors improve reconstruction from sparse distances without guaranteeing a unique structure|Sparse-distance reconstruction uses a related diffusion prior]], but a plausible completion does not establish that the measurements determine a unique structure.
