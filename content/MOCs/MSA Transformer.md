---
title: MSA Transformer
tags:
  - msa-transformer
created: "2026-04-10T14:02:57"
modified: "2026-04-13T11:11:20"
---

**MSA-transformer** is a [[Protein language models|protein language model]] that operates on [[Multiple sequence alignments|multiple sequence alignments]]. It was used as the basis to train [[ESM]]-1v. It was developed in parallel with the [[Evoformer]] and has many features in common. It is the basis for [[ProteinNPT]].

![[Pasted-image-20231107233109.png]]
*Figure from [^rao2021]*

#### Notes

* **The column-wise [[Transformer|attention matrices]] of MSA Transformer recapitulate protein phylogenies, and this was concentrated in early layers of the NN** ([[10.1038__s41467-022-34032-y|Lupo et al 2022]]).
* **MSA transformer outperforms [[Protein language models|PLMs]] and [[Inverse folding]] models on [[Stability and thermostability|stability prediction]] when fine-tuned on the [[10.1038__s41586-023-06328-6|Tsuboyama et al 2023]] dataset** ([[10.1101__2024.04.11.589002|Cuturello et al 2024]]). This includes [[Hybrid sequence-structure models|hybrid sequence-structure methods]] like ProstT5.
* **MSA-transformer can extract intermolecular contacts from correctly paired MSAs, but not incorrectly paired MSAs** ([[10.1073__pnas.2311887121|Lupo et al 2024]]).
![[Pasted-image-20240626072420.png]]
	*Figure from [^lupo2024]*

<!-- generated -->

[^lupo2024]: Lupo et al. (2024) "Pairing interacting protein sequences using masked language modeling." *Proceedings of the National Academy of Sciences*. https://doi.org/10.1073/pnas.2311887121
[^rao2021]: Rao et al. (2021) "MSA Transformer." https://doi.org/10.1101/2021.02.12.430858
