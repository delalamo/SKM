---
tags:
  - model-analysis/interpretability
  - model-analysis/representation-geometry
created: "2026-01-22T12:38:44"
modified: "2026-07-28T14:12:17"
---

## Summary

**[[notes/protein-language-models|Protein language models]] encode increasingly complex biological features as representations pass through deeper layers** [@whitfield2026]. Across ESM2 and AMPLIFY models, basic physicochemical properties and linear motifs are best captured in early layers, secondary structure in subsequent layers, and domain-level semantics in middle layers. Using [[Sparse autoencoder|sparse autoencoders]], [@adams2025] likewise found that structure-level features, including [[Intrinsically disordered regions|disorder]], emerge in later layers.

## Figures

![[Non-family-specific-feature-disordered.png]]
*Ref [@adams2025]*

## See also

- [[Sparse autoencoders recover protein-family and gene-ontology features from PLM representations]]
- [[Sparse autoencoder-derived features do not outperform PLM-derived embeddings for downstream prediction]]
- [[Thermostability prediction from protein language model representations peaks in the last few layers]]
- [[Protein property prediction using PLMs does not benefit from scale except when predicting inferring features of either structural or sparsely populated sequence families]]
