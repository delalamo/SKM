---
tags:
  - prediction/structure
  - inference/guidance
  - evidence/measurements
created: "2026-09-15"
modified: "2026-09-25"
---

#### Summary

**A pretrained protein [[Diffusion models|diffusion]] prior improves reconstruction from sparse structural measurements** [@levy2024]. However, since the problem is ill-posed, plausible reconstruction does not necessarily mean that the measurements are sufficient to uniquely determine the structure, and under severe undersampling, the model can produce plausible structures far from the reference.

#### Figures

![[adp3d-sparse-distance-reconstruction.png]]
*Ref [@levy2024]*

#### See also

- [[Protein backbone design diffusion models can be repurposed for fitting structures into electron density]]
- [[Diffusion guidance]]
- [[Computational models of proteins fit NMR data better than models designed using classical approaches]]
