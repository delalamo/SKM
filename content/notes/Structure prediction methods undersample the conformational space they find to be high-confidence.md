---
tags:
  - structure-prediction/sampling
  - conformational-dynamics/modeling
created: "2025-12-19T12:44:40"
modified: "2026-04-21T07:28:09"
---

#### Summary

**Protein [[structure-prediction|Structure prediction]] methods from both [[alphafold2|AlphaFold2]]- and [[diffusion-models|AF3]]-generation undersample the conformational space that they find to be high-confidence** [@roney2025]. In other words, they will favorably score physiologically relevant conformations when presented indirectly with the structure, but will fail to sample it by default unless hacked with custom alignments and/or templates (e.g., for conformational changes).
