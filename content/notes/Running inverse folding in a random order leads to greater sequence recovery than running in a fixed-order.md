---
tags:
  - inverse-folding/evaluation
created: "2024-04-24T16:12:09"
modified: "2026-04-11T06:06:39"
---

---
summary: Running inverse folding in a random order leads to greater sequence recovery than running in a fixed-order
tags: inverse-folding/training, inverse-folding/execution
---
#### Summary
**Running [[Inverse folding]] in a random order outperforms fixed order** [^dauparas2022]. A related scheme is order-agnostic autoregressive diffusion, used by a sequence diffusion model, in which the identities of individual residues are determined one at a time. The forward noising process masks one residue at a time, in effect. This was shown by [^alamdari2023] to outperform whole-sequence simultaneous diffusion. Applying this scheme on diffusion models for [[Multiple sequence alignments]] outperforms [[MSA Transformer]].

[^dauparas2022]: Dauparas et al. (2022) "Robust deep learning–based protein sequence design using ProteinMPNN." *Science*. https://doi.org/10.1126/science.add2187
[^alamdari2023]: Alamdari et al. (2023) "Protein generation with evolutionary diffusion: sequence is all you need." https://doi.org/10.1101/2023.09.11.556673
