---
tags:
  - antibodies/misc
created: "2024-05-05T08:47:39"
modified: "2026-04-10T14:30:55"
---
#### Summary
**There is insufficient [[Antibodies|antibody]]-antigen binding data to train statistical or machine learning docking models to high accuracy, even when the data points are simulated** [^hummer2023]. Authors say at least 90,000 structures are required for prediction quality to plateau. Separately, a version of RF-diffusion fine-tuned on antibodies supplemented their structures with loop-mediated [[Protein-protein interactions|PPIs]], suggesting too few structures exist for antibody [[Protein backbone design|backbone design]] [^peng2024].

#### Details
Overfitting was avoided with 1 million synthetic measurements from FoldX on [[SAbDab]]. Authors used Ab-Bind DB, but propose replacing it with something more limited with 608 measurements. Overfitting was detected in part by placing specific [[Complementarity-determining regions|CDR]] lengths exclusively in the validation/test set, which reduced Pearson correlation.

#### See also
- [[Accurate fitness landscapes unnecessary for engineering]]

[^hummer2023]: Hummer et al. (2023) "Investigating the Volume and Diversity of Data Needed for Generalizable Antibody-Antigen ∆∆G Prediction." https://doi.org/10.1101/2023.05.17.541222
[^peng2024]: Peng et al. (2023) "Generative Diffusion Models for Antibody Design, Docking, and Optimization." https://doi.org/10.1101/2023.09.25.559190
