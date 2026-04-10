---
title: Multi-sequence protein language models
tags:
  - multi-sequence-protein-language-models
---

Multi-sequence [[Protein language models|protein language models]] use a context of related sequences, either through [[Multiple sequence alignments|multiple sequence alignments]] or through unaligned sequences pre-pended to the query.

#### Models

**Alignment-based**, which essentially treat the input as a 2D sequence
* [[MSA Transformer]]
* [[ProteinNPT]]
* [[Evoformer]]

**Alignment-free**, which pre-pends the homologous sequences to the query that is being subject to inference.
* ProFam1
* Dayhoff
* [[10.1093__bioinformatics__btaf348|ProtMamba]]

#### Notes

* [[Variant effect prediction with homology-aware PLMs improves with ensembling of multiple prompts]]

<!-- generated -->
