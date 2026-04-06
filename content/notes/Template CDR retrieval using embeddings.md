---
tags:
  - antibodies/misc
created: "2026-04-05T17:15:06"
modified: "2026-04-05T23:14:54"
---
#### Summary
**[[Complementarity-determining regions|CDR]] templates with high structural similarity can be fetched by comparing the embeddings to those of templates in the PDB, fetching the top ten, and taking the medoid by Euclidean distance** (Singh et al 2023[^singh2023]). This strategy was found to be more accurate than either DeepAb and [[AlphaFold|AlphaFold2]]. On [[Complementarity-determining regions#CDRH3|CDRH3]] it was more accurate than [[OmegaFold]], while on other CDRs it was about the same (results only show the LSTM model after fine-tuning, not the other two).

#### Figures
| Model | Metric | Chain | CDR 1 | CDR 2 | CDR 3 | Whole Fv |
|---|---|---|---|---|---|---|
| AbMAP-B | TM-Score | H | **0.62** ± 0.007 | **0.67** ± 0.006 | **0.54** ± 0.007 | **0.86** ± 0.006 |
| ProtBert | TM-Score | H | 0.33 ± 0.003 | 0.31 ± 0.003 | 0.28 ± 0.003 | 0.69 ± 0.005 |
| ESM-1b | TM-Score | H | 0.49 ± 0.007 | 0.51 ± 0.006 | 0.44 ± 0.007 | 0.79 ± 0.004 |
| DeepAb | TM-Score | H | 0.51 ± 0.008 | 0.55 ± 0.008 | 0.24 ± 0.004 | 0.54 ± 0.005 |
| OmegaFold | TM-Score | H | 0.61 ± 0.007 | **0.67** ± 0.006 | 0.34 ± 0.005 | 0.79 ± 0.005 |
| AlphaFold2 | TM-Score | H | 0.28 ± 0.003 | 0.30 ± 0.003 | 0.30 ± 0.004 | 0.65 ± 0.004 |
| AbMAP-B | TM-Score | L | 0.62 ± 0.007 | **0.76** ± 0.007 | **0.65** ± 0.007 | **0.89** ± 0.004 |
| ProtBert | TM-Score | L | 0.34 ± 0.003 | 0.60 ± 0.007 | 0.52 ± 0.010 | 0.80 ± 0.005 |
| ESM-1b | TM-Score | L | 0.41 ± 0.005 | 0.61 ± 0.007 | 0.39 ± 0.005 | 0.82 ± 0.004 |
| DeepAb | TM-Score | L | 0.40 ± 0.006 | 0.66 ± 0.009 | 0.38 ± 0.006 | 0.52 ± 0.005 |
| OmegaFold | TM-Score | L | **0.63** ± 0.006 | 0.69 ± 0.006 | 0.58 ± 0.006 | 0.83 ± 0.005 |
| AlphaFold2 | TM-Score | L | 0.27 ± 0.003 | 0.36 ± 0.007 | 0.31 ± 0.003 | 0.58 ± 0.004 |
| AbMAP-B | RMSD | H | 0.43 ± 0.016 | 0.38 ± 0.013 | **0.43** ± 0.025 | 2.11 ± 0.082 |
| ProtBert | RMSD | H | 1.40 ± 0.030 | 1.21 ± 0.028 | 0.64 ± 0.031 | 3.07 ± 0.078 |
| ESM-1b | RMSD | H | 0.54 ± 0.017 | 0.76 ± 0.022 | 0.50 ± 0.023 | 2.69 ± 0.063 |
| DeepAb | RMSD | H | 0.56 ± 0.016 | 0.55 ± 0.015 | 0.81 ± 0.031 | **0.72** ± 0.028 |
| OmegaFold | RMSD | H | **0.35** ± 0.013 | **0.37** ± 0.013 | 0.75 ± 0.035 | 2.39 ± 0.067 |
| AlphaFold2 | RMSD | H | 0.70 ± 0.032 | **0.37** ± 0.030 | 1.24 ± 0.063 | 4.40 ± 0.077 |
| AbMAP-B | RMSD | L | 0.41 ± 0.015 | 0.18 ± 0.006 | **0.44** ± 0.022 | 1.42 ± 0.044 |
| ProtBert | RMSD | L | 1.39 ± 0.041 | **0.15** ± 0.008 | 0.64 ± 0.044 | **0.76** ± 0.012 |
| ESM-1b | RMSD | L | 0.68 ± 0.022 | 0.22 ± 0.008 | 0.65 ± 0.028 | 2.38 ± 0.062 |
| DeepAb | RMSD | L | 0.72 ± 0.021 | 0.32 ± 0.011 | 0.84 ± 0.030 | 1.16 ± 0.084 |
| OmegaFold | RMSD | L | **0.40** ± 0.016 | 0.17 ± 0.007 | 0.46 ± 0.017 | 2.31 ± 0.076 |
| AlphaFold2 | RMSD | L | 1.13 ± 0.046 | 0.24 ± 0.024 | 0.64 ± 0.033 | 4.79 ± 0.084 |

From Singh et al 2023[^singh2023]

#### See also
- [[CDR representations segregate into distinct clusters]]
- [[Contrastive learning on whole structures leads to learning of substructures]]

[^singh2023]: Singh et al. (2023) "Learning the Language of Antibody Hypervariability." https://doi.org/10.1101/2023.04.26.538476
