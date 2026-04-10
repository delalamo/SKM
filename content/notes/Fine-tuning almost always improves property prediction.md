---
tags:
  - protein-folding/misc
created: "2026-01-22T12:38:44"
modified: "2026-04-10T14:02:57"
---

#### Summary

**Fine-tuning [[Protein language models|PLMs]] [[ESM]]2, ProtT5, and Ankh virtually always improved property prediction** ([[Variant effect prediction|variant effect prediction]], [[Stability and thermostability|stability]] prediction, [[Function prediction|function prediction]], others) **compared to zero-shot** [^schmirler2023]. [^jiang2024] found that active learning for [[Directed evolution|directed evolution]] benefited from fine-tuning over zero-shot prediction after two to four rounds (fine-tuning carried out using a [[Random forest|random forest]] model trained on mean-pooled embeddings).

#### Figures
\![[Pasted-image-20240102175550.png]]

*Figure 1 from [^schmirler2023]*

\![[Pasted-image-20240722093551.png]]

*Figure from [^jiang2024]*

#### See also
* [[Protein property prediction using PLMs does not benefit from scale except when predicting inferring features of either structural or sparsely populated sequence families]]
* [[Sequences with lower log-likelihoods are worse for zero-shot variant effect prediction using PLMs]]

[^schmirler2023]: Schmirler et al. (2023) "Fine-tuning protein language models boosts predictions across diverse tasks." https://doi.org/10.1101/2023.12.13.571462
[^jiang2024]: Jiang et al. (2024) "Rapid protein evolution by few-shot learning with a protein language model." https://doi.org/10.1101/2024.07.17.604015
