---
title: Generic PLMs outperform antibody-specific PLMs on zero-shot predictions of affinity changes
tags:
  - protein-language-models/antibodies
  - thermostability/prediction
created: 2024-07-02T05:11:51
modified: "2026-04-21T05:01:15"
---
#### Summary
 **Generic [[Protein language models|PLMs]] outperform [[Antibodies|antibody]] LMs on zero-shot prediction of affinity changes.** This was observed using [[ESM]] [@hie2023] and other [[BERT]]-based models [@li2023machine], as well as the autoregressive model like [[ProGen]] [@nijkamp2023]. However, they are worse at predicting [[Antibody LMs outperform generic PLMs on intrafamily thermostability prediction|intra-family thermostability]] [@chungyoun2024].

#### Details
Hie et al. concluded this by comparing experimental binding affinity data collected on clones picked using ESM to zero-shot predictions by AbLang and SAPIENS. [@hie2023]

The failure of antibody LMs to predict residues with high affinity may be due to their [[PLMs are biased toward germline antibodies|bias toward germline residues]].
