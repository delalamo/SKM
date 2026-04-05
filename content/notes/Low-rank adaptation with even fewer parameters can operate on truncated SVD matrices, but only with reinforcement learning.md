---
tags:
  - protein-folding/misc
---
#### Summary
**[[Low-rank Adaptation|Low-rank adaptation]] can work with even fewer parameters than traditional LoRA, but only with [[Reinforcement learning|reinforcement learning]]** (Balazy et al 2024[^balazy2024], Morris et al 2026[^morris2026]). Additionally, initialization of the adaptor matrices with values from SVD matrices outperforms those of random matrices.

#### Figures
![](/assets/Pasted-image-20260306082917.png)
![](/assets/Pasted-image-20260306083131.png)
*Figures from Balazy et al 2024[^balazy2024]*

![](/assets/Pasted-image-20260306083254.png)
*Figure from Morris et al 2026[^morris2026]; SFT = supervised fine-tuning; GRPO = a type of [[Reinforcement learning|reinforcement learning]]*

[^balazy2024]: Bałazy et al. (2024) "LoRA-XS: Low-Rank Adaptation with Extremely Small Number of Parameters." https://doi.org/10.48550/ARXIV.2405.17604
[^morris2026]: Morris et al. (2026) "Learning to Reason in 13 Parameters." https://doi.org/10.48550/ARXIV.2602.04118
