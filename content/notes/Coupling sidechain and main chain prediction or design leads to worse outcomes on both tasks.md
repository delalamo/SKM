---
tags:
  - protein-design/misc
created: "2025-03-03T00:28:27"
modified: "2026-04-05T23:14:54"
---

#### Summary

**Coupling backbone and side chain prediction and/or design leads to worse results than a two-step approach** (Chu et al 2023[^chu2023], Vangaru & Bhattacharya 2025[^vangaru2025]). For protein backbone design, Chu et al 2023[^chu2023] found that co-designing side chains during diffusion led to unrealistic side chain geometries, and avoided it by running a final redesign/repack at the end of design. For protein side chain prediction, Vangaru & Bhattacharya 2025[^vangaru2025] found that AlphaFold3 performs worse that AlphaFold2 on sidechain prediction.

[^chu2023]: Chu et al. (2023) "An all-atom protein generative model." https://doi.org/10.1101/2023.05.24.542194
[^vangaru2025]: Vangaru & Bhattacharya (2025) "To pack or not to pack: revisiting protein side-chain packing in the post‐AlphaFold era." https://doi.org/10.1101/2025.02.22.639681
