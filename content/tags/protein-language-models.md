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
- **ProtBERT** and **DistillProtBERT** [@geffen2022]
- **[[ProteinNPT]]**
- **xTrimoPGLM**
- **CARP**: A [[Convolutional neural networks|CNN]] that performs as well as transformer-based methods on both pretraining and downstream tasks. Anecdotally, these can't indirectly calculate contact maps via the [[Categorical Jacobian method]] as well as transformer-based models.
- **DASM** (deep amino acid sequence model), which is trained on germline-descendant point mutation pairs to learn relative mutation frequencies, after normalizing for expected mutation frequencies in the codon table [@elife109644].

## Notes

#### General observations

- **PLMs are in-context learners that default to retrieving information from nearby repeats** [@kantroo2025].

#### Representations

- **Multiple instance learning using PLM embeddings of all genes in a viral genome identifies which sequences are responsible for host tropism** [@liu2024d]. For example, this ranked the [[Spike protein]] as the key contributor of host tropism.
- **Homolog detection using PLM representations can be improved by compression** [@kilinc2023]. Using the full representations worsened detection AUC by 7.4%.
- **[[tags/protein-language-models|PLMs]] with a smoother representation space are better predictors of protein function** [@matthews2023].
 ![[Pasted-Graphic-2-1.png]]
 _Figure from [@matthews2023]_

#### Hybrid PLM-[[tags/inverse-folding|inverse folding]] models

_From [[Hybrid sequence-structure models]]_

#### Training

- **Matthews et al. [@matthews2023] found that masking 0.5% of residues when training [[tags/protein-language-models|PLMs]] improved predictive performance (greater $R^{2}$) relative to 15% used by [[ESM]].**
