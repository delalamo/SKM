---
tags:
  - alphafold3
  - antibody-structure-prediction/complex-prediction
created: "2026-03-06T09:43:56"
modified: "2026-04-11T06:06:39"
---

#### Summary

**[[AlphaFold|AlphaFold3]] [[TM-score|ipTM]] can distinguish [[Antibodies|antibodies]] that bind and those that don't with an [[Binary classifiers|AUC]] of 0.86** [^bennett2024]. However, previous studies have not found the same for AlphaFold2-generation models [^loureno2024]. Meanwhile fine-tuned [[RosettaFold]] was also unable to distinguish these, suggesting a very high base level of performance is required to distinguish binders and nonbinders.

#### See also

- [[PAE weakly correlates with Ab-Ag binding]]
- [[Protein structure prediction and design confidence metrics do not correlate with binding affinity]]

[^bennett2024]: Bennett et al. (2024) "Atomically accurate de novo design of antibodies with RFdiffusion." https://doi.org/10.1101/2024.03.14.585103
[^loureno2024]: Lourenço et al. (2024) "Protein CREATE enables closed-loop design of de novo synthetic protein binders." https://doi.org/10.1101/2024.12.20.629847
