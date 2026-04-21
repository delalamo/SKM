---
tags:
  - conformational-dynamics/molecular-dynamics
created: "2024-07-18T02:32:12"
modified: "2026-04-21T05:19:34"
---
#### Summary
The **NVE ensemble** (microcanonical ensemble) conserves number of atoms, volume, and energy in a [[MD simulations|molecular dynamics simulation]] [^hnin2022]. It is used by classical Hamiltonian dynamics simulations under the ergodicity assumption. Use for equilibration is inadvisable since unstable/strained molecules transfer their energy to kinetic energy, leading to higher temperatures.

#### Details
General formula:
$$
d \boldsymbol{x}=M^{-1} \boldsymbol{p}\, dt \tag{1}
$$

$$
d \boldsymbol{p}=-\nabla_{x} U(\boldsymbol{x})\, dt \tag{2}
$$

Discrete time step approximation:
$$
\delta \boldsymbol{x}=M^{-1} \boldsymbol{p}\,\delta t \tag{3}
$$

$$
\delta \boldsymbol{p}=-\nabla_{\boldsymbol{x}} U(\boldsymbol{x})\, \delta t \tag{4}
$$

Total energy: $\mathcal{H}= \sum_{i=1}^{N}\frac{\mathbf{p}_{i}^{2}}{2m}+U(\mathbf{r}^{N})$

*See [[Mathematical terms in MD]] for notation. Cites [^hnin2022] and [^frenkel2002]*

[^hnin2022]: Hénin et al. (2022) "Enhanced Sampling Methods for Molecular Dynamics Simulations [Article v1.0]." *Living Journal of Computational Molecular Science*. https://doi.org/10.33011/livecoms.4.1.1583
[^frenkel2002]: Unknown (2002) "Understanding Molecular Simulation." https://doi.org/10.1016/B978-0-12-267351-1.X5000-7
