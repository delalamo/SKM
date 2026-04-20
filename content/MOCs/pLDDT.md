---
title: pLDDT
tags:
  - plddt
  - structure-prediction/metrics
created: "2026-04-10T14:02:57"
modified: "2026-04-20T08:16:13"
---

*(LDDT redirects here)*
**pLDDT** (predicted local distance difference test) is a [[Uncertainty quantification|confidence metric]] used by neural networks for [[Structure prediction|protein structure prediction]]. It captures the per-residue accuracy, both in terms of neighborhood and side chain rotamer. It was first directly integrated into structure prediction by [[AlphaFold2]] at the per-residue level and has been widely adopted since. AlphaFold3 adopted per-atom pLDDT.

![[Pasted-image-20240607140515.png]]
*Ref [^terwilliger2023]*

#### Notes

* **When clustering predicted protein structures, sparse clusters tend to have lower pLDDT** ([[10.1038__s41586-024-07809-y|Nomburg et al 2024]]). This was found to be independent of [[Multiple sequence alignments|MSA]] depth.
* **[[pLDDT]] correlates poorly with GDT-TS among [[AlphaFold2]] models in [[CASP15]].** This was observed in a repeat that used deeper [[Multiple sequence alignments|MSAs]] ([[10.1101__2023.07.10.548308|Lee et al 2023b]]). 
* ***De novo* sequences designed by [[Inversion of protein folding neural networks|inversion]] with high [[pLDDT]] were found by [[ESM]] to have high [[Sequence perplexity|perplexity]]** ([[10.1101__2022.12.21.521521|Verkuil et al 2022]]).
* **While the default pLDDT is not continuously differentiable and thus unsuitable for training, [[10.1101__2025.05.09.653096|Trinquier et al 2025]] use a modified version that can be used as a loss function.**
* **pLDDT can be used as spatial restraints in biomolecular simulations**:
$$E_{pLDDT}=\sum{\left( \frac{d_{i}}{1.5*\exp{\left(4*\left(0.7 - pLDDT_{i} \right) \right)}}\right)^{2}} $$
	The equation was originally presented by [[10.1038__s41467-021-21511-x|Hiranuma et al 2021]] and was used by [[10.1073__pnas.2206129119|del Alamo et al 2022]] as coordinate constraints in Rosetta when refining [[AlphaFold2]] models.

<!-- generated -->

## General

- [[AlphaFold3 uses cross-distillation from AlphaFold2 to avoid hallucinating secondary structure in low-pLDDT regions]]
- [[Antibody-antigen modeling by diffusion-based structure prediction is data-limited]]
- [[Confidence metrics for diffusion-based structure prediction methods can be improved with minimal changes to conditioning representations]]
- [[Confidence metrics from structure prediction correlate with accuracy even in the absence of coevolutionary data]]
- [[DiffDock confidence is inversely correlated with RMSD]]
- [[Fine-tuning AlphaFold for MHC prediction by adding Evoformer layers improves RMSD and pLDDT]]
- [[Fine-tuning base models on test cases can improve the performance of variant effect and structure prediction]]
- [[Flow matching and diffusion perform comparably for biomolecular structure prediction]]
- [[High-pLDDT designs can be insoluble]]
- [[Including structure prediction confidence while training inverse folding improves sequence diversity but not sequence recovery]]
- [[Inverse folding methods outperform sequence design by hallucination]]
- [[LM-based antibody structure prediction methods work equally well with generic and Ab PLMs]]
- [[Low-pLDDT hallucinated models from AF3-generation protein structure predictors are designable]]
- [[Most ML quality metrics cannot effectively predict enzyme activity after controlling for similarity to native]]
- [[Natural sequences have higher pTM but lower pLDDT than de novo sequences]]
- [[PLM-designed sequences match the distribution of fitness values, lengths, and structure prediction confidence of natural sequences]]
- [[Protein design using sequence-based models does not benefit from scale]]
- [[Protein folding neural networks cannot predict protein stability]]
- [[Protein structure prediction and design confidence metrics do not correlate with binding affinity]]
- [[Protein structure prediction and design metrics don't correlate with expression probability]]
- [[Randomly masking residues prior to running ESMFold allows false positives to be identified more effectively]]
- [[Reinforcement learning outperforms fine-tuning in property-guided inverse folding]]
- [[Self-consistency perplexity is correlated with pLDDT]]
- [[Sequence- and structure-derived ML quality metrics from ML do not correlate with each other]]
- [[Structure prediction uncertainty metrics as energy functions]]
- [[pLDDT and PAE in protein folding neural networks are correlated]]
- [[pLDDT and PAE inversely correlated with protein dynamics in dynamic naturally occurring proteins, but not de novo proteins]]
- [[pLDDT correlates with number of homologous sequences provided during runtime]]
- [[pLDDT is inversely correlated with CDRH3 length]]
- [[pTM is less lenient than pLDDT toward structural novelty when predicting alternate conformations]]
