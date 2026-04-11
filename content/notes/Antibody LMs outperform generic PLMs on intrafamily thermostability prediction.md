---
tags:
  - protein-language-models/antibodies
created: "2026-02-26T15:14:37"
modified: "2026-04-11T06:06:39"
---

#### Summary

**[[Antibody language models]] outperform generic [[Protein language models|PLMs]] on intrafamily but not general [[Stability and thermostability|thermostability]] prediction** [^chungyoun2024]. A version of [[ProGen]] specifically trained on [[Antibodies|antibody]] sequences outperform generic ProGen models on intra-family [[Stability and thermostability|thermostability]] prediction. On inter-family prediction, they are bested by [[ESM-IF]] (see [[Structure-based methods outperform sequence-based methods on protein stability prediction of point mutants, but not full sequences]]). This could be because antibodies are separated [[PLMs can separate Abs by origin|by V-gene]] by antibody LMs.

#### Figures

\![[Pasted-image-20240116124937.png]]

*Figure 5 from [^chungyoun2024]*

#### See also

- [[Generic PLMs outperform antibody-specific PLMs on zero-shot predictions of affinity changes]]
- [[Protein language models are better zero-shot predictors for ranking closely related sequences than distantly related sequences]]

[^chungyoun2024]: Chungyoun et al. (2024) "FLAb: Benchmarking deep learning methods for antibody fitness prediction." https://doi.org/10.1101/2024.01.13.575504
