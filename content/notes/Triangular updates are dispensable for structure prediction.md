---
tags:
  - structure-prediction/architecture
created: "2025-11-07T17:49:25"
modified: "2026-04-21T07:28:09"
---

#### Summary

**The [[Triangular update]] from AlphaFold2 is dispensable for high-accuracy [[structure-prediction|Structure prediction]]** [@baek2023; @ouyangzhang2025]. This module from [[alphafold2|AlphaFold2]]/[[alphafold3|3]] has a memory footprint that scales cubically with respect to the size of the protein. [[rosettafold|RosettaFold]] circumvented the need for this by instead passing the 3D structure alongside distogram/[[Multiple sequence alignments]] processing, and looking at pairwise residue distances (which scales quadratically). More recently, PairMixer dispensed entirely with the module without any loss of accuracy.

#### Figures

![[Pasted-image-20251107172115.png]]

*Ref [@ouyangzhang2025]*
