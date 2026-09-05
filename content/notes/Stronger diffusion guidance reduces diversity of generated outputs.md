---
tags:
  - inference/guidance
  - design/sequence-generation
created: "2026-04-10T15:35:05"
modified: "2026-07-20T09:52:04"
---

#### Summary
Stronger [[notes/Diffusion guidance|diffusion guidance]] reduces diversity of generated outputs [@yang2025; @singhal2025; @hartman2025]. This was observed in sequence generation using low-N fitness data. In [[Feynman-Kac steering]], increasing the reward weight $\lambda$ is equivalent to deprioritizing the prior distribution, and concentrates particle weights; this can collapse the sampled distribution, while low $\lambda$ recovers behavior closer to the prior.

#### Figures
![[Pasted image 20260410114222.png]]
*Ref [@yang2025]*
