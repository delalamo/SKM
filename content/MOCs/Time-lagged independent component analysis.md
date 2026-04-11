---
title: Time-lagged independent component analysis
tags:
  - time-lagged-independent-component-analysis
created: "2026-04-10T14:02:57"
modified: "2026-04-11T07:41:30"
---

**Time-lagged independent component analysis** (tICA) is a [[Dimensionality reduction|dimensionality reduction]] tool for finding the slowest modes of motion in [[MD simulations]] ([[10.1021__ct300878a|Schwantes & Pande 2013]], [[10.1063__1.4811489|Pérez-Hernández et al 2013]]). In contrast with PCA, which finds directions of maximal variance, tICA finds the rarest events. This is useful when building [[Markov State Models]]. Some studies have used independent components as [[Collective variables|collective variables]] for [[Metadynamics|metadynamics]] simulations.

#### Details
1. Two covariance matrices, $\mathbf{C}(0)$ and $\mathbf{C}(\tau)$, are constructed from the MD data, where $\tau$ is a user-defined time lag.
2. $\mathbf{C}(\tau)$ is symmetrized: $\mathbf{C}(\tau)=\frac{ \mathbf{C}_{d} (\tau) + \mathbf{C}^{T}_{d} (\tau)}{2}$
3. Generalized eigenvalue problem is solved: $\mathbf{C}(\tau) \mathbf{U} = \mathbf{C}(0) \mathbf{U} \mathbf{\Lambda}$
4. Projection onto tICA space via a sub-matrix of $\mathbf{U}$: $\mathbf{z}^{T} (t) = \mathbf{r}^{T} \mathbf{U}$

#### Figures
![[unknown.png]]
*Figure from [http://docs.markovmodel.org/lecture_tica.html](http://docs.markovmodel.org/lecture_tica.html)*

<!-- generated -->
