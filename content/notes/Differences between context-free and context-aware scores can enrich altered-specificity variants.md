---
tags:
  - prediction/variant-effects
  - design/directed-evolution
  - evidence/generalization
created: "2026-09-25"
modified: "2026-09-25"
---

#### Summary

**Differences between context-free and context-aware sequence scores can enrich variants with altered specificity** [@berry2026]. Disagreement can be informative when the objective is to change function rather than preserve the native sequence's preferences.

#### Details

SpecificityStudio combines a context-free PSSM with a fitted contribution from a context-aware model such as ESM-1v. Zero or negative context-aware weights can improve enrichment of specificity-changing variants compared with using the context-aware score alone. The weights were calibrated on other datasets, with leave-one-dataset-out evaluation.

This is retrospective enrichment in measured datasets, not a prospective experimental demonstration of a new design campaign. It also does not establish that broad functional diversity in the homolog alignment causes the improvement.

The result qualifies the [[Language models cannot extrapolate to functional novelty or ultra-high-fitness variants|native-function bias of unmodified zero-shot scores]]. It addresses a different objective from [[Averaging logits from multiple sources can improve fitness prediction|positively averaging model scores for conventional fitness prediction]].

#### See also

- [[Potts models and PSSMs can model fitness landscapes]]
- [[Unbalanced composition of sequence data prevents protein fitness from being identifiable from sequence data alone]]
