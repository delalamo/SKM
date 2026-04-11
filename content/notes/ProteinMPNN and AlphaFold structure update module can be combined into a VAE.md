---
title: ProteinMPNN and AlphaFold structure update module can be combined into a VAE
tags:
  - alphafold2
  - structure-prediction
created: "2024-12-10T01:40:23"
modified: "2026-04-11T06:06:39"
---
#### Summary
 **The encoder from [[ProteinMPNN]] and the structure update module from (AlphaFold2) can be combined into a [[Variational autoencoders|vector-quantized variational autoencoder]]** [^gaujac2024]. They use a vector-quantized VAE similar to [[Foldseek]] to learn a [[Protein structure tokenization|discrete vocabulary]] of either ~4000 or ~64000 possible structural tokens. [[Frame aligned point error]] is used as a loss function.

[^gaujac2024]: Gaujac et al. (2024) "Learning the Language of Protein Structure." https://doi.org/10.48550/ARXIV.2405.15840
