---
tags:
  - protein-language-models/training
created: "2025-04-24T03:21:49"
modified: "2026-04-20T08:32:20"
---
#### Summary
**Sequence clustering of training data affects performance of [[Variant effect prediction|variant effect prediction]] by [[Protein language models|protein language models]]** [^meier2022]. Clustering at 90% leads to the best performance when training [[ESM]] models.

#### Figures
![[Pasted-image-20241009102907.png]]
*Ref [^meier2022]*

#### See also
- [[Correlation between sequence log-likelihood and variant effect prediction performance breaks down as PLMs get larger]]
- [[BERT models trained on sequence clusters outperform those trained on all data]]
- [[Alternate sequence clustering schemes outperform uniform sampling when training protein language models]]

[^meier2022]: Meier et al. (2021) "Language models enable zero-shot prediction of the effects of mutations on protein function." https://doi.org/10.1101/2021.07.09.450648
