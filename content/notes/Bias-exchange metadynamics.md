---
title: Bias-exchange metadynamics
created: 2026-04-10T14:30:55
modified: "2026-04-21T05:19:34"
---

**Bias-exchange metadynamics** is an [[Enhanced sampling|enhanced sampling]] method for [[MD simulations]], specifically a form of parallel-tempering [[Metadynamics|metadynamics]] intended for systems with a large number of [[Collective variables|collective variables]] (CVs). Unlike traditional metadynamics where all CVs are treated in combination, bias-exchange metadynamics runs one independent simulation per CV and swaps them randomly after a predetermined number of steps according to the Metropolis rule, similar to [[Replica-exchange molecular dynamics]].

#### Details
The swapping probability is:
$$
\min\left(1, \exp\left(\beta \left(V_{G}^{a}(X^{a}, t)+V_{G}^{a}(X^{b}, t)-V_{G}^{a}(X^{b}, t)-V_{G}^{a}(X^{a}, t)\right)\right)\right)
$$

where $x^{a}$ and $x^{b}$ are coordinates of replicas $a$ and $b$, $V_{G}^{a(b)}(x, t)$ is the metadynamics potential acting on replica $a(b)$, and $\beta$ is the inverse temperature. If the swap would decrease the biasing potential, it is accepted; otherwise, it is accepted under the Metropolis criterion.

