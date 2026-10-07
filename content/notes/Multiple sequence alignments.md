---
title: Multiple sequence alignments
created: 2026-04-10T14:02:57
modified: "2026-10-07T08:57:03"
tags:
  - evolution/homology
---

**Multiple sequence alignments** (MSAs) are sets of sequences aligned either to a reference sequence or to each other. They are widely used in bioinformatics:
* Calculate summary statistics such as PSSMs and Potts models
* Infer protein properties, such as structure, via neural networks ([[MSA Transformer]], [[notes/AlphaFold2|AlphaFold2]]/[[notes/RoseTTAFold|RosettaFold]])
* Predict evolutionary relationships (e.g., [[notes/Ancestral sequence reconstruction|ancestral sequence reconstruction]])

#### Notes

* **The inclusion of MSAs improves zero-shot prediction using [[notes/Protein language models|PLMs]]** [@su2023]
![[MSA-effect-on-variant-effect-prediction.png]]
	*Ref [@su2023]*

#### See also

- [[PLM embeddings contain enough information to align proteins without fine-tuning]]
