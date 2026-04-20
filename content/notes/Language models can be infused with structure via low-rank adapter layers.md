---
tags:
  - inverse-folding/evaluation
created: "2026-01-22T11:24:28"
modified: "2026-04-20T07:16:03"
---

#### Summary

**[[Protein language models]] can be converted into [[Inverse folding|inverse folding]] models by adding intermediate adapter layers and fine-tuning on structural data** ([^ruffolo2024], using [[ProGen]] models; [^li2025] using [[ESM]]2-650M). This leads to improvements in sequence recovery and [[Fitness prediction|fitness prediction]] beyond what can be achieved by concatenation. Larger models maintain the improvements in perplexity. These structures can include non-protein material if the adaptor layer allows it. This is conceptually similar to [[Low-rank Adaptation|LoRA]]. [^ruffolo2024] validate designs in the wet lab.

#### Figures

![[Pasted-image-20240918080921.png]]

*Figure from [^ruffolo2024]*

![[inverse.png]]

*Figure from [^li2025b]*

#### See also

* [[Adding structural adaptors to language models leads to improvements in thermostability prediction compared to structure-based NNs alone]]

[^ruffolo2024]: Ruffolo et al. (2024) "Adapting protein language models for structure-conditioned design." https://doi.org/10.1101/2024.08.03.606485
[^li2025]: Li & Luo (2025) "Generalizable and scalable protein stability prediction with rewired protein generative models." Nature Communications. https://doi.org/10.1038/s41467-025-67609-4
[^li2025b]: Li & Luo (2025) "Generalizable and scalable protein stability prediction with rewired protein generative models." *Nature Communications*. https://doi.org/10.1038/s41467-025-67609-4
