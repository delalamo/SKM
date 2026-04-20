---
title: ProteinNPT
tags:
created: 2026-04-10T14:02:57
modified: "2026-04-20T08:16:13"
---

**ProteinNPT** is a module that can be appended to [[Multiple sequence alignments|MSA]]-based [[Protein language models|protein language models]] that was first introduced by [[10.1101__2023.12.06.570473|Notin et al 2023b]].
![[Pasted-image-20240126170230.png]]
*Figure 1 from [[10.1101__2023.12.06.570473|Notin et al 2023b]]*

## Notes:

* The method consists of five layers appended to, in the case of the paper, [[MSA Transformer]], which is frozen throughout training. They compare against one-hot encoded representations
* Relevant data to predict is appended as columns. Additional columns that are not relevant for prediction but nonetheless correlate with the property of interest are also added ("Auxiliary labels")
* The method is re-trained for every MSA/target/set of data using 15% masking as with [[ESM]]. At the start of training, the loss is mostly focused on recovering the masked amino acids, but as training proceeds the loss shifts toward recovering the labels
* As with MSA-Transformer, it uses tied row attention to reduce memory footprint under the assumption that the fold is conserved among aligned sequences
* ProteinNPT with [[Tranception]] embeddings had the best performance on prediction of catalytic efficiency ($K_M$):
![[Pasted-Graphic-10.png]]
	*Ref [^muir2024]*

<!-- generated -->

[^muir2024]: Muir et al. (2025) "Evolutionary-scale enzymology enables exploration of a rugged catalytic landscape." Science. https://doi.org/10.1126/science.adu1058
