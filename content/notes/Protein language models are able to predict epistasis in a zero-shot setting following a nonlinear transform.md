---
tags:
  - protein-folding/misc
---

## Summary

**[[Protein language models]] are able to predict [[Epistasis|epistasis]] in a zero-shot setting, but must be nonlinearly transformed to achieve meaningful accuracy** ([Nambiar et al 2025](https://doi.org/10.1101/2025.09.14.676130)). This was studied using [[ESM]]2 model and showed the same [[Scaling hypothesis|scaling]] dependency observed with [[Protein property prediction using PLMs does not benefit from scale except when predicting inferring features of either structural or sparsely populated sequence families|prediction of other properties]].

## Details

Epistasis is defined as $\varepsilon^{e} = \log f^{e}_{AB} - \left( \log f^{e}_{A} + \log f^{e}_{B} \right)$ where $\log f^{e}_{AB}$ is the experimental fitness of the double mutant and $\log f^{e}_{A}$ and $\log f^{e}_{B}$ is the experimental fitness of single mutants $A$ and $B$. The nonlinear transform $\phi_{1}(x) = -\log \left( 1 + \exp \big( -b_{1}(x + c_{1}) \big) \right)$ is applied with fit parameters $b$ and $c$, with $x$ being log-likelihood predictions from the PLM, and $\phi_{1}(x)$ being the output transformed prediction.

## Figures

![](/assets/Pasted-image-20250919070445.png)
*Figure from [Nambiar et al 2025](https://doi.org/10.1101/2025.09.14.676130)*
