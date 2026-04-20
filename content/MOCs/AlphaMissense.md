---
title: AlphaMissense
tags: citation-fix
created: 2026-04-10T14:02:57
modified: "2026-04-20T08:16:13"
---

**AlphaMissense** is a [[Protein language models|protein language model]] designed for [[Variant effect prediction|variant effect prediction]] that is built on top of [[AlphaFold2]] and fine-tuned using primate data. During its release, it achieved state-of-the-are performance on ClinVar data, and predicted that a third of missense mutations in the human proteome were likely pathogenic and half as likely benign. A later paper found that, in the ion channel CFTR, it had both a high false positive rate and high correlation with *in vitro* functional data, concluding that it "cannot differentiate mechanistic effects or the nature of pathophysiology" (https://doi.org/10.1371/journal.pone.0297560).

![[AlphaMissense.png]]
*Ref [^cheng2023]*

#### Notes

* Three-stage training procedure:
	1. Structure prediction and MSA site prediction (vanilla AlphaFold2), except the [[BERT]] losses were upweighted
	2. Fine-tuning on primate sequences
	3. [[Distillation|Self-distillation]] and repeat
* Ablation studies suggest the entire training procedure is necessary
* Reduced performance on residues predicted to be disordered

<!-- generated -->

[^cheng2023]: Cheng et al. (2023) "Accurate proteome-wide missense variant effect prediction with AlphaMissense." *Science*. https://doi.org/10.1126/science.adg7492
