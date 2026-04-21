---
title: Multiple sequence alignments
created: 2026-04-10T14:02:57
modified: "2026-04-21T07:03:26"
---

**Multiple sequence alignments** (MSAs) are sets of sequences aligned either to a reference sequence or to each other. They are widely used in bioinformatics:
* Calculate summary statistics such as PSSMs and Potts models
* Infer protein properties, such as structure, via neural networks ([[MSA Transformer]], [[tags/alphafold2|AlphaFold2]]/[[tags/rosettafold|RosettaFold]])
* Predict evolutionary relationships (e.g., [[tags/ancestral-sequence-reconstruction|ancestral sequence reconstruction]])

#### Notes

* **The inclusion of MSAs improves zero-shot prediction using [[tags/protein-language-models|PLMs]]** [@su2023]
![[MSA-effect-on-variant-effect-prediction.png]]
	*Ref [@su2023]*
