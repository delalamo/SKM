---
tags:
  - protein-folding/misc
created: "2025-07-22T11:37:28"
modified: "2026-04-10T14:30:55"
---
#### Summary
**Synthetic data over-represents mean values of the original data distribution and either underrepresents or exaggerates the presence of outliers** [^shumailov2023]. This can pose a challenge for models trained using [[Distillation]] and can be a cause of [[Catastrophic forgetting]].

#### Figures
\![[Pasted-image-20240216112730.png]]
*Figure from [^shumailov2023]*

#### See also
- [[Training inverse folding and diffusion models exclusively on predicted protein structures worsens performance due to how locally perfect they are]]
- [[ML models trained exclusively on experimental structures are less effective on computational models]]

[^shumailov2023]: Shumailov et al. (2023) "The Curse of Recursion: Training on Generated Data Makes Models Forget." https://doi.org/10.48550/ARXIV.2305.17493
