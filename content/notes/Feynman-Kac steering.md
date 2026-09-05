---
tags:
  - inference/guidance
  - model-design/generative-models
---
#### Summary
**Feynman-Kac steering** is a sequential Monte Carlo-based scheme for [[notes/diffusion-guidance|guiding]] [[notes/diffusion-models|diffusion models]] at inference time. Examples include its use in the [[notes/alphafold3|Alphafold3]] clone [[Boltz]].

It reweights a base model using a reward,

$$
p_{\mathrm{FK}}(x_0\mid c) \propto p_\theta(x_0\mid c)\exp\!\left[\lambda r(x_0,c)\right],
$$

where $\lambda$ acts like an inverse temperature: large values concentrate particles around high-reward modes, while small values approach the unguided prior [@singhal2025].

At scheduled intermediate steps, particles are sampled with replacement from a multinomial distribution parameterized by their normalized potential scores, duplicating high-potential trajectories before the next propagation step. The released implementation supports adaptive resampling: at candidate steps it resamples only when the [[Effective sample size|ESS]] is below $k/2$, otherwise leaving the particle population unchanged [@singhal2025]. Hartman et al. instead resample every $\Delta t$ steps beginning at a chosen $t_{\mathrm{start}}$; resampling less frequently preserves exploration, while delaying guidance until after the high-noise regime improves rewards because early reward estimates are unreliable [@hartman2025]. Useful gains have been reported with only a few particles [@singhal2025; @hartman2025].

#### Figures
![[Pasted image 20260413101146.png]]
*Ref [@hartman2025]*

![[Pasted image 20260413101032.png]]
*Ref [@rectorbrooks2026]*
