---
title: Replica-exchange molecular dynamics
created: 2026-04-10T14:30:55
modified: "2026-04-21T05:19:34"
---

**Replica-exchange [[MD simulations|MD simulations]]** execute multiple versions of the same molecule in parallel, at different conditions (typically different temperatures). This is motivated by using a "ladder" of simulations to connect a target low-temperature distribution with a high-temperature, easier-to-sample distribution, accelerating sampling of the former ([[10.1021__acs.jpclett.2c03327|Invernizzi et al 2022]]).

#### Details
For a set of $M+1$ replicas ranging from $p_{0}(\textbf{x}) = p(\textbf{x})$ to $p_{M}(\textbf{x}) = q(\textbf{x})$, each replica $i$ has $u_{i}(\textbf{x}) = (k_{B}T_{i})^{-1}U(\textbf{x})$ where $U(\textbf{x})$ is the potential energy and $T_{i}$ interpolates between $T_{0}$ and $T_{M}$. Total replicas $M$ scales as $M \propto \sqrt{N}$ with system degrees of freedom.

Configurations $\textbf{x}_{i}$ and $\textbf{x}_{j}$ are exchanged with probability:
$$
\alpha_{REX} = \min \left\{1, \exp\left(\Delta u_{ij}(\textbf{x}_{i})-\Delta u_{ij}(\textbf{x}_{j})\right)\right\}
$$

$$
\Delta u_{ij}(\textbf{x}) = u_{i}(\textbf{x}) - u_{j}(\textbf{x})
$$

