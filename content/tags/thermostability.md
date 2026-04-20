---
title: Stability and thermostability
aliases:
  - Stability and thermostability
created: "2026-04-05T23:36:09"
modified: "2026-04-20T10:13:23"
---

**Thermostability** refers to a protein's ability to remain folded at high temperatures or under harsh conditions. It is a highly desirable property for engineered proteins.

#### Prediction

- **Phantom epistasis refers to the inclusion of unnecessary model parameters when building biophysical/statistical fitness models ([[Fitness prediction]]).** In [[10.1038__s41586-024-07966-0|Faure et al 2024]] this is attributed to Baeza-Centurion et al 2019.
- **Thermodynamic reversability can be used for expanding training sets for stability prediction/ddG prediction ML models.** However, it has been shown to lead to biases that favor WT amino acids. [[10.1101__2023.05.15.540857|Diaz et al 2023]] claim to mitigate this.
- **The amount of ddG data available for a given residue for training can be expanded using thermodynamic permutation, where $n$ measurements are increased to $n*(n-1)$.** This was used by MutComputeXGT on the [[10.1038__s41586-023-06328-6|Tsuboyama et al 2023]] dataset. It is useful for stability prediction and improves generalization in [[10.1101__2023.05.15.540857|Diaz et al 2023]].
- **ddG data is skewed with hydrophobic amino acids** (e.g., alanine scans). This has been reported to increase solvation ddG by 0.8 kcal/mol in studies cited by [[10.1101__2023.05.15.540857|Diaz et al 2023]]. The [[10.1038__s41586-023-06328-6|Tsuboyama et al 2023]] data does not have this bias.
