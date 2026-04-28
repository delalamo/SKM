---
tags:
  - alphafold3
  - structure-prediction/complex-prediction
  - tm-score
  - confidence-metrics
created: 2026-03-06T09:43:56
modified: "2026-04-28T09:20:09"
---

#### Summary

**[[alphafold3|AlphaFold3]] [[tm-score|ipTM]] can distinguish [[antibodies|antibodies]] that bind and those that don't with an [[Binary classifiers|AUC]] of 0.86** [@bennett2024]. This was corroborated in one subsequent prospective study[@sang2026], whereas another study found this to be target-dependent[@harvey2026] (see figure below for details). However, previous studies have not found the same for AlphaFold2-generation models [@loureno2024]. Meanwhile fine-tuned [[rosettafold|RosettaFold]] was also unable to distinguish these, suggesting a very high base level of performance is required to distinguish binders and nonbinders.

#### Figures
![[auroc_af3_ab_ag_iptm.png]]
*Ref[@harvey2026]*

#### See also
- [[PAE weakly correlates with Ab-Ag binding]]
- [[Protein structure prediction and design confidence metrics do not correlate with binding affinity]]
