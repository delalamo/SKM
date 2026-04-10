---
tags:
  - protein-folding/misc
created: "2024-11-04T23:57:57"
modified: "2024-11-04T23:57:57"
---
#### Summary
**Fréchet distance** is a measure of similarity between two curves or point clouds. It was used by [^alamdari2023] to measure the similarity of designed proteins.

$$
\text{FPD} = \|\mu_{\text{test}} - \mu_{\text{gen}}\|^2 + \operatorname{Tr}\left( C_{\text{test}} + C_{\text{gen}} - 2 \sqrt{C_{\text{test}} C_{\text{gen}}} \right)
$$

$\mu$: Mean of set
$C$: Covariance matrix
$Tr$: Trace (sum of components along diagonal)

[^alamdari2023]: Alamdari et al. (2023) "Protein generation with evolutionary diffusion: sequence is all you need." https://doi.org/10.1101/2023.09.11.556673
