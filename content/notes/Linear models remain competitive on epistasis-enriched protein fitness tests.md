---
tags:
  - prediction/variant-effects
  - evidence/generalization
created: "2026-09-25"
modified: "2026-09-25"
---

#### Summary

**Simple additive models can remain competitive at ranking protein fitness even when the test set is enriched for epistasis** [@didi2026]. Non-additive effects do not imply that all useful signal in the measured outcome requires an interaction model.

#### Details

FLIP2's PDZ3 single-to-double split tests binding between mutated PDZ3 domains and CRIPT peptides. Its 579 test pairs were selected for significant non-additive binding effects. One-hot ridge regression remains competitive with the tested fine-tuned protein language models; it is not uniformly the best model.

Ranking total measured fitness is different from predicting the epistatic residual after additive effects are removed. This result therefore does not show that a linear model represents epistasis. It complements [[GFP fitness data is best fit by simple models|simple-model success on GFP]] without implying that the two landscapes have the same structure.

#### See also

- [[No one-size-fits-all best approach to zero-shot or few-shot protein fitness prediction]]
- [[Protein language models are able to predict epistasis in a zero-shot setting following a nonlinear transform]]
