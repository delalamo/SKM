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

#### Alternating diffusion and measurement fitting

ADP-3D uses a pretrained Chroma denoiser as a prior for fitting and completing atomic models in cryo-EM maps [@levy2024]. It alternates denoising with measurement-fitting steps and combines density, sequence, and partial-model information. This extends the evidence for reusing a backbone generator without training a dedicated model for each measurement type.

As with other [[notes/Diffusion guidance|measurement-guided diffusion]] procedures, realistic completion should not be confused with a uniquely determined experimental structure.

#### Figures

![[Pasted-image-20241231133007.png]]

*Ref [@maddipatla2024]*
