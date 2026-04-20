---
title: Protein language models
tags:
  - protein-language-models
created: "2026-04-10T10:46:24"
modified: "2026-04-20T10:13:23"
---

**Protein language models** (PLMs) are a type of [[Transformer]] model trained on either protein sequences or [[Multiple sequence alignments]].

## Methods
#### Single-sequence

* **[[ESM]]**: currently the most widely-used encoder PLM
* **[[ProGen]]**: probably the most widely-used decoder PLM
* **ProtBERT** and **DistillProtBERT** (doi.org/10.1093/bioinformatics/btac474)
* **[[ProteinNPT]]**
* **xTrimoPGLM**
* **CARP**: A [[Convolutional neural networks|CNN]] that performs as well as transformer-based methods on both pretraining and downstream tasks. Anecdotally, these can't indirectly calculate contact maps via the [[Categorical Jacobian method]] as well as transformer-based models.
* **DASM** (deep amino acid sequence model), which is trained on germline-descendant point mutation pairs to learn relative mutation frequencies, after normalizing for expected mutation frequencies in the codon table (doi.org/10.7554/eLife.109644.3.sa0).

## Notes
#### General observations

* **PLMs are in-context learners that default to retrieving information from nearby repeats** ([[10.48550__ARXIV.2504.17068|Kantroo et al 2025]]).

#### Representations

* **Multiple instance learning using PLM embeddings of all genes in a viral genome identifies which sequences are responsible for host tropism** ([[10.1101__2023.04.07.536023|Liu et al 2023d]]). For example, this ranked the [[Spike protein]] as the key contributor of host tropism.
* **Homolog detection using PLM representations can be improved by compression** ([[10.1073__pnas.2211823120|Kilinc et al 2023]]). Using the full representations worsened detection AUC by 7.4%.
* **[[Protein language models|PLMs]] with a smoother representation space are better predictors of protein function** ([[10.1101__2023.12.20.572683|Matthews et al 2023]]).
![[Pasted-Graphic-2-1.png]]
	*Figure from [^matthews2023]*

#### Hybrid PLM-[[Inverse folding|inverse folding]] models

*From [[Hybrid sequence-structure models]]*

#### Training

* **[[10.1101__2023.12.20.572683|Matthews et al 2023]] found that masking 0.5% of residues when training [[Protein language models|PLMs]] improved predictive performance (greater $R^{2}$) relative to 15% used by [[ESM]].**

<!-- generated -->

## Training

