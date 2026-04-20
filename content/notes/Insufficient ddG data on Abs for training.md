---
tags:
created: 2024-05-05T08:47:39
modified: "2026-04-20T07:16:03"
---
#### Summary
**There is insufficient [[Antibodies|antibody]]-antigen binding data to train statistical or machine learning docking models to high accuracy, even when the data points are simulated** [^hummer2023]. Authors say at least 90,000 structures are required for prediction quality to plateau. 

#### Details
Overfitting was avoided with 1 million synthetic measurements from FoldX on [[SAbDab]]. Authors used Ab-Bind DB, but propose replacing it with something more limited with 608 measurements. Overfitting was detected in part by placing specific [[Complementarity-determining regions|CDR]] lengths exclusively in the validation/test set, which reduced Pearson correlation.

#### See also
- [[Accurate fitness landscapes are unnecessary for productively engineering enzymes or proteins]]

[^hummer2023]: Hummer et al. (2025) "Investigating the volume and diversity of data needed for generalizable antibody–antigen ΔΔG prediction." Nature Computational Science. https://doi.org/10.1038/s43588-025-00823-8
