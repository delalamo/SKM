---
title: AlphaMissense
tags: citation-fix
created: 2026-04-10T14:02:57
modified: "2026-04-21T07:03:26"
---

**AlphaMissense** is a [[tags/protein-language-models|protein language model]] designed for [[tags/variant-effect-prediction|variant effect prediction]] that is built on top of [[tags/alphafold2|AlphaFold2]] and fine-tuned using primate data. During its release, it achieved state-of-the-are performance on ClinVar data, and predicted that a third of missense mutations in the human proteome were likely pathogenic and half as likely benign. A later paper found that, in the ion channel CFTR, it had both a high false positive rate and high correlation with *in vitro* functional data, concluding that it "cannot differentiate mechanistic effects or the nature of pathophysiology" [@mcdonald2024].

![[AlphaMissense.png]]
*Ref [@cheng2023]*

#### Notes

* Three-stage training procedure:
	1. Structure prediction and MSA site prediction (vanilla AlphaFold2), except the [[BERT]] losses were upweighted
	2. Fine-tuning on primate sequences
	3. [[Distillation|Self-distillation]] and repeat
* Ablation studies suggest the entire training procedure is necessary
* Reduced performance on residues predicted to be disordered
