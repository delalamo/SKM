---
tags:
created: 2024-04-29T14:55:51
modified: "2026-04-21T05:01:15"
---
#### Summary
In the context of [[MD simulations]], the **Boltzmann distribution** in configurational space ($\nu$) and in phase space ($\mu$) is defined as:
$$\nu (\boldsymbol{x}) = \int \mu(\boldsymbol{x}, \boldsymbol{p}) d \boldsymbol{p} = \frac{1}{Z} e^{-\beta U(\boldsymbol{x})} \tag{1}$$

#### Details
In phase space, which considers both positions and momenta of atoms:
$$\mu (\boldsymbol{x}, \boldsymbol{p}) = \frac{1}{Q} e^{ - \beta (U(\boldsymbol{x})+K(\boldsymbol{p}))} \tag{2}$$

- $\boldsymbol{x}$: positions of 3D coordinates, $\boldsymbol{x} \in \mathbb{R}^{3N}$ ($N$: number of particles)
- $\boldsymbol{p}$: momenta, $\boldsymbol{p} \in \mathbb{R}^{3N}$
- $U(\boldsymbol{x})$: potential energy function
- $K(\boldsymbol{p})$: kinetic energy function
- $\beta$: inverse temperature ($\frac{1}{k_{B}T}$)
- $Z$: configurational partition function, $Z=\int e^{- \beta U(\boldsymbol{x})} d \boldsymbol{x}$
- $Q$: partition function, $Q=\int e^{- \beta (U(\boldsymbol{x})+K(\boldsymbol{p}))} d \boldsymbol{x} d \boldsymbol{p}$

*See [[Mathematical terms in MD]] for notation. Extensively cites [@hnin2022]*
