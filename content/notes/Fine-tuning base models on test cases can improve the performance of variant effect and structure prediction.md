---
tags:
  - protein-folding/misc
created: "2026-04-05T23:36:09"
modified: "2026-04-05T23:36:09"
---
#### Summary
**Fine-tuning base models (such as [[Transformer|transformers]]) on test data of interest can lead to improved prediction of [[Structure prediction|protein structure]] and [[Variant effect prediction|variant effect]]** [^bushuiev2024]. This was shown with [[ESMFold]] using standard masked [[Protein language models|language model]] loss, leading to improvements in [[pLDDT]] and zero-shot [[Variant effect prediction|variant effect prediction]]. [[Low-rank Adaptation|Low-rank adaptation]] is used to overcome the cost of backpropagation across such a large network.

#### Figures
![](/assets/Pasted-image-20241112055147.png)
*Figure from [^bushuiev2024]*

[^bushuiev2024]: Bushuiev et al. (2024) "One protein is all you need." https://doi.org/10.48550/ARXIV.2411.02109
