---
title: MD potentials from ML are more effective when protein-specific
tags:
  - conformational-dynamics/molecular-dynamics
created: "2026-04-05T18:00:02"
modified: "2026-04-11T07:27:50"
---
#### Summary
 **Potentials for [[MD simulations]] that are derived from machine learning are more effective when they are specific to each protein, rather than general-purpose** [^navarro2023]. These force fields were calculated using [[Graph neural networks]].

#### Figures
| Protein | FF-NNP Min RMSD (Å) | FF-NNP Mean RMSD (Å) | FF-NNP Macro prob. (%) | G-NNP Min RMSD (Å) | G-NNP Mean RMSD (Å) | G-NNP Macro prob. (%) |
|---|---|---|---|---|---|---|
| Chignolin | **0.3** | **0.9 ± 0.7** | **42.5 ± 0.2** | **0.2** | **1.5 ± 0.4** | **16.3 ± 0.2** |
| Trp-cage | 1.1 | 3.2 ± 1.4 | 5.5 ± 0.1 | 4.0 | 5.5 ± 0.5 | 11.0 ± 0.1 |
| BBA | **0.4** | **1.3 ± 0.7** | **30.0 ± 0.1** | **1.6** | **2.5 ± 0.4** | **42.9 ± 0.1** |
| WW-domain | **0.4** | **1.0 ± 0.6** | **1.8 ± 0.2** | 2.7 | 4.9 ± 0.9 | 4.4 ± 0.1 |
| Villin | **0.4** | **1.0 ± 0.5** | **18.6 ± 0.1** | 2.2 | 6.9 ± 1.4 | 6.9 ± 0.1 |
| NTL9 | **0.5** | **0.9 ± 0.3** | **16.0 ± 0.1** | 2.7 | 4.7 ± 0.4 | 2.9 ± 0.1 |
| BBL | **0.5** | **1.8 ± 0.6** | **4.6 ± 0.2** | 3.3 | 6.1 ± 1.3 | 17.0 ± 0.1 |
| Protein B | 4.0 | 8.6 ± 2.5 | 9.9 ± 0.1 | 4.5 | 6.6 ± 0.7 | 4.8 ± 0.1 |
| Homeodomain | 0.5 | 3.6 ± 3.9 | 35.0 ± 0.1 | 4.1 | 7.2 ± 0.9 | 7.1 ± 0.1 |
| Protein G | **0.5** | **1.0 ± 0.4** | **1.5 ± 0.1** | **1.7** | **2.8 ± 0.4** | **6.1 ± 0.1** |
| a3d | 3.4 | 8.5 ± 2.3 | 5.8 ± 0.1 | 4.1 | 7.0 ± 2.3 | 5.7 ± 0.1 |
| λ-repressor | 4.9 | 6.8 ± 1.5 | 0.4 ± 0.2 | 4.6 | 7.5 ± 1.1 | 4.9 ± 0.1 |
*Figure from [^navarro2023]*

#### See also
* [[MD simulations]]

[^navarro2023]: Navarro et al. (2023) "Top-Down Machine Learning of Coarse-Grained Protein Force Fields." *Journal of Chemical Theory and Computation*. https://doi.org/10.1021/acs.jctc.3c00638
