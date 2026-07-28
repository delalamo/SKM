---
tags:
  - protein-language-models/antibodies
  - protein-language-models/representations
  - antibody-developability/expression
created: "2026-07-28"
modified: "2026-07-28T14:12:17"
---

#### Summary

**Random data splits overestimate the ability of general-purpose [[protein-language-models|protein language model]] embeddings to predict [[Nanobodies|nanobody]] expression because the embeddings encode antibody-program identity rather than transferable determinants of expression** [@wang2026_BJ]. General-purpose ESM2 embeddings achieved a ROC-AUC of approximately 0.88 under a random split but only 0.68 when evaluated on held-out antibody programs. AINN-P1 and domain-fine-tuned ESM2 retained ROC-AUC values of 0.81 and 0.83, respectively, on unseen programs.

This qualifies comparisons such as [[Antibody LMs are worse for expression prediction than generic PLMs]]: model rankings and apparent representation quality can depend strongly on whether the evaluation split separates related discovery programs.

#### Figures

![[wang2026-vhh-expression-split-performance.png]]
*Leave-program-out evaluation reveals substantially more leakage in general-purpose ESM2 representations than in AINN-P1 or domain-fine-tuned ESM2 representations. Ref [@wang2026_BJ]*

#### See also

- [[Training antibody language models on normalized mutation frequencies improves zero-shot expression prediction]]
- [[PLMs learn family-specific protein contacts from sequence context windows of about 20-40 amino acids]]
- [[Sequence homology composition can affect performance of fine-tuned protein language models for variant effect prediction]]
- [[Composition of negative data affects rule discovery in binary classification tasks]]
