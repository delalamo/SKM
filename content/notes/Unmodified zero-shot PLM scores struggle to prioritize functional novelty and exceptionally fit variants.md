---
aliases:
  - "Language models cannot extrapolate to functional novelty or ultra-high-fitness variants"
  - "notes/Language models cannot extrapolate to functional novelty or ultra-high-fitness variants"
tags:
  - evidence/generalization
  - prediction/variant-effects
  - evidence/design-validation
created: "2026-06-23"
modified: "2026-09-25"
---

#### Summary

**Unmodified zero-shot [[notes/Protein language models|protein language model]] scores struggle to prioritize functional novelty and exceptionally fit variants.** Zero-shot PLMs are mostly useful as coarse filters separating poor or unfit variants from fit variants, but do not reliably rank highly fit variants or prioritize new-to-nature functional novelty [@woolley2026].

#### Native-specificity bias

Across the SpecificityStudio assays, context-aware sequence models, particularly PLMs, tended to penalize variants with altered specificity relative to variants retaining native function [@berry2026]. This supports a limitation of the scoring objective, not an absence of useful fitness information.

Combining a context-free PSSM with a fitted zero or negative contribution from a context-aware score improved enrichment of altered-specificity variants in held-out retrospective datasets. Thus, a blanket claim that all uses of language models cannot support functional novelty is too strong. This is distinct from the [[Unbalanced composition of sequence data prevents protein fitness from being identifiable from sequence data alone|non-identifiability of fitness from sequence distributions alone]].

#### Figures

![[plms-poorly-rank-high-fitness-variants.png]]

![[plms-fail-functional-novelty-extrapolation.jpg]]

*Figures from [@woolley2026]*

#### See also

* [[No one-size-fits-all best approach to zero-shot or few-shot protein fitness prediction]]
* [[Protein language models are better zero-shot predictors for ranking closely related sequences than distantly related sequences]]
* [[Fitness prediction]]
