---
tags:
  - protein-design/misc
---

#### Summary

**[[Protein language models]] can be converted into [[Inverse folding|inverse folding]] models by adding intermediate adapter layers and fine-tuning on structural data** (Ruffolo et al 2024b[^ruffolo2024], using [[ProGen]] models; Li et al 2025b[^li2025] using [[ESM]]2-650M). This leads to improvements in sequence recovery and [[Fitness prediction|fitness prediction]] beyond what can be achieved by concatenation. Larger models maintain the improvements in perplexity. These structures can include non-protein material if the adaptor layer allows it. This is conceptually similar to [[Low-rank Adaptation|LoRA]]. Ruffolo et al 2024b[^ruffolo2024] validate designs in the wet lab.

#### Figures

![](/assets/Pasted-image-20240918080921.png)

*Figure from Ruffolo et al 2024b[^ruffolo2024]*

![](/assets/inverse.png)

*Figure from Li et al 2025[^li2025b]*

#### See also

* [[Adding structural adaptors to language models leads to improvements in thermostability prediction compared to structure-based NNs alone]]

[^ruffolo2024]: Ruffolo et al. (2024) "Adapting protein language models for structure-conditioned design." https://doi.org/10.1101/2024.08.03.606485
[^li2025]: Li & Luo (2025) "Generalizable and scalable protein stability prediction with rewired protein generative models." https://doi.org/10.1101/2025.02.13.638154
[^li2025b]: Li & Luo (2025) "Generalizable and scalable protein stability prediction with rewired protein generative models." *Nature Communications*. https://doi.org/10.1038/s41467-025-67609-4
