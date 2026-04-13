---
title: Multiple sequence alignments
tags:
  - multiple-sequence-alignments
created: "2026-04-10T14:02:57"
modified: "2026-04-13T11:11:20"
---

**Multiple sequence alignments** (MSAs) are sets of sequences aligned either to a reference sequence or to each other. They are widely used in bioinformatics:
* Calculate summary statistics such as PSSMs and Potts models
* Infer protein properties, such as structure, via neural networks ([[MSA Transformer]], [[AlphaFold|AlphaFold2]]/[[RosettaFold]])
* Predict evolutionary relationships (e.g., [[Ancestral sequence reconstruction|ancestral sequence reconstruction]])

#### Notes

* **The inclusion of MSAs improves zero-shot prediction using [[Protein language models|PLMs]]** ([[10.1101__2023.10.01.560349|Su et al 2023]])
![[MSA-effect-on-variant-effect-prediction.png]]
	*Figure from [^su2023]*

<!-- generated -->

[^su2023]: Su et al. (2023) "SaProt: Protein Language Modeling with Structure-aware Vocabulary." https://doi.org/10.1101/2023.10.01.560349
