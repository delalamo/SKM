---
tags:
created: 2024-07-15T07:53:51
modified: "2026-04-20T10:13:23"
---
#### Summary
In [[MD simulations]], the **Helmholtz free energy** ($F$) describes "the useful work obtainable from a closed thermodynamic system at a constant temperature." It is a property of a macrostate of a system, and is proportional to the logarithm of its partition function. Frenkel & Smit[^frenkel] define it as a system's total energy minus the contribution of entropy ($F=E-TS$).

#### Details
$$F \propto \beta^{-1} \ln Z_{\Sigma} \tag{1}$$
$$F \propto -\beta^{-1} \ln \int_{\Sigma} e^{-\beta U(\boldsymbol{x})} d \boldsymbol{x} \tag{2}$$

Two states $A$ and $B$ with free energies $F_{A}$ and $F_{B}$ can be compared as: $\Delta F_{A,B} = \beta ^{-1} \ln \left(\frac{P_{A}}{P_{B}}\right)$

#### Reduced free energy
The definition of the reduced free energy $f$ depends on whether the simulation uses a [[NVT ensemble|canonical ensemble]] ($f= \beta F$) or an [[NPT ensemble|isothermal-isobaric ensemble]] ($f=\beta G$).

*Extensively cites [^hnin2022]*

[^frenkel]: Unknown (2002) "Understanding Molecular Simulation." https://doi.org/10.1016/B978-0-12-267351-1.X5000-7
[^hnin2022]: Hénin et al. (2022) "Enhanced Sampling Methods for Molecular Dynamics Simulations [Article v1.0]." *Living Journal of Computational Molecular Science*. https://doi.org/10.33011/livecoms.4.1.1583
