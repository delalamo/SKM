---
tags:
  - protein-language-models/representations
  - thermostability/prediction
created: "2026-07-19"
modified: "2026-07-22T09:35:52"
---

#### Summary

**Thermostability prediction using [[Sparse autoencoder|sparse-autoencoder]] features performs best with features from the final layers of a protein language model** [@candido2026; @adams2025]. This was shown in ESM-C-6B, where layer 79 out of 80 was substantially better, and [[ESM-2]]-650M, where the last layer was best (albeit probing every four layers).

#### See also

- [[Protein language models learn structure-level features, including disorder, in later layers]]
- [[Sparse autoencoders recover protein-family and gene-ontology features from PLM representations]]
- [[PLM pseudoperplexity stratifies stability-prediction accuracy]]
