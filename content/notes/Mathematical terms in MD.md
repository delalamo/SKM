---
tags:
  - conformational-dynamics/molecular-dynamics
created: "2024-04-16T22:58:57"
modified: "2026-04-21T05:01:15"
---
#### Summary
Notation follows the convention of [@hnin2022].

- $\boldsymbol{x}$: positions of 3D coordinates, $\boldsymbol{x} \in \mathbb{R}^{3N}$ ($N$: number of particles)
- $\boldsymbol{p}$: momenta, $\boldsymbol{p} \in \mathbb{R}^{3N}$
- $\beta$: inverse temperature ($\frac{1}{k_{B}T}$)
- $Q$: partition function or normalization factor, $Q=\int e^{- \beta (U(\boldsymbol{x})+K(\boldsymbol{p}))}$
- $M$: diagonal mass matrix
- $W_{t}$: Brownian motion in dimension $3N$

#### Energy terms

- $U(\boldsymbol{x})$: potential energy function
- $u_{i}(\boldsymbol{X})$: reduced energy function for state $i$, defined as $u_{i}(\boldsymbol{x}) = \beta_{i} (U_{i} (\boldsymbol{x}) + p_{i}V(\boldsymbol{x}))$
- $p_{i}V(\boldsymbol{x})$: pressure-volume term, only included in constant-pressure ensembles (e.g., [[NPT ensemble]]); $p_{i}$ is the external pressure
- $K(\boldsymbol{p})$: kinetic energy function
- $F$: [[Helmholtz free energy]]
- $S$: entropy, $S= k_{B} \ln \Omega$
- $\Omega (E)$: density of states with specific total energy $E$, $\int \delta (E - H(\boldsymbol{x}, \boldsymbol{p})) d \boldsymbol{x} d \boldsymbol{p}$
- $\Omega (U)$: configurational density with specific potential energy $U$, $\int \delta (U-U(\boldsymbol{x}))d \boldsymbol{x}$
