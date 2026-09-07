---
tags:
  - prediction/confidence
  - prediction/stability-expression
title: Raw folding-model confidence is not a general protein stability predictor
created: "2026-03-06T09:43:56"
modified: "2026-08-19T16:32:04"
---

## Summary

**Raw confidence from protein folding neural networks is not a general predictor of [[notes/Stability and thermostability|protein stability]].** Mutation-induced ddG values show little or no correlation with changes in [[notes/pLDDT|pLDDT]] [@pak2023alphafold], and high-pLDDT designs can still unfold during Hamiltonian [[Replica-exchange molecular dynamics]] [@aina2023]. The networks nonetheless contain some stability-related signal: [[notes/AlphaFold2|AlphaFold2]] pLDDT correlates with stability within restricted fold families [@ferrari2025], and [[ESMFold]] pLDDT moderately discriminates experimentally successful from unsuccessful monomer designs [@garcia2025]. Dedicated downstream models can also predict ddG from AlphaFold structures about as accurately as from experimental structures [@diaz2023]. RMSD itself does not correlate with stability, although [@mcbride2023] showed that a custom strain score was able to predict this with some success.

## Figures

![[Pasted-image-20240624104718.png]]
*Ref [@pak2023alphafold]*

## See also

* [[High-pLDDT designs can be insoluble]]
* [[Protein structure prediction and design confidence metrics do not correlate with binding affinity]]
* [[ESMFold pLDDT weakly correlates with intra-family differences in stability and experimental success, but not differences in cooperativity]]
