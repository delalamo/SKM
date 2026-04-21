---
tags:
created: 2024-05-05T08:47:39
modified: "2026-04-21T05:01:15"
---
#### Summary
**There is insufficient [[Antibodies|antibody]]-antigen binding data to train statistical or machine learning docking models to high accuracy, even when the data points are simulated** [@hummer2023]. Authors say at least 90,000 structures are required for prediction quality to plateau. 

#### Details
Overfitting was avoided with 1 million synthetic measurements from FoldX on [[SAbDab]]. Authors used Ab-Bind DB, but propose replacing it with something more limited with 608 measurements. Overfitting was detected in part by placing specific [[Complementarity-determining regions|CDR]] lengths exclusively in the validation/test set, which reduced Pearson correlation.

#### See also
- [[Accurate fitness landscapes are unnecessary for productively engineering enzymes or proteins]]
