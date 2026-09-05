---
tags:
  - evidence/datasets
  - design/inverse-folding
created: "2026-07-28"
modified: "2026-07-28T14:12:17"
---

#### Summary

**[[notes/Inverse folding|Inverse folding]] models favor archaeal sequence characteristics, whereas sequence-only [[notes/Protein language models|protein language models]] and [[Hybrid sequence-structure models|hybrid sequence-structure models]] favor eukaryotic sequence characteristics** [@dillon2026]. This refines the broader observation that [[PLMs are biased by uneven distribution of sequence data in datasets such as UniRef and UniProt|protein models inherit taxonomic biases from their training data]]: backbone-conditioned models organize scores primarily around compactness, packing, and charge, whereas sequence-only models retain stronger within-family taxonomic effects.

#### Figures

![[dillon2026-taxonomic-model-bias.png]]
*Backbone-conditioned models favor archaeal sequences, while sequence-only models favor eukaryotic sequences. Ref [@dillon2026]*

#### See also

- [[Unbalanced composition of sequence data prevents protein fitness from being identifiable from sequence data alone]]
- [[ESM-IF, but not other inverse folding models, has learned some evolutionary constraints from sequence databases]]
- [[Zero-shot performance of PLMs, but not inverse folding models, correlates with number of homologs available for training]]
