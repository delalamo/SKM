---
tags:
  - protein-language-models/training
  - structure-prediction/training
  - plddt
  - low-rank-adaptation
created: 2026-04-05T23:36:09
modified: "2026-04-21T07:03:26"
---
#### Summary
**Fine-tuning base models (such as [[Transformer|transformers]]) on test data of interest can lead to improved prediction of [[tags/structure-prediction|protein structure]] and [[tags/variant-effect-prediction|variant effect]]** [@bushuiev2024]. This was shown with [[ESMFold]] using standard masked [[tags/protein-language-models|language model]] loss, leading to improvements in [[tags/plddt|pLDDT]] and zero-shot [[tags/variant-effect-prediction|variant effect prediction]]. [[Low-rank Adaptation|Low-rank adaptation]] is used to overcome the cost of backpropagation across such a large network.

#### Figures
![[Pasted-image-20241112055147.png]]
*Ref [@bushuiev2024]*
