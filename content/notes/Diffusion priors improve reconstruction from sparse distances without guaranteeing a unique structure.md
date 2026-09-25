---
tags:
  - prediction/structure
  - inference/guidance
  - evidence/measurements
created: "2026-09-15"
modified: "2026-09-25"
---

#### Summary

**A pretrained protein [[Diffusion models|diffusion]] prior improves reconstruction from sparse structural measurements, but plausible reconstruction does not establish that the measurements uniquely determine the structure** [@levy2024]. The distinction is between filling missing coordinates using a learned prior and obtaining additional experimental evidence.

#### Details

ADP-3D alternates measurement fitting with denoising, usually using Chroma, to estimate a maximum-a-posteriori structure. It can use partial coordinates, cryo-EM density, or sampled Cα distances without training a separate model for each measurement type.

For a 127-residue BRD4 domain (PDB 7R5B), representative best-of-eight reconstructions reached 1.07 Å RMSD with 500 known distances and 0.93 Å with 4,000 (Figure 4). The curve averages best-of-eight results over ten randomly sampled distance sets. These are exact distances sampled from a reference structure, not a benchmark using noisy experimental NMR restraints.

Under severe undersampling, the model can produce plausible structures far from the reference (Appendix G.1). Inferring that missing information remains ambiguous follows from this result; it does not mean that priors cannot correctly predict unmeasured coordinates.

#### Figures

![[adp3d-sparse-distance-reconstruction.png]]
*Figure 4 from [@levy2024]. The dashed experimental-resolution line is a reference, not a confidence interval or a general RMSD acceptance threshold.*

#### See also

- [[Protein backbone design diffusion models can be repurposed for fitting structures into electron density]]
- [[Diffusion guidance]]
- [[Computational models of proteins fit NMR data better than models designed using classical approaches]]
