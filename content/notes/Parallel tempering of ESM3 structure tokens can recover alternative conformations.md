---
tags:
  - prediction/ensembles
  - inference/sampling-and-search
  - model-design/multimodal
created: "2026-09-15"
modified: "2026-09-25"
---

#### Summary

**[[Replica-exchange molecular dynamics|Parallel tempering]] applied to [[ESM|ESM3]] [[Protein structure tokenization|structure tokens]] can recover alternative protein conformations without retraining the model** [@wang2026msfold]. Sequence log-likelihood conditioned on each sampled structure provides a reference-free ranking score. The paper reports better selection than pTM or pLDDT.

#### See also

- [[Structure prediction methods undersample the conformational space they find to be high-confidence]]
- [[Protein structure prediction methods are unable to predict the energetics of a conformational landscape unless explicitly trained for that purpose]]
- [[Sequence perplexity and TM-score are negatively correlated when predicting structure using protein language models]]
