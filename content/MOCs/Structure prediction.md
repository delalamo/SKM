---
title: Structure prediction
tags:
  - structure-prediction
created: "2026-04-10T14:02:57"
modified: "2026-04-10T15:51:38"
---

**Structure prediction** refers to the problem of predicting the 3D shape of a protein or nucleotide sequence without any experimental information. Common metrics used for evaluating the quality of predicted structures include [[LDDT]] (residue-level, [[TM-score]] (whole-structure level), and [[DockQ]] (complex level).

## Methods
#### [[Multiple sequence alignments|MSA]]-based

* **[[AlphaFold]]**: currently viewed as the highest-accuracy method
* **[[RosettaFold]]**
* **Diffold**: A fine-tuned version of AlphaFold2

#### [[Protein language models|PLM]]-based

* **[[ESMFold]]**: currently the most widely-used method, albeit probably not the most accurate model in this category
* **[[OmegaFold]]**
* **xTrimoPGLM**

#### Others

* **EquiFold**: a method that needs to be fine-tuned on specific families of proteins
* **EigenFold**: a method that uses diffusion to model the dynamics of proteins, albeit unsuccessfully

#### For [[Antibodies|antibodies]]

*See [[Antibody structure prediction]]*

## Notes
#### Conformational sampling methods

*From [[AlphaFold#Conformational modeling]]*
*Others*

#### Training

	\![[Pasted-image-20231211070606.png]]
	*Figure from [[10.1101__2022.11.20.517210|Ahdritz et al 2024]]*

#### Sidechain prediction

* **Formulating the sidechain prediction problem as a classification problem by binning chi angles, rather than a regression problem, let to improved performance** ([[10.1101__2023.08.03.551328|Randolph and Kuhlman 2023]]).
* **Sidechain prediction methods not sensitive to B-factor cutoffs.** The outcome of sidechain prediction model PIPPack was not strongly affected by B-factor values of protein structures in the training set ([[10.1101__2023.08.03.551328|Randolph and Kuhlman 2023]]).

<!-- generated -->

## Miscellaneous

- [[Scrambled MSAs outperform single-sequence-prediction with AlphaFold]]
- [[Structure prediction with AlphaFold improved when starting from an initial guess, rather than default initialization]]
