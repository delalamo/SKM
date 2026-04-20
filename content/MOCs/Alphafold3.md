---
title: Alphafold3
created: "2026-04-11T06:06:39"
modified: "2026-04-20T10:13:23"
---
**AlphaFold3** is a [[Diffusion models|diffusion]]-based all-atom [[Structure prediction|structure prediction]] method that is widely seen as state-of-the-art. 

![[Pasted-Graphic-4.png]]
*Architecture of AlphaFold3 from [[10.1038__s41586-024-07487-w|Abramson et al 2024]]*

#### Architectural and ML contributions
* PairFormer
* PDE: predicted distance error (replacing frame aligned point error)
* Non-equivariant per-atom prediction, which leads to [[DL structure tools introduce chiral errors such as swapped chiral centers, D-amino acids, and cis-amide bonds|occasional errors when predicting chirality]]
* [[Distillation|Cross-distillation]] from [[AlphaFold2]]-Multimer v2.3 to avoid hallucination of low-[[pLDDT]] regions

<!-- generated -->

## General

- [[AF3 binding affinity predictions are orthogonal to those made by force fields and other neural networks]]
- [[AF3-generation methods can be substantially shrunk without sacrificing prediction quality, except on PPIs]]
- [[AF3-generation methods incorporate MSA information exclusively into the pair representation]]
- [[AlphaFold3 ipTM can distinguish between antibody binders and nonbinders]]
- [[AlphaFold3 learns intramolecular interactions faster than intermolecular interactions]]
- [[AlphaFold3 performs comparably to AlphaFold2 when predicting multiple conformations of fold-switching proteins]]
- [[AlphaFold3 universally predicts the active state of ligand-bound GPCRs, even when the ligand is an antagonist]]
- [[AlphaFold3 uses cross-distillation from AlphaFold2 to avoid hallucinating secondary structure in low-pLDDT regions]]
- [[Antibody-antigen modeling by diffusion-based structure prediction is data-limited]]
- [[Conformational sampling by AlphaFold3-generation methods can be achieved by scaling the pair representation]]
- [[Correct antibody-antigen prediction in AF3 and related models is partially determined by training set similarity]]
- [[Diffusion outperforms hallucination when using AF3-generation protein structure prediction methods]]
- [[Flow matching and diffusion perform comparably for biomolecular structure prediction]]
- [[Low-pLDDT hallucinated models from AF3-generation protein structure predictors are designable]]
- [[Protein-ligand co-folding methods do not generalize beyond their training set]]
- [[The Boltz-2 affinity module cannot be effectively repurposed for PPI affinity prediction]]
- [[The confidence metrics of AlphaFold2 are better calibrated than those of AlphaFold3]]
