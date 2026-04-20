---
tags:
  - structure-prediction/architecture
created: "2024-08-13T05:05:39"
modified: "2026-04-20T08:32:20"
---

#### Summary

**The [[Protein language models#Representations|latent space]] of [[ESMFold]] is discontinuous** [^del2023][^lu2024]. However, it can be smoothened by compression using a [[Variational autoencoders|VAE]].

#### Figures

![[Original-Latent-Space.png]]

*Ref [^lu2024]*

#### See also

- [[Masking ESMFold can sometimes sample alternate conformations]]

[^del2023]: del Alamo et al. (2023) "Conformational sampling and interpolation using language-based protein folding neural networks." https://doi.org/10.1101/2023.12.16.571997
[^lu2024]: Lu et al. (2025) "Tokenized and continuous embedding compressions of protein sequence and structure." Patterns. https://doi.org/10.1016/j.patter.2025.101289
