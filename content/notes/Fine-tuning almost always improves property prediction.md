---
tags:
  - protein-language-models/training
  - thermostability/prediction
created: "2026-01-22T12:38:44"
modified: "2026-08-25T13:38:32"
---

#### Summary

**Fine-tuning [[protein-language-models|PLMs]] [[ESM]]2, ProtT5, and Ankh virtually always improves property prediction** ([[variant-effect-prediction|variant effect prediction]], [[thermostability|stability]] prediction, [[Function prediction|function prediction]], others) **compared to zero-shot across eight supervised benchmarks** [@schmirler2023]. However, this is not a guarantee for every objective or evaluation split: fine-tuning can degrade representations or generalization through high variance and [[Catastrophic forgetting|catastrophic forgetting]] [@detlefsen2022; @heinzinger2023]. When fine-tuning on paired [[antibodies|antibody]] sequences, retaining the unpaired pretraining data and objective mitigated forgetting [@kenlay2024large]. Outside protein ML, RLHF also worsened the performance of [[GPT]]-4 on some tasks [@chen2024how].

#### Figures
![[Pasted-image-20240102175550.png]]

*Figure 1 from [@schmirler2023]*

![[Pasted-image-20240722093551.png]]

*Ref [@jiang2024]*

![[Fine-tuning-benchmark.png]]

*Ref [@detlefsen2022]*

#### See also
* [[Protein property prediction using PLMs does not benefit from scale except when predicting inferring features of either structural or sparsely populated sequence families]]
* [[Sequences with lower log-likelihoods are worse for zero-shot variant effect prediction using PLMs]]
* [[Inverse-folding-guided site-saturation libraries outperform random mutagenesis]]
