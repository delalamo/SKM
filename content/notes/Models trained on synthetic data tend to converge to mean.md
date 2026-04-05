---
tags:
  - protein-folding/misc
---
#### Summary
**Synthetic data over-represents mean values of the original data distribution and either underrepresents or exaggerates the presence of outliers** (Shumailov et al 2023[^shumailov2023]). This can pose a challenge for models trained using [[Distillation]] and can be a cause of [[Catastrophic forgetting]].

#### Figures
![](/assets/Pasted-image-20240216112730.png)
*Figure from Shumailov et al 2023[^shumailov2023]*

#### See also
- [[Training inverse folding and diffusion models exclusively on predicted protein structures worsens performance due to how locally perfect they are]]
- [[ML models trained exclusively on experimental structures are less effective on computational models]]

[^shumailov2023]: Shumailov et al. (2023) "The Curse of Recursion: Training on Generated Data Makes Models Forget." https://doi.org/10.48550/ARXIV.2305.17493
