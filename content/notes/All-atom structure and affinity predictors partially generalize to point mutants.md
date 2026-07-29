---
tags:
  - alphafold3
  - variant-effect-prediction
created: "2026-07-28"
modified: "2026-07-28T14:12:17"
---

#### Summary

**All-atom structure-and-affinity predictors partially generalize from wild-type protein-drug binding to the effects of [[variant-effect-prediction|point mutations]], but mutant predictions are less accurate** [@ngo2026]. Across hERG, NaV1.5, HER2, and CYP3A4, [[alphafold3|Boltz-2]] affinity predictions reached Pearson correlations with experimental IC50 values of up to 0.76 for wild-type proteins and 0.60 for mutants.

The evaluation compared the default setting of 200 diffusion steps and five samples with increased-sampling settings of 300 steps and seven samples or 400 steps and nine samples.

#### Figures

![[ngo2026-boltzomics-wildtype-mutant-performance.png]]
![[ngo2026-boltzomics-sampling-settings.png]]
*Settings 0, 1, and 2 have 200, 300, and 400 diffusion steps and 5, 7, and 9 samples . Ref [@ngo2026]*

#### See also

- [[AF3 binding affinity predictions are orthogonal to those made by force fields and other neural networks]]
- [[The Boltz-2 affinity module cannot be effectively repurposed for PPI affinity prediction]]
- [[Structure-based methods outperform sequence-based methods at zero-shot prediction of binding, whereas the reverse is true for zero-shot prediction of enzymatic activity]]
- [[Increasing diffusion samples is sufficient to yield correctly predicted antibody-antigen complexes]]
- [[Large-scale measurements, such as Kd and IC50, from different assays correlate weakly in different studies]]
