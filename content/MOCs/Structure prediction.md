---
title: Structure prediction
tags:
  - structure-prediction
created: "2026-04-10T14:02:57"
modified: "2026-04-20T08:30:52"
---

**Structure prediction** refers to the problem of predicting the 3D shape of a protein or nucleotide sequence without any experimental information. Common metrics used for evaluating the quality of predicted structures include [[LDDT]] (residue-level, [[TM-score]] (whole-structure level), and [[DockQ]] (complex level).

## Methods
#### [[Multiple sequence alignments|MSA]]-based

* **[[AlphaFold2]]**: currently viewed as the highest-accuracy method
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

#### Training

![[Pasted-image-20231211070606.png]]
	*Figure from [@ahdritz2024]*

#### Sidechain prediction

* **Formulating the sidechain prediction problem as a classification problem by binning chi angles, rather than a regression problem, let to improved performance** ([[10.1002__prot.26705|Randolph and Kuhlman 2024]]).
* **Sidechain prediction methods not sensitive to B-factor cutoffs.** The outcome of sidechain prediction model PIPPack was not strongly affected by B-factor values of protein structures in the training set ([[10.1002__prot.26705|Randolph and Kuhlman 2024]]).

<!-- generated -->

## Sampling

- [[AlphaFold2 and RosettaFold sometimes produce different conformations]]
- [[AlphaFold2 generalizes to unseen secondary structures and topologies]]
- [[AlphaFold2 predicts Apo conformations with poorer RMSD than holo conformations]]
- [[AlphaFold2 predicts ground states more often]]
- [[AlphaFold2 predicts the holo form of proteins in most cases]]
- [[AlphaFold3 learns intramolecular interactions faster than intermolecular interactions]]
- [[AlphaFold3 performs comparably to AlphaFold2 when predicting multiple conformations of fold-switching proteins]]
- [[AlphaFold3 universally predicts the active state of ligand-bound GPCRs, even when the ligand is an antagonist]]
- [[Alternate conformations can be sampled by inverting AlphaFold2 and backpropagating along specific user-picked collective variables]]
- [[Alternate conformations can be sampled with MSA-based structure prediction methods using custom PDB databases and subsampled MSAs]]
- [[Conformational sampling by AlphaFold3-generation methods can be achieved by scaling the pair representation]]
- [[Guidance potentials can be added to diffusion-based structure prediction for enhanced sampling of protein conformations]]
- [[Language-based protein folding NNs predict novelty with far lower confidence than MSA-based protein folding NNs]]
- [[MSA-based structure predictions outperform PLM-based methods]]
- [[Masking ESMFold can sometimes sample alternate conformations]]
- [[Protein ensemble prediction methods do not generate conformations that are amenable to PPI docking]]
- [[Protein folding neural networks can be combined with VAEs for conformational modeling]]
- [[Structure prediction and design tools trained on monomers generalize to oligomers]]
- [[Structure prediction from conformational samplers tends to be worse than those from vanilla structure prediction methods]]
- [[Structure prediction methods undersample the conformational space they find to be high-confidence]]
- [[Structure prediction with AlphaFold improved when starting from an initial guess, rather than default initialization]]
- [[The AlphaFold and ESMFold databases can be mined for alternate conformations]]
- [[ddG predictions calculated from AlphaFold structures are equally accurate as those derived from experimental structures]]
- [[pLDDT and PAE inversely correlated with protein dynamics in dynamic naturally occurring proteins, but not de novo proteins]]
- [[pTM is less lenient than pLDDT toward structural novelty when predicting alternate conformations]]

## Metrics

- [[Confidence metrics for diffusion-based structure prediction methods can be improved with minimal changes to conditioning representations]]
- [[Confidence metrics from structure prediction correlate with accuracy even in the absence of coevolutionary data]]
- [[DiffDock confidence is inversely correlated with RMSD]]
- [[Sequence perplexity and TM-score are negatively correlated when predicting structure using protein language models]]
- [[Structure prediction metrics can be used to predict oligomer stoichiometry]]
- [[Structure prediction uncertainty metrics as energy functions]]
- [[The confidence metrics of AlphaFold2 are better calibrated than those of AlphaFold3]]
- [[pLDDT and PAE in protein folding neural networks are correlated]]
- [[pLDDT correlates with number of homologous sequences provided during runtime]]

## Training

- [[AlphaFold3 uses cross-distillation from AlphaFold2 to avoid hallucinating secondary structure in low-pLDDT regions]]
- [[Diverse MSAs are better for training structure prediction neural networks than random MSAs]]
- [[Fine-tuning AlphaFold for MHC prediction by adding Evoformer layers improves RMSD and pLDDT]]
- [[Fine-tuning base models on test cases can improve the performance of variant effect and structure prediction]]
- [[Including crystal contacts in training data improves sidechain prediction]]
- [[Increasing RosettaFold embedding dimension improves structure prediction]]
- [[MSA-based structure prediction models can be retrained as pathogenicity prediction models by upweighting BERT losses]]
- [[Protein models designed using inverse folding can be used to supplement training DBs for PLMs and structure prediction models]]
- [[RMSD is a poor training objective for structure prediction]]
- [[Scrambled MSAs outperform single-sequence-prediction with AlphaFold]]
- [[Self-distillation exposes more data to Evoformer]]
- [[Training protein structure prediction neural networks on both positive and negative protein-protein interactions improves PPI discrimination]]

## Architecture

- [[FAPE can be extended to ligands]]
- [[Flow matching and diffusion perform comparably for biomolecular structure prediction]]
- [[Invariant point attention is dispensable to structure prediction]]
- [[Iterative structure prediction outperforms all-at-once structure prediction]]
- [[ProteinMPNN and AlphaFold structure update module can be combined into a VAE]]
- [[The Evoformer can calculate ligand-binding residues]]
- [[The latent space of ESMFold is dicontinuous, but can be smoothened by channel compression]]
- [[Triangular updates are dispensable for structure prediction]]

## Limitations

- [[All-atom protein structure prediction methods are unable to model PPIs with large buried surface areas]]
- [[All-atom structure prediction of RNA is driven by memorization]]
- [[Coevolutionary patterns in multiple sequence alignments do not contribute to protein-protein complex prediction]]
- [[Correct protomer structure prediction is necessary but insufficient for accurate protein-protein docking]]
- [[Crystal structures can have nonphysiological salt bridges]]
- [[DL ligand docking methods generate unrealistic poses]]
- [[DL structure prediction methods cannot predict CDR conformations unseen during training]]
- [[DL structure tools introduce chiral errors such as swapped chiral centers, D-amino acids, and cis-amide bonds]]
- [[Memorization in protein structure prediction]]
- [[Protein folding neural networks can be subject to adversarial attacks]]
- [[Protein folding neural networks cannot predict protein stability]]
- [[Protein folding neural networks do not extrapolate to new ligand binding sites]]
- [[Protein folding neural networks do not learn the physics of protein folding for most proteins]]
- [[Protein folding neural networks make local optimizations in the absence of coevolutionary information]]
- [[Protein structure prediction methods are unable to predict the energetics of a conformational landscape unless explicitly trained for that purpose]]
- [[Protein-ligand co-folding methods do not generalize beyond their training set]]
- [[Randomly masking residues prior to running ESMFold allows false positives to be identified more effectively]]
- [[Unfolded and nonfunctional isoforms of folded proteins are incorrectly predicted as folded by protein folding neural networks]]
- [[Variable regions can adopt multiple interchain orientations, and these are difficult to predict]]

## Complex Prediction

- [[All-atom protein structure prediction methods are unable to model PPIs with large buried surface areas]]
- [[AlphaFold3 ipTM can distinguish between antibody binders and nonbinders]]
- [[Antibody-antigen modeling by diffusion-based structure prediction is data-limited]]
- [[Antigen context improves CDRH3 structure prediction]]
- [[Correct CDRH3 prediction is necessary but insufficient for correct Ab-Ag docking]]
- [[Correct antibody-antigen prediction in AF3 and related models is partially determined by training set similarity]]
- [[Correct protomer structure prediction is necessary but insufficient for accurate protein-protein docking]]
- [[Increasing diffusion samples is sufficient to yield correctly predicted antibody-antigen complexes]]

## Experimental Data

- [[Computational models of proteins fit NMR data better than models designed using classical approaches]]
- [[Ligand-binding sites fit experimental electron density better than other parts of protein structures]]

## General

- [[Evolutionary pathway between two folds identified using AlphaFold2 and ancestral sequence reconstruction]]
