---
tags:
  - inverse-folding/evaluation
created: "2026-01-22T11:24:28"
modified: "2026-04-21T07:03:26"
---

#### Summary

**[[tags/protein-language-models|Protein language models]] can be converted into [[tags/inverse-folding|inverse folding]] models by adding intermediate adapter layers and fine-tuning on structural data** ([@ruffolo2024], using [[ProGen]] models; [@li2025] using [[ESM]]2-650M). This leads to improvements in sequence recovery and [[Fitness prediction|fitness prediction]] beyond what can be achieved by concatenation. Larger models maintain the improvements in perplexity. These structures can include non-protein material if the adaptor layer allows it. This is conceptually similar to [[Low-rank Adaptation|LoRA]]. [@ruffolo2024] validate designs in the wet lab.

#### Figures

![[Pasted-image-20240918080921.png]]

*Ref [@ruffolo2024]*

![[inverse.png]]

*Ref [@li2025]*

#### See also

* [[Adding structural adaptors to language models leads to improvements in thermostability prediction compared to structure-based NNs alone]]
