---
tags:
  - protein-structure-prediction/limitations
  - protein-backbone-design
  - citation-fix
created: "2025-03-03T00:28:27"
modified: "2026-04-20T10:13:23"
---

#### Summary
**Coupling backbone and side chain prediction or design does not necessarily lead to better performance** [^chu2023][^vangaru2025][^didi2026]. Methods from early 2026 found strong performance in binder design when combining [[Protein backbone design|backbone design]] and [[Inverse Folding|inverse folding]], and degraded performance when backbones were redesigned with [[ProteinMPNN]] afterwards. However, prior work found the opposite conclusion in protein backbone design [^chu2023][^vangaru2025]. In parricular, [[Alphafold3]] was found to be worse than [[Alphafold2]] at sidechain packing[^vangaru2025].

[^chu2023]: Chu et al. (2023) "An all-atom protein generative model." https://doi.org/10.1101/2023.05.24.542194
[^vangaru2025]: Vangaru & Bhattacharya (2025) "To pack or not to pack: revisiting protein side-chain packing in the post‐AlphaFold era." https://doi.org/10.1101/2025.02.22.639681
[^didi2026]: Didi et al. (2026) "Proteina-Complexa: Scaling Atomistic Protein Binder Design with Generative Pretraining and Test-Time Compute." https://doi.org/10.48550/arXiv.2603.27950