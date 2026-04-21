---
title: ProteinNPT
created: 2026-04-10T14:02:57
modified: "2026-04-21T07:03:26"
---

**ProteinNPT** is a module that can be appended to [[Multiple sequence alignments|MSA]]-based [[tags/protein-language-models|protein language models]] that was first introduced by [@notin2023b].
![[Pasted-image-20240126170230.png]]
*Figure 1 from Notin et al. [@notin2023b]*

## Notes:

* The method consists of five layers appended to, in the case of the paper, [[MSA Transformer]], which is frozen throughout training. They compare against one-hot encoded representations
* Relevant data to predict is appended as columns. Additional columns that are not relevant for prediction but nonetheless correlate with the property of interest are also added ("Auxiliary labels")
* The method is re-trained for every MSA/target/set of data using 15% masking as with [[ESM]]. At the start of training, the loss is mostly focused on recovering the masked amino acids, but as training proceeds the loss shifts toward recovering the labels
* As with MSA-Transformer, it uses tied row attention to reduce memory footprint under the assumption that the fold is conserved among aligned sequences
* ProteinNPT with [[Tranception]] embeddings had the best performance on prediction of catalytic efficiency ($K_M$):
![[Pasted-Graphic-10.png]]
	*Ref [@muir2024]*
