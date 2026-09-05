---
title: MSA Transformer
created: 2026-04-10T14:02:57
modified: "2026-07-28T14:12:17"
tags:
  - training/pretraining-and-scaling
  - model-design/architectures
---

**MSA-transformer** is a [[notes/protein-language-models|protein language model]] that operates on [[Multiple sequence alignments|multiple sequence alignments]]. It was used as the basis to train [[ESM]]-1v. It was developed in parallel with the [[Evoformer]] and has many features in common. It is the basis for [[ProteinNPT]].

![[Pasted-image-20231107233109.png]]
*Ref [@rao2021]*

#### Notes

* **The column-wise [[Transformer|attention matrices]] of MSA Transformer recapitulate protein phylogenies, and this was concentrated in early layers of the NN** [@lupo2022].
* **MSA transformer outperforms [[notes/protein-language-models|PLMs]] and [[notes/inverse-folding|Inverse folding]] models on [[notes/thermostability|stability prediction]] when fine-tuned on the Tsuboyama et al. [@tsuboyama2023] dataset** [@cuturello2024]. This includes [[Hybrid sequence-structure models|hybrid sequence-structure methods]] like ProstT5.
* [[MSA protein language models can identify intermolecular contacts|MSA Transformer can extract intermolecular contacts from correctly paired, but not incorrectly paired, MSAs]] [@lupo2024].
![[Pasted-image-20240626072420.png]]
	*Ref [@lupo2024]*
