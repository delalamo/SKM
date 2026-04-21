---
title: Structure prediction
aliases:
  - Structure prediction
created: "2026-04-10T14:02:57"
modified: "2026-04-20T07:16:03"
---

**Structure prediction** refers to the problem of predicting the 3D shape of a protein or nucleotide sequence without any experimental information. Common metrics used for evaluating the quality of predicted structures include [[LDDT]] (residue-level, [[tags/tm-score|TM-score]] (whole-structure level), and [[DockQ]] (complex level).

## Methods

#### [[Multiple sequence alignments|MSA]]-based

- **[[tags/alphafold2|AlphaFold2]]**: currently viewed as the highest-accuracy method
- **[[tags/rosettafold|RosettaFold]]**
- **Diffold**: A fine-tuned version of AlphaFold2

#### [[tags/protein-language-models|PLM]]-based

- **[[ESMFold]]**: currently the most widely-used method, albeit probably not the most accurate model in this category
- **[[OmegaFold]]**
- **xTrimoPGLM**

#### Others

- **EquiFold**: a method that needs to be fine-tuned on specific families of proteins
- **EigenFold**: a method that uses diffusion to model the dynamics of proteins, albeit unsuccessfully

#### For [[tags/antibodies|antibodies]]

_See [[tags/antibody-structure-prediction|Antibody structure prediction]]_

## Notes

#### Training

![[Pasted-image-20231211070606.png]]
_Figure from [@ahdritz2024]_

#### Sidechain prediction

- **Formulating the sidechain prediction problem as a classification problem by binning chi angles, rather than a regression problem, let to improved performance** [@randolph2024].
- **Sidechain prediction methods not sensitive to B-factor cutoffs.** The outcome of sidechain prediction model PIPPack was not strongly affected by B-factor values of protein structures in the training set [@randolph2024].