- [[Alternate sequence clustering schemes outperform uniform sampling when training protein language models]]
- [[Alternative noise schedules improve training of multimodal PLMs]]
- [[BERT models trained on sequence clusters outperform those trained on all data]]
- [[Base PLMs must usually be fine-tuned to generate functionally active sequences]]
- [[Diverse MSAs are better for training structure prediction neural networks than random MSAs]]
- [[Fine-tuning almost always improves property prediction]]
- [[Fine-tuning base models on test cases can improve the performance of variant effect and structure prediction]]
- [[Fine-tuning can be detrimental to performance]]
- [[Hybrid protein sequence-structure ML models rely more on sequence when many homologs were available during training]]
- [[Including optimal growth temperature during pre-training of PLMs improves prediction and design of thermostability]]
- [[Including sequences from multiplexed ancestral sequence reconstruction improves PLM training]]
- [[Incorporating ancestral sequences during PLM training improves performance in downstream tasks]]
- [[Larger PLMs generate more novel sequences from more sparsely populated protein families]]
- [[Logistic regression outperforms fine-tuned LMs on finding point mutations from NGS data]]
- [[ML models trained exclusively on experimental structures are less effective on computational models]]
- [[MSA-based structure prediction models can be retrained as pathogenicity prediction models by upweighting BERT losses]]
- [[Masked LMs can be fine-tuned starting from autoregressive LMs, but not vice-versa]]
- [[Masked PLMs are more sensitive to training imbalances than autoregressive PLMs]]
- [[Overtrained language models are more difficult to fine-tune]]
- [[PLMs are biased by uneven distribution of sequence data in datasets such as UniRef and UniProt]]
- [[Pretraining contributes nearly nothing to performance when fine-tuning protein language models in data-rich situations]]
- [[Protein design using sequence-based models does not benefit from scale]]
- [[Protein language models have a lower bound of training loss regardless of size]]
- [[Protein language models make equally effective predictions when trained on individual proteins or protein families]]
- [[Protein models designed using inverse folding can be used to supplement training DBs for PLMs and structure prediction models]]
- [[Residue conservation and solvent exposure data perform comparably to PLMs at some property prediction tasks]]
- [[Sequence clustering of training data affects variant effect prediction performance by PLMs]]
- [[Sequence-only protein language models implicitly cluster proteins at fineness levels that increase with size]]
- [[Training on newly updated databases doesn't guarantee better performance]]
- [[Unbalanced composition of sequence data prevents protein fitness from being identifiable from sequence data alone]]
- [[Unfreezing PLM during structure training improves prediction quality]]

## Representations

- [[Concatenating sequence and structural features is not effective for sequence recovery]]
- [[Contrastive learning of PLM embeddings on functional annotation improves variant effect prediction and homolog detection]]
- [[Contrastive learning on whole structures leads to learning of distinct substructures]]
- [[Correlation between sequence log-likelihood and variant effect prediction performance breaks down as PLMs get larger]]
- [[Distance between PLM representations of two proteins correlates with functional dissimilarity]]
- [[Distance between averaged PLM embeddings does not correlate with structural difference]]
- [[Enzymes can be miniaturized with Monte Carlo sampling and embedding similarity of catalytic residues]]
- [[HMMs cannot identify remote homologs]]
- [[High-confidence predictions from protein language models co-cluster together in embedding space and correlate with performance on variant effect prediction tasks]]
- [[Larger PLMs are better at homolog detection]]
- [[Mean-pooled embeddings outperform other zero-shot approaches for transfer learning of PLMs using the full sequence]]
- [[Membrane proteins are predicted by PLMs via solvent-exposed hydrophobic residues]]
- [[Optimal transport outperforms mean-pooling on property prediction tasks]]
- [[PLM attention maps from specific heads can be used to predict allosteric networks]]
- [[PLM attention matrices correspond to 3D contacts]]
- [[PLM embeddings contain enough information to align proteins without fine-tuning]]
- [[PLM embeddings fine-tuned using contrastive learning outperform other representations in drug-target interaction prediction]]
- [[PLM-based sequence searches outperform sequence- and matches structure-based search methods]]
- [[PLM-derived antibody representations can distinguish engineered from human-derived Abs]]
- [[PLMs learn family-specific protein contacts from sequence context windows of about 20-40 amino acids]]
- [[Protein language model embeddings are more predictive of homology than catalytic efficiency]]
- [[Protein language models are able to predict epistasis in a zero-shot setting following a nonlinear transform]]
- [[Protein language models are better zero-shot predictors for ranking closely related sequences than distantly related sequences]]
- [[Protein language models can predict zero-shot which proteins belong to the same species]]
- [[Protein language models learn structure-level features, including disorder, in later layers]]
- [[Protein property prediction using PLMs does not benefit from scale except when predicting inferring features of either structural or sparsely populated sequence families]]
- [[Sequence homology composition can affect performance of fine-tuned protein language models for variant effect prediction]]
- [[Sequences with lower log-likelihoods are worse for zero-shot variant effect prediction using PLMs]]
- [[Sparse autoencoder-derived features do not outperform PLM-derived embeddings for downstream prediction]]
- [[Structural classifications can be learned from PLM-based alignment prediction]]
- [[Structure-based methods outperform sequence-based methods at zero-shot prediction of binding, whereas the reverse is true for zero-shot prediction of enzymatic activity]]
- [[Structure-derived embeddings outperform sequence-derived embeddings on LM-based alignment]]
- [[Variant effect prediction with homology-aware PLMs improves with ensembling of multiple prompts]]
- [[Zero-shot performance of PLMs, but not inverse folding models, correlates with number of homologs available for training]]
- [[Zero-shot protein fitness prediction using sequence-only NNs can be improved by averaging predictions from many orthologs]]

## Antibodies

- [[Antibody LMs are worse for expression prediction than generic PLMs]]
- [[Antibody LMs outperform generic PLMs on intrafamily thermostability prediction]]
- [[Antibody PLMs match or outperform generic PLMs on specificity prediction]]
- [[Antibody language models are able to distinguish correctly and incorrectly paired sequences, but are sensitive to scale and training dataset size]]
- [[Attention matrices from antibody LMs can be used for paratope prediction]]
- [[Attention matrices of antibody language models do not correspond to contacts]]
- [[CDR representations segregate into distinct clusters]]
- [[Contrastive fine-tuning PLMs on inverse folding embeddings of experimental structures but not computational models improves downstream tasks]]
- [[Features for antibody property prediction derived from MD simulations outperform those from language models and static structures]]
- [[Generic PLMs outperform antibody-specific PLMs on zero-shot predictions of affinity changes]]
- [[LM-based antibody structure prediction methods work equally well with generic and Ab PLMs]]
- [[Light chain representations affected by heavy chain, but not vice versa]]
- [[Optimal scaling of antibody LMs improves prediction of masked CDRH3 residues but not framework residues]]
- [[PLMs are better at reproducing sequence-based developability predictions than structure-based predictions]]
- [[PLMs are biased toward germline antibodies]]
- [[PLMs can separate Abs by origin]]
- [[PLMs cluster antibodies from the same repertoire by maturation status]]
- [[Paired antibody LMs outperform equivalent unpaired LMs on sequence recovery for various regions]]
- [[Structure-based methods outperform sequence-based methods on antigen-dependent antibody design]]
- [[Template CDR retrieval using embeddings]]
- [[Training antibody language models on normalized mutation frequencies improves zero-shot expression prediction]]

## General

- [[Categorical Jacobian method]]
- [[PLM-designed sequences match the distribution of fitness values, lengths, and structure prediction confidence of natural sequences]]
- [[Subnetworks within protein language models encode specific protein families]]
