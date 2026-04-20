---
tags:
  - protein-design/design
created: 2026-04-05T17:53:07
modified: "2026-04-20T10:13:23"
---

#### Summary

**[[Protein language models]] can be steered to design proteins with specific properties with greater success than traditional fine-tuning** [^huang2025]. The procedure involves training linear [[Binary classifiers|binary classifier]] heads on top of the activations of each layer and selecting the head with the highest validation score. Larger language models are more steerable, which contrasts with evidence against the [[Scaling hypothesis|scaling hypothesis]] of sequence-only language-only models in other domains. This was done with the [[ESM]]2-650M and ESM2-3B models.

#### Figures

| Base Model | Method | Thermostability ↑ | Thermostability Diversity ↑ | Thermostability Novelty ↑ | Solubility ↑ | Solubility Diversity ↑ | Solubility Novelty ↑ |
|---|---|---|---|---|---|---|---|
| ESM2-650M | Original Model | 56.48 (12.04) | 0.954 (0.023) | 0.591 (0.110) | 0.289 (0.151) | 0.963 (0.019) | 0.596 (0.130) |
| | Fine-tuning | 63.56 (14.87) | 0.953 (0.023) | 0.585 (0.099) | 0.356 (0.213) | 0.961 (0.020) | 0.594 (0.132) |
| | Activation Steering | **82.20 (12.92)** | **0.971 (0.023)** | **0.739 (0.130)** | **0.494 (0.241)** | **0.998 (0.001)** | **0.880 (0.087)** |
| ESM2 3B | Original Model | 56.05 (11.24) | 0.968 (0.020) | 0.632 (0.143) | 0.298 (0.174) | 0.971 (0.021) | 0.622 (0.162) |
| | Fine-tuning | 64.22 (14.49) | 0.965 (0.022) | 0.629 (0.143) | 0.385 (0.236) | 0.966 (0.022) | 0.610 (0.165) |
| | Activation Steering | **83.33 (9.47)** | **0.990 (0.006)** | **0.915 (0.105)** | **0.631 (0.228)** | **0.996 (0.003)** | **0.951 (0.077)** |

*Figure from [^huang2025]*

[^huang2025]: Huang et al. (2025) "Steering Protein Language Models." https://doi.org/10.48550/ARXIV.2509.07983
