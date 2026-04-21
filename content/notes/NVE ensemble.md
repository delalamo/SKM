---
tags:
  - conformational-dynamics/molecular-dynamics
created: "2024-07-18T02:32:12"
modified: "2026-04-21T05:01:15"
---
#### Summary
The **NVE ensemble** (microcanonical ensemble) conserves number of atoms, volume, and energy in a [[MD simulations|molecular dynamics simulation]] [@hnin2022]. It is used by classical Hamiltonian dynamics simulations under the ergodicity assumption. Use for equilibration is inadvisable since unstable/strained molecules transfer their energy to kinetic energy, leading to higher temperatures.

#### Details
General formula:
$$d \boldsymbol{x}=M^{-1} \boldsymbol{p}\, dt \tag{1}$$
$$d \boldsymbol{p}=-\nabla_{x} U(\boldsymbol{x})\, dt \tag{2}$$

Discrete time step approximation:
$$\delta \boldsymbol{x}=M^{-1} \boldsymbol{p}\,\delta t \tag{3}$$
$$\delta \boldsymbol{p}=-\nabla_{\boldsymbol{x}} U(\boldsymbol{x})\, \delta t \tag{4}$$

Total energy: $\mathcal{H}= \sum_{i=1}^{N}\frac{\mathbf{p}_{i}^{2}}{2m}+U(\mathbf{r}^{N})$

*See [[Mathematical terms in MD]] for notation. Cites [@hnin2022; @frenkel2002]*
