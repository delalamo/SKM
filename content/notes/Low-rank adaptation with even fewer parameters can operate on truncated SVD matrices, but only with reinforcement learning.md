---
tags:
  - protein-folding/misc
created: "2026-03-06T11:08:59"
modified: "2026-04-10T14:30:55"
---
#### Summary
**[[Low-rank Adaptation|Low-rank adaptation]] can work with even fewer parameters than traditional LoRA, but only with [[Reinforcement learning|reinforcement learning]]** [^balazy2024][^morris2026]. Additionally, initialization of the adaptor matrices with values from SVD matrices outperforms those of random matrices.

#### Figures
\![[Pasted-image-20260306082917.png]]
\![[Pasted-image-20260306083131.png]]
*Figures from [^balazy2024]*

\![[Pasted-image-20260306083254.png]]
*Figure from [^morris2026]; SFT = supervised fine-tuning; GRPO = a type of [[Reinforcement learning|reinforcement learning]]*

[^balazy2024]: Bałazy et al. (2024) "LoRA-XS: Low-Rank Adaptation with Extremely Small Number of Parameters." https://doi.org/10.48550/ARXIV.2405.17604
[^morris2026]: Morris et al. (2026) "Learning to Reason in 13 Parameters." https://doi.org/10.48550/ARXIV.2602.04118
