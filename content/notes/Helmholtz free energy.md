---
tags:
created: 2024-07-15T07:53:51
modified: "2026-04-21T05:19:34"
---
#### Summary
In [[MD simulations]], the **Helmholtz free energy** ($F$) describes "the useful work obtainable from a closed thermodynamic system at a constant temperature." It is a property of a macrostate of a system, and is proportional to the logarithm of its partition function. Frenkel & Smit [@frenkel2002] define it as a system's total energy minus the contribution of entropy ($F=E-TS$).

#### Details
$$
F \propto \beta^{-1} \ln Z_{\Sigma} \tag{1}
$$

$$
F \propto -\beta^{-1} \ln \int_{\Sigma} e^{-\beta U(\boldsymbol{x})} d \boldsymbol{x} \tag{2}
$$

Two states $A$ and $B$ with free energies $F_{A}$ and $F_{B}$ can be compared as: $\Delta F_{A,B} = \beta ^{-1} \ln \left(\frac{P_{A}}{P_{B}}\right)$

#### Reduced free energy
The definition of the reduced free energy $f$ depends on whether the simulation uses a [[NVT ensemble|canonical ensemble]] ($f= \beta F$) or an [[NPT ensemble|isothermal-isobaric ensemble]] ($f=\beta G$).

*Extensively cites [@hnin2022]*
