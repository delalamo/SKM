---
tags:
  - structure-prediction/architecture
created: "2024-08-13T05:05:39"
modified: "2026-04-11T07:41:30"
---

#### Summary

**The [[Protein language models#Representations|latent space]] of [[ESMFold]] is discontinuous** [^del2023][^lu2024]. However, it can be smoothened by compression using a [[Variational autoencoders|VAE]].

#### Figures

![[Original-Latent-Space.png]]

*Figure from [^lu2024]*

#### See also

- [[Masking ESMFold can sometimes sample alternate conformations]]

[^del2023]: del Alamo et al. (2023) "Conformational sampling and interpolation using language-based protein folding neural networks." https://doi.org/10.1101/2023.12.16.571997
[^lu2024]: Lu et al. (2024) "Tokenized and Continuous Embedding Compressions of Protein Sequence and Structure." https://doi.org/10.1101/2024.08.06.606920
