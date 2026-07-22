---
tags:
  - protein-language-models/representations
  - thermostability/prediction
created: "2026-07-19"
modified: "2026-07-22T09:48:55"
---

#### Summary

**Representations from later [[protein-language-models|protein language model]] layers are most effective for thermostability prediction.** In ESMC-6B, ridge regression on raw mean-pooled representations peaked at the penultimate layer, layer 79 of 80, before dropping in the final layer [@candido2026]. Adams et al. likewise found that [[ESM|ESM-2]]-650M representations were most predictive of thermostability in later layers, although they sampled at four-layer intervals rather than layer by layer [@adams2025].

#### See also

- [[PLM pseudoperplexity stratifies stability-prediction accuracy]]
