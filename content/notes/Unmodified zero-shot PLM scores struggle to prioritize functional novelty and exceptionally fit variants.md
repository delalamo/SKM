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

**Zero-shot [[notes/Protein language models|protein language model]] log-likelihood values penalize novelty and exceptionally fit variants** [@berry2026]. Zero-shot PLMs are mostly useful as coarse filters separating poor or unfit variants from fit variants, but do not reliably rank highly fit variants or prioritize new-to-nature functional novelty [@woolley2026].

#### Native-specificity bias
This bias can be overcome by subtracting PLM log-likelihoods from PSSM-derived log-likelihoods, as the latter reflect a broader neighborhood of extant sequences [@berry2026].

#### Figures

![[plms-poorly-rank-high-fitness-variants.png]]

![[plms-fail-functional-novelty-extrapolation.jpg]]

*Figures from [@woolley2026]*

#### See also

* [[No one-size-fits-all best approach to zero-shot or few-shot protein fitness prediction]]
* [[Protein language models are better zero-shot predictors for ranking closely related sequences than distantly related sequences]]
* [[Fitness prediction]]
* [[Unbalanced composition of sequence data prevents protein fitness from being identifiable from sequence data alone]]
