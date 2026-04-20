---
title: Protein language models
aliases:
  - Protein language models
created: "2026-04-10T10:46:24"
modified: "2026-04-20T07:16:03"
---

**Protein language models** (PLMs) are a type of [[Transformer]] model trained on either protein sequences or [[Multiple sequence alignments]].

## Methods

#### Single-sequence

- **[[ESM]]**: currently the most widely-used encoder PLM
- **[[ProGen]]**: probably the most widely-used decoder PLM
- **ProtBERT** and **DistillProtBERT** (doi.org/10.1093/bioinformatics/btac474)
- **[[ProteinNPT]]**
- **xTrimoPGLM**
- **CARP**: A [[Convolutional neural networks|CNN]] that performs as well as transformer-based methods on both pretraining and downstream tasks. Anecdotally, these can't indirectly calculate contact maps via the [[Categorical Jacobian method]] as well as transformer-based models.
- **DASM** (deep amino acid sequence model), which is trained on germline-descendant point mutation pairs to learn relative mutation frequencies, after normalizing for expected mutation frequencies in the codon table (doi.org/10.7554/eLife.109644.3.sa0).

## Notes

#### General observations

- **PLMs are in-context learners that default to retrieving information from nearby repeats** ([[10.48550__ARXIV.2504.17068|Kantroo et al 2025]]).

#### Representations

- **Multiple instance learning using PLM embeddings of all genes in a viral genome identifies which sequences are responsible for host tropism** ([[10.1371__journal.pcbi.1012597|Liu et al 2024d]]). For example, this ranked the [[Spike protein]] as the key contributor of host tropism.
- **Homolog detection using PLM representations can be improved by compression** ([[10.1073__pnas.2211823120|Kilinc et al 2023]]). Using the full representations worsened detection AUC by 7.4%.
- **[[Protein language models|PLMs]] with a smoother representation space are better predictors of protein function** ([[10.1038__s42256-024-00935-2|Matthews et al 2024]]).
  ![[Pasted-Graphic-2-1.png]]
  _Figure from [^matthews2023]_

#### Hybrid PLM-[[Inverse folding|inverse folding]] models

_From [[Hybrid sequence-structure models]]_

#### Training

- **[[10.1038__s42256-024-00935-2|Matthews et al 2024]] found that masking 0.5% of residues when training [[Protein language models|PLMs]] improved predictive performance (greater $R^{2}$) relative to 15% used by [[ESM]].**
