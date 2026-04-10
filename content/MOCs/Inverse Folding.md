---
title: Inverse folding
tags:
  - inverse-folding
created: "2026-04-10T14:02:57"
modified: "2026-04-10T14:30:55"
---

**Inverse folding** describes the problem of designing a sequence for a structure. Typically these are limited to the twenty canonical amino acids.

## Methods

*See [[Hybrid sequence-structure models]] for a list of methods that incorporate [[Protein language models|PLMs]]*
* **[[ProteinMPNN]]** and its derivatives
* **[[ESM-IF]]**
* **GearNet**
* **Frame2seq**
* **[[Geometric Vector Perceptrons|GVP-GNN]]**

## Notes
#### Training

* **Training inverse folding models with backbone dihedral angles as features usually improved sequence recovery** ([[sTYuRVrdK3|Jamasb et al 2023]]).
	\![[Pasted-image-20240117115655.png]]
	*Figure from [[sTYuRVrdK3|Jamasb et al 2023]]*

#### Execution

* **Forward-folding is a stronger predictor of inverse folding success than sequence recovery** ([[10.48550__arXiv.2312.02447|Yang et al 2023b]], citing [[10.1038__s41586-023-06415-8|Watson et al 2023]] and [[10.1126__science.add2187|Dauparas et al 2022]]).

#### Datasets

* **PDBench** is a dataset of 595 protein structures with diverse, evenly divided topologies for benchmarking of [[Inverse folding]] methods ([[10.1093__bioinformatics__btad027|Castorina et al 2023]]).
	\![[Alpha-Beta-Barre.png]]
	*Figure 2 from [[10.1093__bioinformatics__btad027|Castorina et al 2023]]*

<!-- generated -->

## Training

- [[Ab-Ag inverse folding methods benefit from pretraining]]
- [[Adding noise while training non-Ab inverse folding models improves self-consistency while worsening sequence recovery]]

## Antibodies

- [[Ab finetuning improves naturalness of inverse folding designs]]

## Miscellaneous

- [[Inverse folding NNs are better predictors of equilibrium dynamics than protein folding NNs]]
