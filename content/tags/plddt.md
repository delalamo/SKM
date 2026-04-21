---
title: pLDDT
aliases:
  - pLDDT
created: "2026-04-10T14:02:57"
modified: "2026-04-20T10:13:23"
---

_(LDDT redirects here)_
**pLDDT** (predicted local distance difference test) is a [[Uncertainty quantification|confidence metric]] used by neural networks for [[tags/structure-prediction|protein structure prediction]]. It captures the per-residue accuracy, both in terms of neighborhood and side chain rotamer. It was first directly integrated into structure prediction by [[tags/alphafold2|AlphaFold2]] at the per-residue level and has been widely adopted since. AlphaFold3 adopted per-atom pLDDT.

![[Pasted-image-20240607140515.png]]
_Figure from [@terwilliger2023]_

#### Notes

- **When clustering predicted protein structures, sparse clusters tend to have lower pLDDT** [@nomburg2024]. This was found to be independent of [[Multiple sequence alignments|MSA]] depth.
- **[[tags/plddt|pLDDT]] correlates poorly with GDT-TS among [[tags/alphafold2|AlphaFold2]] models in [[CASP15]].** This was observed in a repeat that used deeper [[Multiple sequence alignments|MSAs]] [@lee2023b].
- **_De novo_ sequences designed by [[Inversion of protein folding neural networks|inversion]] with high [[tags/plddt|pLDDT]] were found by [[ESM]] to have high [[Sequence perplexity|perplexity]]** [@verkuil2022].
- **While the default pLDDT is not continuously differentiable and thus unsuitable for training, [@trinquier2025] use a modified version that can be used as a loss function.**
- **pLDDT can be used as spatial restraints in biomolecular simulations**:
  $$
  E_{pLDDT}=\sum{\left( \frac{d_{i}}{1.5*\exp{\left(4*\left(0.7 - pLDDT_{i} \right) \right)}}\right)^{2}}
  $$
  The equation was originally presented by Hiranuma et al. [@hiranuma2021] and was used by del Alamo et al. [@delalamo2022b] as coordinate constraints in Rosetta when refining [[tags/alphafold2|AlphaFold2]] models.
