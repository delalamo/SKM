---
tags:
  - protein-folding/misc
created: "2024-07-15T08:36:40"
modified: "2026-04-10T14:30:55"
---
#### Summary
The **NVT ensemble** (canonical ensemble) retains number of atoms, volume, and temperature in a [[MD simulations|molecular dynamics simulation]]. It simulates at an external temperature bath at a target temperature. Spontaneous changes in NVT simulations cannot lead to increases in [[Helmholtz free energy]] [^frenkel2002].

#### Details
[^lemkul2019] note that it is common to first equilibrate temperature in an NVT ensemble before applying the barostat:

> "...it is often more robust to first equilibrate the temperature of a system before applying a barostat to control the temperature. The simultaneous combination of velocity generation and coordinate scaling under the influence of the barostat can introduce instabilities in a system that may be far from equilibrium."

Langevin dynamics is an example of an NVT ensemble [^hnin2022]:

$$d \boldsymbol{x} = M^{-1} \boldsymbol{p}\, dt \tag{1}$$
$$d \boldsymbol{p} = \left(- \nabla_{\boldsymbol{x}} U(\boldsymbol{x})- \gamma \boldsymbol{p}\right) dt + \sqrt{\frac{2 \gamma M}{\beta}} d \boldsymbol{W}_{t} \tag{2}$$

This reduces to Hamiltonian dynamics ([[NVE ensemble]]) when $\gamma = 0$.

*See [[Mathematical terms in MD]] for notation.*

[^frenkel2002]: Unknown (2002) "Understanding Molecular Simulation." https://doi.org/10.1016/B978-0-12-267351-1.X5000-7
[^lemkul2019]: Lemkul (2018) "From Proteins to Perturbed Hamiltonians: A Suite of Tutorials for the GROMACS-2018 Molecular Simulation Package [Article v1.0]." *Living Journal of Computational Molecular Science*. https://doi.org/10.33011/livecoms.1.1.5068
[^hnin2022]: Hénin et al. (2022) "Enhanced Sampling Methods for Molecular Dynamics Simulations [Article v1.0]." *Living Journal of Computational Molecular Science*. https://doi.org/10.33011/livecoms.4.1.1583
