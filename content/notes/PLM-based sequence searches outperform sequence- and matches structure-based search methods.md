---
tags:
  - tm-score
  - protein-language-models/representations
  - alignment/sequence-based
  - alignment/structure-based
created: 2025-05-19T03:43:23
modified: "2026-04-21T05:01:15"
---

## Summary

**The [[Protein language models|PLM]]-based sequence search method PLMSearch [@liu2024plmsearch] outperformed virtually all other tested sequence-based methods when querying DBs, while matching structure-based methods such as [[Foldseek]].** This includes pairs with low sequence identity (<0.3) but high structurally similarity ([[TM-score]] > 0.5). Additionally, it did so at far faster speeds using precomputed mean-pooled [[ESM]]-1b embeddings (so fixed size per protein).

## Figures

![[Pasted-image-20240416133906.png]]
*Ref [@liu2024plmsearch]*
