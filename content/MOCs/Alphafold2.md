---
title: Alphafold2
tags:
  - alphafold2
aliases:
  - openfold
created: "2026-04-11T06:06:39"
modified: "2026-04-20T10:13:23"
---
*(OpenFold redirects here)*

**AlphaFold2** is a protein [[Structure prediction|structure prediction]] method from 2020, and is the first to make extensive use of the [[Transformer]] architecture, consisting of 97 million parameters. [[AlphaMissense]] is a derivative of this method.

![[Pasted-image-20231029184254.png]]
*Architecture of AlphaFold2 from [[10.1038__s41586-021-03819-2|Jumper et al 2021]]*

#### Architectural and ML contributions

* [[Evoformer]]
* [[Invariant point attention]]
* [[Frame aligned point error]]
* [[Distillation|Self-distillation]] for protein structures
* [[Predicted aligned error]]
* [[Triangular update]]

<!-- generated -->

## General

- [[AF2 RMSD to ground truth correlated with RMSD between conformations]]
- [[AlphaFold2 and RosettaFold sometimes produce different conformations]]
- [[AlphaFold2 generalizes to unseen secondary structures and topologies]]
- [[AlphaFold2 outperforms ESMFold at distinguishing designable and undesignable protein backbones]]
- [[AlphaFold2 predicts Apo conformations with poorer RMSD than holo conformations]]
- [[AlphaFold2 predicts ground states more often]]
- [[AlphaFold2 predicts the holo form of proteins in most cases]]
- [[AlphaFold2 recapitulates interaction biases from PDB when modeling antibodies]]
- [[AlphaFold3 performs comparably to AlphaFold2 when predicting multiple conformations of fold-switching proteins]]
- [[Alternate conformations can be sampled by inverting AlphaFold2 and backpropagating along specific user-picked collective variables]]
- [[Antibodies can be humanized using AlphaFold2 models]]
- [[Antibody structure prediction improved with AlphaFold2 features]]
- [[Conformationally stabilizing mutations can be identified from sequence clusters that are predicted to fold into that conformation when passed to AlphaFold2]]
- [[Dropout improves AF2 multimer prediction, including for antibody-antigen complexes]]
- [[Fine-tuning AlphaFold for MHC prediction by adding Evoformer layers improves RMSD and pLDDT]]
- [[Monomeric AF2 is better able to distinguish positive and negative PPIs than AF2-multimer]]
- [[ProteinMPNN and AlphaFold structure update module can be combined into a VAE]]
- [[Scrambled MSAs outperform single-sequence-prediction with AlphaFold]]
- [[Structure prediction with AlphaFold improved when starting from an initial guess, rather than default initialization]]
- [[The AlphaFold and ESMFold databases can be mined for alternate conformations]]
- [[The confidence metrics of AlphaFold2 are better calibrated than those of AlphaFold3]]
- [[ddG predictions calculated from AlphaFold structures are equally accurate as those derived from experimental structures]]
