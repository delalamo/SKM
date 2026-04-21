---
tags:
  - protein-language-models/antibodies
created: "2026-02-26T15:14:37"
modified: "2026-04-21T07:28:09"
---

#### Summary

**[[antibodies|Antibody]]-specific [[protein-language-models|protein language models]] outperform generic PLMs on intrafamily but not general [[thermostability|thermostability]] prediction** [@chungyoun2024]. A version of [[ProGen]] specifically trained on [[antibodies|antibody]] sequences outperform generic ProGen models on intra-family [[thermostability|thermostability]] prediction. On inter-family prediction, they are bested by [[ESM-IF]] (see [[Structure-based methods outperform sequence-based methods on protein stability prediction of point mutants, but not full sequences]]).

#### Details
One related observation (unpublished as of 19 April 2026) is that the mean-pooled CDRH3 embeddings learned by generic LMs, but not antibody LMs, are basically meaningless insofar as they match those of scrambled CDRH3 sequences with the same framework. A separate theory is that this could be because antibodies are separated [[PLMs cluster antibodies from the same repertoire by V gene and maturation status|by V-gene]] by antibody LMs.

#### Figures

![[Pasted-image-20240116124937.png]]

*Figure 5 from [@chungyoun2024]*

#### See also

- [[Generic PLMs outperform antibody-specific PLMs on zero-shot predictions of affinity changes]]
- [[Protein language models are better zero-shot predictors for ranking closely related sequences than distantly related sequences]]
