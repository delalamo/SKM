---
tags:
  - prediction/stability-expression
  - inference/feature-extraction
created: "2026-07-19"
modified: "2026-07-28T14:12:17"
---

#### Summary

**Representations from later [[notes/protein-language-models|protein language model]] layers are most effective for [[notes/thermostability|thermostability]] prediction.** In ESMC-6B, ridge regression on raw mean-pooled representations peaked at the penultimate layer, layer 79 of 80, before dropping significantly in the final layer [@candido2026]. Adams et al. likewise found that [[ESM|ESM-2]]-650M representations were most predictive of thermostability in the last layer, although they sampled at four-layer intervals rather than layer by layer [@adams2025].

#### See also

- [[Protein language models learn structure-level features, including disorder, in later layers]]
