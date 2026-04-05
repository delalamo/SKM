---
tags:
  - protein-folding/misc
---
#### Summary
When training neural networks, **learning rate decay** is used to gradually lower the learning rate over a fixed training duration. Typically cosine decay is used, though this has the disadvantage of being carried out over a predefined duration that cannot easily be extended. Hägele et al 2024[^hgele2024] found that [[Weight averaging]] can work in tandem with this but cannot replace it.

#### Figures
![](/assets/Pasted-image-20240601062539.png)
*Figure from Hägele et al 2024[^hgele2024]*

#### Types
- Cosine decay
- Linear decay (or "trapezoidal" decay)
- Square root decay: $1-\sqrt{\frac{n-(N-N_{decay})}{n_{decay}}}$, with 5% of training steps dedicated to cooldown (Hägele et al 2024[^hgele2024])
- Schedule-free optimization

[^hgele2024]: Hägele et al. (2024) "Scaling Laws and Compute-Optimal Training Beyond Fixed Training Durations." https://doi.org/10.48550/ARXIV.2405.18392
