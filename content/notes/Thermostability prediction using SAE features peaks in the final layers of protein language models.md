---
tags:
  - protein-language-models/representations
  - thermostability/prediction
created: "2026-07-19"
modified: "2026-07-22T09:35:52"
---

#### Summary

**Thermostability prediction using [[Sparse autoencoder|sparse-autoencoder]] features performs best with features from the final layers of a protein language model.** Adams et al. showed this in ESM-2 650M, but sampled SAE features at four-layer intervals rather than layer by layer [@adams2025]. A more granular layer-by-layer analysis of raw ESMC-6B representations found that stability prediction instead peaks at the penultimate layer, layer 79 of 80, before dropping sharply in the final layer [@candido2026].

#### See also

- [[Protein language models learn structure-level features, including disorder, in later layers]]
- [[Sparse autoencoders recover protein-family and gene-ontology features from PLM representations]]
- [[PLM pseudoperplexity stratifies stability-prediction accuracy]]
