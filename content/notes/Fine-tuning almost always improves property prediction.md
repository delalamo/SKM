---
tags:
  - protein-language-models/training
  - thermostability/prediction
created: "2026-01-22T12:38:44"
modified: "2026-08-19T16:32:04"
---

#### Summary

**Fine-tuning [[protein-language-models|PLMs]] [[ESM]]2, ProtT5, and Ankh virtually always improved property prediction** ([[variant-effect-prediction|variant effect prediction]], [[thermostability|stability]] prediction, [[Function prediction|function prediction]], others) **compared to zero-shot across eight supervised benchmarks** [@schmirler2023]. This is not a guarantee for every objective or evaluation split: fine-tuning can degrade representations or generalization through high variance and [[Catastrophic forgetting|catastrophic forgetting]] [@detlefsen2022; @heinzinger2023]. [@jiang2024] found that active learning for [[Directed evolution|directed evolution]] benefited from fine-tuning over zero-shot prediction after two to four rounds (fine-tuning carried out using a [[Random forest|random forest]] model trained on mean-pooled embeddings).

#### Figures
![[Pasted-image-20240102175550.png]]

*Figure 1 from [@schmirler2023]*

![[Pasted-image-20240722093551.png]]

*Ref [@jiang2024]*

#### See also
* [[Protein property prediction using PLMs does not benefit from scale except when predicting inferring features of either structural or sparsely populated sequence families]]
* [[Sequences with lower log-likelihoods are worse for zero-shot variant effect prediction using PLMs]]
* [[Inverse-folding-guided site-saturation libraries outperform random mutagenesis]]
* [[Fine-tuning can be detrimental to performance]]
