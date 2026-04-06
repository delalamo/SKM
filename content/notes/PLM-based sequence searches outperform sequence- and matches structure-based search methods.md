---
tags:
  - protein-folding/misc
created: "2025-05-19T03:43:23"
modified: "2026-04-05T23:14:54"
---

## Summary

**The [[Protein language models|PLM]]-based sequence search method PLMSearch ([Liu et al 2024a](https://doi.org/10.1038/s41467-024-46808-5)) outperformed virtually all other tested sequence-based methods when querying DBs, while matching structure-based methods such as [[Foldseek]].** This includes pairs with low sequence identity (<0.3) but high structurally similarity ([[TM-score]] > 0.5). Additionally, it did so at far faster speeds using precomputed mean-pooled [[ESM]]-1b embeddings (so fixed size per protein).

## Figures

![](/assets/Pasted-image-20240416133906.png)
*Figure from [Liu et al 2024a](https://doi.org/10.1038/s41467-024-46808-5)*
