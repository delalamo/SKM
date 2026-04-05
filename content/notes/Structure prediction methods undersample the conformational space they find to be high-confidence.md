---
tags:
  - protein-folding/misc
---

#### Summary

**Protein [[Structure prediction]] methods from both [[AlphaFold|AF2]]- and [[Diffusion models|AF3]]-generation undersample the conformational space that they find to be high-confidence** (Roney et al 2025[^roney2025]). In other words, they will favorably score physiologically relevant conformations when presented indirectly with the structure, but will fail to sample it by default unless hacked with custom alignments and/or templates (e.g., for conformational changes).

[^roney2025]: Roney et al. (2025) "Protein Diffusion Models as Statistical Potentials." https://doi.org/10.64898/2025.12.09.693073
