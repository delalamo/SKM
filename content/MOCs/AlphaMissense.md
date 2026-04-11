---
title: AlphaMissense
tags:
  - alphamissense
created: "2026-04-10T14:02:57"
modified: "2026-04-11T07:42:59"
---

**AlphaMissense** is a [[Protein language models|protein language model]] designed for [[Variant effect prediction|variant effect prediction]] that is built on top of [[AlphaFold|AlphaFold2]] and fine-tuned using primate data. Achieves state-of-the-are performance on ClinVar data.

![[AlphaMissense.png]]
*Figure from [[10.1126__science.adg7492|Cheng et al 2023]]*

#### Notes

* Three-stage training procedure:
	1. Structure prediction and MSA site prediction (vanilla AlphaFold2), except the [[BERT]] losses were upweighted
	2. Fine-tuning on primate sequences
	3. [[Distillation|Self-distillation]] and repeat
* Ablation studies suggest the entire training procedure is necessary
* A third of missense mutations in the human proteome were defined as likely pathogenic and half as likely benign
* Reduced performance on residues predicted to be disordered
* **AlphaMissense had a high false-positive rate in CFTR, but had higher correlation with *in vitro* functional data** ([[10.1101__2023.10.05.561147|McDonald et al 2023]]). Authors concluded that it "cannot differentiate mechanistic effects or the nature of pathophysiology."
* **AlphaMissense has the strongest correlation between performance on DMS datasets and on clinical datasets out of all variant effect predictors tested by [[10.1101__2024.05.12.593741|Livesey & Marsh 2024]].**
![[Figure-S1.-Distribution-of-Spearman's-correlations-of-different-VEPs-across-different-DMS-datasets..png]]

<!-- generated -->
