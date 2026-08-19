---
tags:
  - protein-language-models
  - variant-effect-prediction
  - fitness-prediction
title: Zero-shot protein language models do not reliably extrapolate to functional novelty
created: "2026-06-23"
modified: "2026-08-19T16:32:04"
---

#### Summary

**Zero-shot [[protein-language-models|protein language models]] do not reliably extrapolate to functional novelty or ultra-high-fitness variants.** They are mostly useful as coarse filters separating poor or unfit variants from fit variants, but do not reliably rank highly fit variants or prioritize new-to-nature functions [@woolley2026]. This does not preclude functionally active, highly divergent generation after task-specific conditioning or fine-tuning: ProGen generated catalytically active lysozymes with as little as 31.4% identity to natural proteins [@madani2023]. Sequence divergence is therefore not itself evidence of functional extrapolation.

#### Figures

![[plms-poorly-rank-high-fitness-variants.png]]

![[plms-fail-functional-novelty-extrapolation.jpg]]

*Figures from [@woolley2026]*

#### See also

* [[No one-size-fits-all best approach to zero-shot or few-shot protein fitness prediction]]
* [[Protein language models are better zero-shot predictors for ranking closely related sequences than distantly related sequences]]
* [[Fitness prediction]]
