---
tags:
  - model-design/multimodal
  - model-design/generative-models
created: 2024-12-10T01:40:01
modified: "2026-07-19T10:07:27"
---

## Summary

**Compression of protein sequences and [[notes/structure-prediction|structures]] from [[notes/protein-language-models#Representations|PLM representations]] passed through [[Variational autoencoders|VQ-VAEs]] is prone to codebook collapse when insufficiently compressed** [@lu2025tokenized]. This can be ameliorated using alternative architectures.

## Figures

![[Codebook-Sizel.png]]
*Ref [@lu2025tokenized]*

## See also

* [[notes/protein-structure-tokenization|Protein structure tokenization]]
* [[Straight-through estimator]]
