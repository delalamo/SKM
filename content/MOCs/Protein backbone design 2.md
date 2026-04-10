---
title: Protein backbone design
tags:
  - protein-backbone-design
created: "2026-04-10T14:30:55"
modified: "2026-04-10T14:30:55"
---

**Protein backbone design** is the generation of protein backbones in three-dimensional space. This section also covers generation and design of entire protein structures in Cartesian space, but most methods uncouple design of the backbone and design of the sequence given the backbone ([[Inverse folding|inverse folding]]). As of May 2024, the current state of the art uses [[Diffusion models|diffusion]].

#### Methods

* **[[Chroma]]** ([[10.1038__s41586-023-06728-8|Ingraham et al 2023]])
* **RF-diffusion** ([[10.1038__s41586-023-06415-8|Watson et al 2023]]) and **RFam** ([[10.1101__2024.11.13.623507|Kim et al 2024]])
* [[Inversion of protein folding neural networks|Hallucination]] using [[AlphaFold|AlphaFold2]] and [[RosettaFold]]
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
