---
tags:
  - protein-folding/misc
---
#### Summary
**Fréchet distance** is a measure of similarity between two curves or point clouds. It was used by [[10.1101__2023.09.11.556673|Alamdari et al 2023]] to measure the similarity of designed proteins.

$$
\text{FPD} = \|\mu_{\text{test}} - \mu_{\text{gen}}\|^2 + \operatorname{Tr}\left( C_{\text{test}} + C_{\text{gen}} - 2 \sqrt{C_{\text{test}} C_{\text{gen}}} \right)
$$

$\mu$: Mean of set
$C$: Covariance matrix
$Tr$: Trace (sum of components along diagonal)
