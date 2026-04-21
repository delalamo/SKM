---
tags:
  - inverse-folding/training
created: 2026-04-05T17:47:00
modified: "2026-04-21T07:28:09"
---

#### Summary

**Using evolutionary information for label smoothing when training [[inverse-folding|inverse folding]] models improves [[variant-effect-prediction|variant effect prediction]].** Zhou et al. used the [[blosum62|BLOSUM62]] matrix, whereas Gong et al. [@gong2024] used PSSMs. By contrast, Dauparas et al. used uniform smoothing [@zhou2024; @dauparas2022].

#### Details

Zhou et al. use a temperature value $t$ to balance the contribution of the WT amino acid and the BLOSUM62 matrix - the figure below defines this as $\mathbf{B}' = \sigma (\mathbf{B})^{t}$ where $\mathbf{B}'$ and $\mathbf{B}$ are the target matrices and BLOSUM matrices, respectively, and $\sigma$ is a nonlinear operator. [@zhou2024]

In contrast, Gong et al. [@gong2024] calculated propensities from [[Multiple sequence alignments|MSAs]].

#### Figures

![[Pasted-image-20240430090828.png]]

*Figure S7 from [@zhou2024]*

| Method | T2837 ρ↑ | T2837 AUC↑ | S669 ρ↑ | S669 AUC↑ | S-Sym ρ↑ | S-Sym AUC↑ | Myolobin ρ↑ | Myolobin AUC↑ | FireProtDB ρ↑ | FireProtDB AUC↑ | Gβ1 ρ↑ | Gβ1 AUC↑ | T2837 Reverse ρ↑ | T2837 Reverse AUC↑ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **# Mutations** | 2837 | | 669 | | 342 | | 134 | | 1764 | | 935 | | 2837 | |
| RaSP* (Blaabjerg et al., 2023) | 0.58 | 0.61 | 0.39 | 0.69 | 0.64 | 0.73 | **0.68** | 0.75 | 0.56 | 0.71 | **0.72** | 0.66 | 0.23 | 0.59 |
| ThermoMPNN* (Dieckhaus et al., 2023) | 0.55 | 0.78 | 0.39 | 0.68 | 0.66 | 0.82 | 0.58 | 0.77 | 0.57 | 0.75 | 0.65 | 0.78 | 0.43 | 0.71 |
| Prostata-IFML (Diaz et al., 2023) | 0.53 | 0.75 | 0.49 | 0.76 | 0.55 | 0.75 | 0.54 | 0.67 | - | - | 0.66 | **0.82** | 0.52 | 0.75 |
| Stability Oracle (Diaz et al., 2023) | **0.59** | **0.81** | **0.52** | **0.74** | **0.72** | **0.87** | **0.68** | **0.81** | **0.61** | **0.79** | 0.71 | **0.82** | **0.59** | **0.81** |
| ESM2* (Lin et al., 2023) | 0.28 | 0.60 | 0.04 | 0.50 | 0.26 | 0.56 | 0.15 | 0.57 | 0.25 | 0.57 | 0.25 | 0.63 | 0.28 | 0.60 |
| ProteinMPNN* (Dauparas et al., 2022) | 0.36 | 0.70 | 0.25 | 0.59 | 0.32 | 0.64 | 0.35 | 0.66 | 0.31 | 0.70 | 0.35 | 0.67 | 0.36 | 0.70 |
| MutComputeXGT (Diaz et al., 2023) | 0.34 | 0.68 | 0.27 | 0.57 | 0.38 | 0.72 | 0.37 | 0.72 | 0.30 | 0.69 | 0.34 | 0.66 | 0.34 | 0.68 |
| MutComputeXGT w/ MSA soft-label (Ours) | 0.37 | 0.70 | 0.30 | 0.59 | 0.48 | 0.75 | 0.45 | 0.75 | 0.36 | 0.71 | 0.41 | 0.69 | 0.37 | 0.70 |
| MutRank (Ours) | **0.51** | **0.78** | **0.40** | **0.67** | **0.62** | **0.84** | **0.68** | **0.84** | **0.51** | **0.77** | **0.62** | **0.77** | **0.51** | **0.78** |
| SSL Improvement ↑ | 42% | 11% | 48% | 14% | 63% | 17% | 83% | 17% | 65% | 10% | 77% | 15% | 42% | 11% |
| Supervised Fine-Tuning Gap ↓ | 14% | 4% | 23% | 9% | 14% | 3% | 0% | -4% | 16% | 3% | 13% | 3% | 14% | 4% |

*Table 3 from [@gong2024]*

#### Publication history

22 March 2026: https://biomlzk.ghost.io/training-inverse-folding-models-with-evolutionary-information-improves-fitness-prediction-performance/
