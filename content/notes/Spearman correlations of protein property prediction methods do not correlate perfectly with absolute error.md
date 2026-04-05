---
tags:
  - protein-folding/misc
---

#### Summary

**Spearman values of protein property prediction methods do not correlate with their mean squared errors** (Cuturello et al 2024[^cuturello2024]).

#### Figures

| Method | Pearson r | MAE | RMSE |
|---|---|---|---|
| MSAesm_ddG | **0.54** | **0.96** | **1.39** |
| PROSTATA | 0.49 | 1.00 | 1.45 |
| ACDC-NN | 0.46 | 1.05 | 1.49 |
| ACDC-NN-Seq | 0.42 | 1.08 | 1.53 |
| ThermoMPNN | 0.43 | - | 1.52 |
| DDGun3D | 0.43 | 1.11 | 1.60 |
| DDGun | 0.41 | 1.25 | 1.72 |
| PremPS | 0.41 | 1.08 | 1.50 |
| RaSP | 0.39 | 1.14 | 1.63 |
| ThermoNet | 0.39 | 1.17 | 1.62 |
| Rosetta | 0.39 | 2.08 | 2.70 |
| Dynamut | 0.41 | 1.19 | 1.60 |
| INPS3D | 0.43 | 1.07 | 1.50 |
| INPS-Seq | 0.43 | 1.09 | 1.52 |
| SDM | 0.41 | 1.26 | 1.67 |
| PoPMuSiC | 0.41 | 1.09 | 1.51 |
| MAESTRO | 0.50 | 1.06 | 1.44 |
| FoldX | 0.22 | 1.56 | 2.30 |
| DUET | 0.41 | 1.10 | 1.52 |
| I-Mutant3.0 | 0.36 | 1.12 | 1.52 |
| Dynamut2 | 0.34 | 1.15 | 1.58 |

*Table from Cuturello et al 2024[^cuturello2024]*

[^cuturello2024]: Cuturello et al. (2024) "Enhancing predictions of protein stability changes induced by single mutations using MSA-based Language Models." https://doi.org/10.1101/2024.04.11.589002
