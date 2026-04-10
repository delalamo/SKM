---
title: Protein language models
tags:
  - protein-language-models
created: "2026-04-10T10:46:24"
modified: "2026-04-10T10:46:24"
---

**Protein language models** (PLMs) are a type of [[Transformer]] model trained on either protein sequences or [[Multiple sequence alignments]].

## Methods
#### Single-sequence

* **[[ESM]]**: currently the most widely-used encoder PLM
* **[[ProGen]]**: probably the most widely-used decoder PLM
* **ProtBERT** and **DistillProtBERT** ([[10.1093__bioinformatics__btac474|Geffen et al 2022]])
* **[[ProteinNPT]]**
* **xTrimoPGLM**
* **CARP**: A [[Convolutional neural networks|CNN]] that performs as well as transformer-based methods on both pretraining and downstream tasks. Anecdotally, these can't indirectly calculate contact maps via the [[Categorical Jacobian method]] as well as transformer-based models.
* **DASM** (deep amino acid sequence model), which is trained on germline-descendant point mutation pairs to learn relative mutation frequencies, after normalizing for expected mutation frequencies in the codon table ([[10.7554__eLife.109644.3.sa0|Matsen et al 2026]]).

#### Antibody-specific

*From [[Antibody language models#Models]]*

## Notes
#### General observations

* **PLMs are in-context learners that default to retrieving information from nearby repeats** ([[10.48550__ARXIV.2504.17068|Kantroo et al 2025]]).

#### Representations

* **Multiple instance learning using PLM embeddings of all genes in a viral genome identifies which sequences are responsible for host tropism** ([[10.1101__2023.04.07.536023|Liu et al 2023d]]). For example, this ranked the [[Spike protein]] as the key contributor of host tropism.
* **Homolog detection using PLM representations can be improved by compression** ([[10.1073__pnas.2211823120|Kilinc et al 2023]]). Using the full representations worsened detection AUC by 7.4%.
* **[[Protein language models|PLMs]] with a smoother representation space are better predictors of protein function** ([[10.1101__2023.12.20.572683|Matthews et al 2023]]).
	![](/assets/Pasted-Graphic-2-1.png)
	*Figure from [[10.1101__2023.12.20.572683|Matthews et al 2023]]*

#### Hybrid PLM-[[Inverse folding|inverse folding]] models

*From [[Hybrid sequence-structure models]]*

#### Training

* **[[10.1101__2023.12.20.572683|Matthews et al 2023]] found that masking 0.5% of residues when training [[Protein language models|PLMs]] improved predictive performance (greater $R^{2}$) relative to 15% used by [[ESM]].**

<!-- generated -->
