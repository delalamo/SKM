---
tags:
  - protein-folding/misc
created: "2024-11-27T00:56:30"
modified: "2026-04-10T14:30:55"
---

#### Summary

**Mean-pooled embeddings outperform other zero-shot approaches when transfer learning on [[Protein language models|protein language models]]** [^vieira2024]. Moreover, the outperformance was more noticeably in variable-length datasets (PISCES) than fixed-lengths datasets (DMS). This was done using the ESM2-150M model with Lasso regression and cross-validation. However, [[Optimal transport outperforms mean-pooling on property prediction tasks|it was found to perform worse than optimal transport]], especially when using embeddings from small neural networks when a small amount of training data was available.

#### Figures

\![[Pasted-image-20241125084457.png]]

*Figure from [^vieira2024]*

[^vieira2024]: Vieira et al. (2024) "Medium-sized protein language models perform well at transfer learning on realistic datasets." https://doi.org/10.1101/2024.11.22.624936
