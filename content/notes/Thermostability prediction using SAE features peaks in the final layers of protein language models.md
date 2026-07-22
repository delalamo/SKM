---
tags:
  - protein-language-models/representations
  - thermostability/prediction
created: "2026-07-19"
modified: "2026-07-22T09:45:09"
---

#### Summary

**Thermostability prediction using [[Sparse autoencoder|sparse-autoencoder]] features performs best with features from the final layers of a protein language model** [@adams2025]. This was shown in [[ESM|ESM-2]]-650M, where the last layer was best (albeit probing every four layers). A more granular layer-by-layer analysis of raw ESMC-6B representations similarly found that the penultimate layer, layer 79 of 80, was best [@candido2026].

#### See also

- [[Protein language models learn structure-level features, including disorder, in later layers]]
- [[Sparse autoencoders recover protein-family and gene-ontology features from PLM representations]]
- [[PLM pseudoperplexity stratifies stability-prediction accuracy]]
