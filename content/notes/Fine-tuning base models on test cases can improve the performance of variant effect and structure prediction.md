---
tags:
  - protein-language-models/training
  - structure-prediction/training
  - plddt
  - low-rank-adaptation
created: 2026-04-05T23:36:09
modified: "2026-08-19T16:32:04"
---
#### Summary
**Fine-tuning base models (such as [[Transformer|transformers]]) on test data of interest can lead to improved prediction of [[structure-prediction|protein structure]] and [[variant-effect-prediction|variant effect]]** [@bushuiev2024]. This was shown with [[ESMFold]] using standard masked [[protein-language-models|language model]] loss, leading to improvements in [[plddt|pLDDT]] and zero-shot [[variant-effect-prediction|variant effect prediction]]. [[Low-rank Adaptation|Low-rank adaptation]] is used to overcome the cost of backpropagation across such a large network.

#### Figures
![[Pasted-image-20241112055147.png]]
*Ref [@bushuiev2024]*

#### See also

* [[Fine-tuned protein language models don't generalize to positions absent in the fine-tuning data]]
