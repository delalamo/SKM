---
tags:
  - training/fine-tuning
  - prediction/variant-effects
  - prediction/structure
created: 2026-04-05T23:36:09
modified: "2026-04-21T07:28:09"
---
#### Summary
**Fine-tuning base models (such as [[Transformer|transformers]]) on test data of interest can lead to improved prediction of [[notes/Structure prediction|protein structure]] and [[notes/Variant effect prediction|variant effect]]** [@bushuiev2024]. This was shown with [[ESMFold]] using standard masked [[notes/Protein language models|language model]] loss, leading to improvements in [[notes/pLDDT|pLDDT]] and zero-shot [[notes/Variant effect prediction|variant effect prediction]]. [[Low-rank Adaptation|Low-rank adaptation]] is used to overcome the cost of backpropagation across such a large network.

#### Figures
![[Pasted-image-20241112055147.png]]
*Ref [@bushuiev2024]*
