---
title: Protein structure tokenization
tags:
  - protein-structure-tokenization
created: "2026-04-10T14:30:55"
modified: "2026-04-20T10:13:23"
---

**Protein structure tokenization** refers to the process of discretizing protein structure using a learned codebook derived from [[Variational autoencoders|vector-quantized variational autoencoders]]. It was first used for search purposes with [[Foldseek]] and has since been adopted for use with [[ESM|ESM3]], [[SaProt]], and others.

#### Notes

* **Structural tokenization circumvents the inability of [[Inverse folding|inverse folding]] models to be [[ML models trained exclusively on experimental structures are less effective on computational models|effectively trained on exclusively computational models]].**

<!-- generated -->

## General

- [[Protein sequence and structure compression using VQ-VAE tokens is prone to codebook collapse]]
- [[Structural tokens improve zero-shot variant effect prediction in ESM3, but only when structures are not computationally derived]]
