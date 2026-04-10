---
tags:
  - protein-folding/misc
created: "2026-01-22T12:38:44"
modified: "2026-04-10T14:30:55"
---
#### Summary
**Pretraining performance does not capture effectiveness on downstream tasks** [^neyshabur2020][^li2024]. Neyshabur et al found that using different post-plateau checkpoints as starting points for fine-tuning had drastically different performance on downstream tasks, with more heavily trained models showing better performance.

#### See also
- [[Protein property prediction using PLMs does not benefit from scale except when predicting inferring features of either structural or sparsely populated sequence families]]
- [[Fine-tuning leads to small changes in parameter values in L2 space]]
- [[Fine-tuning can be detrimental to performance]]

[^neyshabur2020]: Neyshabur et al. (2020) "What is being transferred in transfer learning?." *arXiv*. https://doi.org/10.48550/ARXIV.2008.11687
[^li2024]: Li et al. (2024) "Feature Reuse and Scaling: Understanding Transfer Learning with Protein Language Models." https://doi.org/10.1101/2024.02.05.578959
