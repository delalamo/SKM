---
tags:
  - protein-folding/misc
created: "2025-11-07T17:49:25"
modified: "2026-04-05T23:36:09"
---

#### Summary

**The [[Triangular update]] from AlphaFold2 is dispensable for high-accuracy [[Structure prediction]]** [^baek2023][^ouyangzhang2025]. This module from [[AlphaFold]]2/3 has a memory footprint that scales cubically with respect to the size of the protein. [[RosettaFold]] circumvented the need for this by instead passing the 3D structure alongside distogram/[[Multiple sequence alignments]] processing, and looking at pairwise residue distances (which scales quadratically). More recently, PairMixer dispensed entirely with the module without any loss of accuracy.

#### Figures

![](/assets/Pasted-image-20251107172115.png)

*Figure from [^ouyangzhang2025]*

[^baek2023]: Baek et al. (2023) "Efficient and accurate prediction of protein structure using RoseTTAFold2." https://doi.org/10.1101/2023.05.24.542179
[^ouyangzhang2025]: Ouyang-Zhang et al. (2025) "Triangle Multiplication Is All You Need For Biomolecular Structure Representations." https://doi.org/10.48550/ARXIV.2510.18870
