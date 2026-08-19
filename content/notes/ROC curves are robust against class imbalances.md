---
tags:
title: ROC-AUC is prevalence-invariant but does not measure deployment precision
created: 2024-07-01T02:28:08
modified: "2026-08-19T16:32:04"
---
#### Summary
**The coordinates and AUC of [[Binary classifiers|ROC curves]] are invariant to class prevalence when the class-conditional score distributions are unchanged** [@richardson2024]. However, with rare positives, even a small false-positive rate can yield many false positives; precision-recall curves expose this prevalence-dependent positive predictive value more directly and can make operational differences between classifiers easier to see [@davis2006]. Robustness to class imbalance therefore does not mean that ROC-AUC captures deployment-specific precision or error costs.

#### Figures
![[Pasted-image-20240604071928.png]]
*Ref [@richardson2024]*

#### See also
- [[Sequence perplexity]]
