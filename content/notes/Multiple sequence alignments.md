---
title: Multiple sequence alignments
created: 2026-04-10T14:02:57
modified: "2026-04-20T08:32:20"
---

**Multiple sequence alignments** (MSAs) are sets of sequences aligned either to a reference sequence or to each other. They are widely used in bioinformatics:
* Calculate summary statistics such as PSSMs and Potts models
* Infer protein properties, such as structure, via neural networks ([[MSA Transformer]], [[AlphaFold2]]/[[RosettaFold]])
* Predict evolutionary relationships (e.g., [[Ancestral sequence reconstruction|ancestral sequence reconstruction]])

#### Notes

* **The inclusion of MSAs improves zero-shot prediction using [[Protein language models|PLMs]]** [@su2023]
![[MSA-effect-on-variant-effect-prediction.png]]
	*Ref [@su2023]*
