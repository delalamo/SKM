---
title: Variational autoencoders
created: 2026-04-10T14:30:55
modified: "2026-04-20T07:16:03"
---

**Variational autoencoders** (VAEs) are neural networks that learn a [[Dimensionality reduction|reduced representation]] of a set of inputs by compressing an input signal and trying to recover it in the presence of noise. **Vector-quantized variational autoencoders** (VQ-VAEs) discretize the inputs into one-hot representations, essentially creating an alphabet (or codebook) for possible input values. These can, however, be prone to "codebook collapse" [@lu2025tokenized].
