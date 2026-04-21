---
tags:
  - inverse-folding/evaluation
created: "2024-04-24T16:12:09"
modified: "2026-04-21T07:03:26"
summary: Running inverse folding in a random order leads to greater sequence recovery than running in a fixed-order
---
#### Summary
**Running [[tags/inverse-folding|Inverse folding]] in a random order outperforms fixed order** [@dauparas2022]. A related scheme is order-agnostic autoregressive diffusion, used by a sequence diffusion model, in which the identities of individual residues are determined one at a time. The forward noising process masks one residue at a time, in effect. This was shown by [@alamdari2023] to outperform whole-sequence simultaneous diffusion. Applying this scheme on diffusion models for [[Multiple sequence alignments]] outperforms [[MSA Transformer]].
