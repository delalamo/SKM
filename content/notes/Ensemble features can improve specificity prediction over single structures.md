---
tags:
  - prediction/binding
  - inference/feature-extraction
  - evidence/generalization
created: "2026-09-25"
modified: "2026-09-25"
---

#### Summary

**Features describing a structural ensemble can improve specificity prediction over features from a single structure** [@lyudovyk2026]. The demonstrated example is TCR–peptide–MHC classification; the general strategy is to use variation across sampled interfaces as predictive information.

#### Evidence and scope

enFoldX summarizes [[AlphaFold3]] interface and confidence features by their means and standard deviations across predicted complexes. On the evaluated TCR specificity tasks, ensemble features outperformed features from the top-ranked structure. The model achieved AUROC 0.77 on newly released epitopes; some HLA-C alleles remained difficult. Results depend on the evaluation set and how non-cognate pairs are constructed [@lyudovyk2026].

This supports [[Sequence-only TCR specificity models often struggle to generalize to unseen epitopes|a qualified account of unseen-epitope generalization]]. It does not establish that an ensemble improves every specificity task or that generated samples represent equilibrium populations.

#### Related findings

- [[Features for antibody property prediction derived from MD simulations outperform those from language models and static structures|MD-derived antibody features]] provide a related ensemble-featurization example for developability, with different sampling and prediction targets.
- [[Ensembling structure prediction methods for filtering improves recovery|Ensembling different predictors for filtering]] combines methods; enFoldX summarizes multiple samples from one predictor.
- [[Protein ensemble prediction methods do not generate conformations that are amenable to PPI docking|Difficulties docking predicted conformers]] concern a different task from classifying features of already predicted complexes.
