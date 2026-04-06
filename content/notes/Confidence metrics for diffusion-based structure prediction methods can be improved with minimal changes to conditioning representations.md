---
tags:
  - protein-folding/misc
created: "2026-03-06T09:43:56"
modified: "2026-04-05T23:14:54"
---

#### Summary

**Confidence metrics like ipTM from diffusion-based protein structure prediction can be improved with relatively small changes in the conditioning probabilities** (Maddipatla et al 2026[^maddipatla2026]). This was observed when using this as an objective for diffusion guidance.

#### Figures

![](/assets/Pasted-image-20260306093812.png)

*Figure from Maddipatla et al 2026[^maddipatla2026]*

#### See also

- [[Diffusion-based structure prediction can be steered by modifying the conditioning embeddings rather than the latent space, and such embeddings can be used for subsequent iterations]]
- [[Protein structure prediction and design metrics don't correlate with expression probability]]
- [[Sequence- and structure-derived ML quality metrics from ML do not correlate with each other]]
- [[pLDDT correlates with number of homologous sequences provided during runtime]]
- [[Protein structure prediction and design confidence metrics do not correlate with binding affinity]]
- [[Protein folding neural networks cannot predict protein stability]]

[^maddipatla2026]: Maddipatla et al. (2026) "Inference-time optimization for experiment-grounded protein ensemble generation." https://doi.org/10.48550/ARXIV.2602.24007
