---
title: Antibody structure prediction
tags:
  - antibody-structure-prediction
created: "2026-04-10T14:30:55"
modified: "2026-04-11T06:06:39"
---

The **[[Antibodies|antibody]] [[Structure prediction|structure prediction]]** problem is a subclass of the protein structure prediction problem that is mostly focused on predicting the [[Complementarity-determining regions|CDRs]], specifically the [[Complementarity-determining regions#CDRH3|CDRH3]] loop that mediates antigen binding. It also sometimes includes the antibody-antigen docking problem.

#### Models

* **AbFold**: a method that concatenates information from [[IgFold]] and [[AlphaFold|AlphaFold2]] Multimer when modeling antibodies, which usually predict different conformations, leading to [[Antibody structure prediction improved with AlphaFold2 features|improved prediction quality]] ([[10.1101__2023.04.20.537598|Peng et al 2023]])
* **[[IgFold]]**: a method that uses embeddings from the [[Antibody language models|antibody LM]] AntiBERTy
* **[[ImmuneBuilder]]**: Consists of ABodyBuilder2 (for [[Antibodies]]), NanoBodyBuilder2 (for [[Nanobodies]]), and TCRBuilder2 (for [[T-cell receptors]]).

#### Structure prediction observations

*See also [[Antibody-antigen interactions]]*

<!-- generated -->

## CDR

- [[AlphaFold2 recapitulates interaction biases from PDB when modeling antibodies]]
- [[Antibody structure prediction improved with AlphaFold2 features]]
- [[CDR representations segregate into distinct clusters]]
- [[CDRH3 conformation is affected by interdomain orientation]]
- [[CDRH3 flanking residues more conserved and easier to predict than those in the center]]
- [[DL structure prediction methods cannot predict CDR conformations unseen during training]]
- [[Deep learning methods produce different CDRH3 conformers]]
- [[Different CDRL3 lengths are found in functional and dysfunctional antibodies]]
- [[Inclusion of adjacent loops can improve CDRH3 structural modeling]]
- [[Inverse folding models trained on all proteins outperform those trained on Abs for CDR prediction]]
- [[Kappa subtype restricts CDRH3 dynamics]]
- [[Kinks in nanobody CDR3 loops are correctly predicted by structure prediction methods]]
- [[LM-based antibody structure prediction methods work equally well with generic and Ab PLMs]]
- [[Length independent clustering improves CDR prediction]]
- [[Loops from one V-region chain affect the conformations and dynamics of loops in the other chain]]
- [[Nanobody CDRH3 loops are longer but more compact]]
- [[Optimal scaling of antibody LMs improves prediction of masked CDRH3 residues but not framework residues]]
- [[Psi torsion angles are effective metadynamic CVs for CDRH3 and CDRL3]]
- [[QM-MM and unbiased MD are insufficient to correctly determine CDRH3 conformation]]
- [[Sequence clusters and structural clusters of CDRH3 do not overlap]]
- [[Template CDR retrieval using embeddings]]
- [[pLDDT is inversely correlated with CDRH3 length]]

## Complex Prediction

- [[Ab-Ag inverse folding methods benefit from pretraining]]
- [[AlphaFold3 ipTM can distinguish between antibody binders and nonbinders]]
- [[Antibody-antigen binding modes are not necessarily defined by induced fit]]
- [[Antibody-antigen modeling by diffusion-based structure prediction is data-limited]]
- [[Antigen context improves CDRH3 structure prediction]]
- [[Correct CDRH3 prediction is necessary but insufficient for correct Ab-Ag docking]]
- [[Correct antibody-antigen prediction in AF3 and related models is partially determined by training set similarity]]
- [[Dropout improves AF2 multimer prediction, including for antibody-antigen complexes]]
- [[Increasing diffusion samples is sufficient to yield correctly predicted antibody-antigen complexes]]
- [[Inverse folding models can predict antibody-antigen binding affinities with higher accuracy by correcting with predictions from unbound state]]
- [[PAE weakly correlates with Ab-Ag binding]]
- [[Partial diffusion of de novo designed binders and VHHs improves refoldability and designability scores]]
- [[Structure-based methods outperform sequence-based methods on antigen-dependent antibody design]]
- [[The structures of nanobodies with kinked CDR3 loops are more difficult to predict in complex with their antigen]]
