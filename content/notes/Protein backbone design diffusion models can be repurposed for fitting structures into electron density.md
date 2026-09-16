---
tags:
  - prediction/ensembles
  - evidence/measurements
  - inference/guidance
created: "2024-12-31T07:33:08"
modified: "2026-09-16T12:00:34"
---

#### Summary

**[[notes/Protein backbone design|Protein backbone design]] methods can be repurposed for modeling [[Protein dynamics|dynamics]] into electron density derived from either [[X-ray-crystallography|crystallography]] or [[cryo-EM]]** [@maddipatla2024]. Here the method [[Chroma]] was used, and fit to electron density was captured as a score that could supplement the score used by the diffusion model. The same kind of guidance does not require experimental density: shape potentials can steer backbone diffusion toward arbitrary user-specified global protein shapes [@qi2026_D].

#### Figures

![[Pasted-image-20241231133007.png]]

*Ref [@maddipatla2024]*

#### Details

ADP-3D similarly uses a pretrained Chroma denoiser as a prior for fitting and completing atomic models in cryo-EM maps [@levy2024]. It alternates denoising with measurement-fitting steps and combines density, sequence, and partial-model information. This supplies additional evidence for repurposing a backbone generator without training a dedicated model for each measurement type. Its [[Diffusion priors improve reconstruction from sparse distances without guaranteeing a unique structure|sparse-distance experiments]] also illustrate why realistic completion should not be confused with uniquely determined experimental structure.

#### See also

- [[Diffusion guidance]]
- [[Diffusion priors improve reconstruction from sparse distances without guaranteeing a unique structure]]
