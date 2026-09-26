---
aliases:
  - "Guidance potentials can be added to diffusion-based structure prediction for enhanced sampling of protein conformations"
  - "notes/Guidance potentials can be added to diffusion-based structure prediction for enhanced sampling of protein conformations"
tags:
  - prediction/ensembles
  - inference/guidance
created: "2026-02-20T18:23:36"
modified: "2026-09-25"
---

#### Summary

**Guidance potentials can enhance conformational sampling in protein diffusion models for both structure prediction and design** [@lam2026; @ohnuki2025; @omidi2026]. In prediction, the results do not necessarily reproduce the effectiveness of MSA subsampling [@lam2026; @ohnuki2025].

#### Design-time ensemble sampling

Diff-Switch applies a history-dependent bias along user-specified collective variables to diversify global domain arrangements while preserving local domain geometry. Inspired by [[Metadynamics]], it discourages repeatedly sampling the same arrangement and produces candidate states for multistate [[Inverse folding]] [@omidi2026]. This extends the role of [[Diffusion guidance]] from exploring a given sequence's conformations to supplying backbone ensembles for sequence design.

These applications do not establish universally faster or more faithful sampling: [[Enhanced diffusion with metadynamics-like potentials can sometimes convergence slower than unbiased diffusion|metadynamics-like diffusion can converge more slowly in some settings]].

#### Details

![[Pasted-image-20260220182258.png]]
*Ref [@ohnuki2025]*

![[Pasted-image-20260220182329.png]]
*Ref [@lam2026]*
