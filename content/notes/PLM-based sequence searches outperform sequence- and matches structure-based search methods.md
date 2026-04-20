---
tags:
  - tm-score
  - protein-language-models/representations
created: 2025-05-19T03:43:23
modified: "2026-04-20T10:13:23"
---

## Summary

**The [[Protein language models|PLM]]-based sequence search method PLMSearch ([Liu et al 2024a][^liu2024]) outperformed virtually all other tested sequence-based methods when querying DBs, while matching structure-based methods such as [[Foldseek]].** This includes pairs with low sequence identity (<0.3) but high structurally similarity ([[TM-score]] > 0.5). Additionally, it did so at far faster speeds using precomputed mean-pooled [[ESM]]-1b embeddings (so fixed size per protein).

## Figures

![[Pasted-image-20240416133906.png]]
*Figure from [Liu et al 2024a][^liu2024]*

[^liu2024]: Liu et al. (2024) "PLMSearch: Protein language model powers accurate and fast sequence search for remote homology." *Nature Communications*. https://doi.org/10.1038/s41467-024-46808-5
