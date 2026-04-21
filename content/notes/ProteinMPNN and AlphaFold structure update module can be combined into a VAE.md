---
title: ProteinMPNN and AlphaFold structure update module can be combined into a VAE
tags:
  - alphafold2
  - structure-prediction/architecture
created: "2024-12-10T01:40:23"
modified: "2026-04-21T07:28:09"
---
#### Summary
 **The encoder from [[ProteinMPNN]] and the structure update module from (AlphaFold2) can be combined into a [[Variational autoencoders|vector-quantized variational autoencoder]]** [@gaujac2024]. They use a vector-quantized VAE similar to [[Foldseek]] to learn a [[protein-structure-tokenization|discrete vocabulary]] of either ~4000 or ~64000 possible structural tokens. [[Frame aligned point error]] is used as a loss function.
