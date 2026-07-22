---
tags:
  - protein-language-models/representations
  - thermostability/prediction
created: "2026-07-19"
modified: "2026-07-22T09:29:55"
---

#### Summary

**In ESMC-6B, the penultimate transformer representation—layer 79 of 80—is substantially more predictive of thermodynamic folding stability than the final layer.** Candido et al. fitted ridge regressions to mean-pooled representations from every layer. Performance rises through layer 79 and then drops sharply at layer 80, which is projected to the final sequence logits [@candido2026].

This is inconsistent with Adams et al., whose [[Sparse autoencoder|sparse-autoencoder]] and raw-embedding probes of the 33-layer ESM-2 650M model found thermostability prediction weakest in the middle layers and strongest again in the last layers [@adams2025]. One possible explanation is model scale and depth: ESMC-6B is much larger and deeper, with 6 billion parameters and 80 layers, so its final representation may be more specialized for masked-token prediction. The studies also differ in their targets and evaluation data—Candido et al. predict thermodynamic folding stability (ΔG) on Megascale, whereas Adams et al. predict melting temperature on the Meltome Atlas—and in their use of raw representations versus sparse-autoencoder features, so model size is not the only possible explanation.

#### See also

- [[Protein language models learn structure-level features, including disorder, in later layers]]
- [[Sparse autoencoders recover protein-family and gene-ontology features from PLM representations]]
- [[PLM pseudoperplexity stratifies stability-prediction accuracy]]
