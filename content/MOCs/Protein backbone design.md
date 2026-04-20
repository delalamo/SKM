---
title: Protein backbone design
tags:
  - protein-backbone-design
created: "2026-04-10T14:30:55"
modified: "2026-04-20T07:16:03"
---

**Protein backbone design** is the generation of protein backbones in three-dimensional space. This section also covers generation and design of entire protein structures in Cartesian space, but most methods uncouple design of the backbone and design of the sequence given the backbone ([[Inverse folding|inverse folding]]). As of May 2024, the current state of the art uses [[Diffusion models|diffusion]].

#### Methods

* **[[Chroma]]** ([[10.1038__s41586-023-06728-8|Ingraham et al 2023]])
* **RF-diffusion** ([[10.1038__s41586-023-06415-8|Watson et al 2023]]) and **RFam** ([[10.1038__s41586-025-09746-w|Kim et al 2026]])
* [[Inversion of protein folding neural networks|Hallucination]] using [[AlphaFold2]] and [[RosettaFold]]
* Inpainting using [[RosettaFold]] ([[10.1126__science.abn2100|Wang et al 2022]])

#### Datasets

* [[10.1101__2022.12.21.521521|Verkuil et al 2022]] use a test set of 39 PDBs for their validation, although they cite someone else:
	* 1QYS
	* 2KL8
	* 2KPO
	* 2LN3
	* 2LTA
	* 2LVB
	* 2N2T
	* 2N2U
	* 2N3Z
	* 2N76
	* 4KY3
	* 4KYZ
	* 5CW9
	* 5KPE
	* 5KPH
	* 5L33
	* 5TPJ
	* 5TRV
	* 6CZG
	* 6CZH
	* 6CZI
	* 6CZJ
	* 6D0T
	* 6DG6
	* 6DKM A
	* 6DKM B
	* 6DLM A
	* 6DLM B
	* 6E5C
	* 6LLQ
	* 6MRR
	* 6MRS
	* 6MSP
	* 6NUK
	* 6W3F
	* 6W3W
	* 6WI5
	* 6WVS
	* 7MCD

<!-- generated -->

## Designability

- [[Adding noise while training non-Ab inverse folding models improves self-consistency while worsening sequence recovery]]
- [[Affinity maturation of de novo minibinders introduces mutations far from the active site]]
- [[AlphaFold2 outperforms ESMFold at distinguishing designable and undesignable protein backbones]]
- [[Buried nonpolar surface area is a major determinant of whether de novo designed proteins are stable]]
- [[Computational models are less designable than experimental structures]]
- [[De novo designed backbones can increase the size of proteins for cryo-EM structure determination]]
- [[De novo designed proteins with alpha helices are easier to predict than those with other secondary structures]]
- [[De novo structure prediction with ligands outperforms apo de novo structure prediction alone]]
- [[Inverse folding methods outperform sequence design by hallucination]]
- [[Inverse folding models can distinguish between and design backbones belonging to transmembrane and soluble beta-barrels]]
- [[Low-pLDDT hallucinated models from AF3-generation protein structure predictors are designable]]
- [[Most possible alpha-beta topologies unexplored by nature]]
- [[Natural sequences have higher pTM but lower pLDDT than de novo sequences]]
- [[Nearly half of CATH domains do not pass designability filters used to evaluate protein backbone design performance]]
- [[Protein language models and PLM-based structure prediction generalize to de novo designed proteins]]
- [[Protein structure prediction methods predict idealized secondary structures in de novo proteins]]
- [[ProteinMPNN-derived inverse folding methods underdesign aromatic residues]]
- [[Sequence-based variant effect prediction methods generalize to de novo proteins]]
- [[Sheets are less designable than helices]]
- [[The structures of shorter de novo designed sequences are easier to predict than those of longer proteins]]

## General

- [[Coupling sidechain and main chain prediction or design does not always lead to improvements]]
- [[Multimodal sequence-structure guidance outperforms unimodal guidance in cases where both need to be designed]]
