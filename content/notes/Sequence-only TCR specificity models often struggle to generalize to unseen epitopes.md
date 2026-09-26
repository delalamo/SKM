---
aliases:
  - "Deep learning methods cannot generalize T-cell receptor binding to new epitopes"
  - "notes/Deep learning methods cannot generalize T-cell receptor binding to new epitopes"
tags:
  - evidence/generalization
  - prediction/binding
created: 2024-05-18T08:35:46
modified: "2026-09-25"
---

#### Summary

**Sequence-only specificity predictors for [[T-cell receptors]] often struggle when test epitopes differ from those in training.** The earlier evaluation found strong dependence on epitope similarity [@groce2023]. This is evidence about the tested predictors and splits, rather than an impossibility result for all deep-learning approaches.

[[Ensemble features can improve specificity prediction over single structures|Structure-ensemble features provide a counterexample]]: enFoldX generalized to unseen epitopes, although performance depended on the dataset and HLA allele [@lyudovyk2026]. Extending either conclusion to [[B-cell receptors]] or [[tags/antibodies|antibodies]] requires evidence for those systems.

#### See also
* [[DL models excel at finding pockets but not docking into them]]
* [[DL structure prediction methods cannot predict CDR conformations unseen during training]]
