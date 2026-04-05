---
title: pLDDT
tags:
  - plddt
---

*(LDDT redirects here)*
**pLDDT** (predicted local distance difference test) is a [[Uncertainty quantification|confidence metric]] used by neural networks for [[Structure prediction|protein structure prediction]]. It captures the per-residue accuracy, both in terms of neighborhood and side chain rotamer. It was first directly integrated into structure prediction by [[AlphaFold|AlphaFold2]] at the per-residue level and has been widely adopted since. AlphaFold3 adopted per-atom pLDDT.

![](/assets/Pasted-image-20240607140515.png)
*Figure from [[10.1038__s41592-023-02087-4|Terwilliger et al 2023]]*

#### Notes

* **When clustering predicted protein structures, sparse clusters tend to have lower pLDDT** ([[10.1038__s41586-024-07809-y|Nomburg et al 2024]]). This was found to be independent of [[Multiple sequence alignments|MSA]] depth.
* **[[pLDDT]] correlates poorly with GDT-TS among [[AlphaFold|AlphaFold2]] models in [[CASP15]].** This was observed in a repeat that used deeper [[Multiple sequence alignments|MSAs]] ([[10.1101__2023.07.10.548308|Lee et al 2023b]]). 
* ***De novo* sequences designed by [[Inversion of protein folding neural networks|inversion]] with high [[pLDDT]] were found by [[ESM]] to have high [[Sequence perplexity|perplexity]]** ([[10.1101__2022.12.21.521521|Verkuil et al 2022]]).
* **While the default pLDDT is not continuously differentiable and thus unsuitable for training, [[10.1101__2025.05.09.653096|Trinquier et al 2025]] use a modified version that can be used as a loss function.**
* **pLDDT can be used as spatial restraints in biomolecular simulations**:
$$E_{pLDDT}=\sum{\left( \frac{d_{i}}{1.5*\exp{\left(4*\left(0.7 - pLDDT_{i} \right) \right)}}\right)^{2}} $$
	The equation was originally presented by [[10.1038__s41467-021-21511-x|Hiranuma et al 2021]] and was used by [[10.1073__pnas.2206129119|del Alamo et al 2022]] as coordinate constraints in Rosetta when refining [[AlphaFold|AlphaFold2]] models.

<!-- generated -->
