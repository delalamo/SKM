---
tags:
  - protein-language-models/antibodies
  - antibody-structure-prediction/cdr
created: 2026-04-05T17:38:14
modified: "2026-04-21T05:01:15"
---

#### Summary

**[[Antibody structure prediction|Predicting the structure of antibodies]] using embeddings from [[Antibodies|antibody]] [[Protein language models|language models]] leads to equal or worse performance compared to using embeddings from generic protein language models** [@lee2023solvent; @kenlay2024]. The former found that training [[IgFold]] with with [[ESM]]2-35M embeddings gave comparable performance to using the AntiBERTy embeddings used by default, while the latter obtained better performance on ABodyBuilder3 ProtT5 embeddings compared to IgBERT and IgT5.

#### Figures

| Method | Embedder | Embedder Status | Meta-arch | lDDT-Cα | OCD | H Fr | H1 | H2 | H3 | L Fr | L1 | L2 | L3 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| IgFold(paper) | | | | | 3.77 | 0.45 | 0.80 | 0.75 | 2.99 | 0.45 | 0.83 | 0.51 | 1.07 |
| IgFold(reproduced) | Antiberty(25M) | Freeze | IGFold | 0.93 | 3.74 | 0.57 | 0.92 | 0.80 | 3.09 | 0.67 | 1.12 | 0.55 | 1.15 |
| IgFold-variant1 | ESM-2(35M) | Freeze | IGFold | 0.92 | 3.76 | 0.62 | 0.87 | 0.94 | 3.06 | 0.49 | 0.90 | 0.51 | 1.15 |
| IgFold-variant2 | ESM-2(650M) | Freeze | IGFold | 0.93 | 3.77 | 0.48 | 0.91 | 0.94 | 3.20 | 0.48 | 0.94 | 0.49 | 1.13 |
| IgFold-variant3 | ESM-2(35M) | Trainable | IGFold | 0.93 | 3.88 | 0.51 | 0.89 | 0.85 | 3.14 | 0.51 | 1.00 | 0.50 | 1.10 |

*Ref [@lee2023solvent]*
