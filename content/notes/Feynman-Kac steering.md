#### Summary
**Feynman-Kac steering** is a sequential Monte Carlo-based scheme for [[diffusion-guidance|guiding]] [[diffusion-models|diffusion models]] at inference time. Examples include its use in the [[alphafold3|Alphafold3]] clone [[Boltz]].

It reweights a base model using a reward,

$$
p_{\mathrm{FK}}(x_0\mid c) \propto p_\theta(x_0\mid c)\exp\!\left[\lambda r(x_0,c)\right],
$$

where $\lambda$ acts like an inverse temperature: large values concentrate particles around high-reward modes, while small values approach the unguided prior [@singhal2025]. The effective sample size,

$$
\mathrm{ESS}=\frac{\left(\sum_i w_i\right)^2}{\sum_i w_i^2},
$$

measures weight concentration from $1$ to the number of particles $k$. Resampling rules use ESS to balance reward exploitation against particle diversity. Useful gains have been reported with only a few particles [@singhal2025; @hartman2025].

#### Figures
![[Pasted image 20260413101146.png]]
*Ref [@hartman2025]*

![[Pasted image 20260413101032.png]]
*Ref [@rectorbrooks2026]*
