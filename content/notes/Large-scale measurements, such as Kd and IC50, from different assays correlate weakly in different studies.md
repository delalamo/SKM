---
tags:
  - citation-fix
created: 2026-04-05T17:41:51
modified: "2026-04-21T05:01:15"
---

#### Summary

Measurements of protein-ligand effects (such as $K_d$ and $IC_50$) carried out in different assays only weakly correlate with each other. The correlation is strengthened when the assays share many protein-ligand pairs [@landrum2024]. This means that substantial noise is introduced when combining data from multiple assays, even on the same protein. Another recent paper found that the same data collected in two different labs with different equipment has an average Spearman correlation of 0.73. Due to these factors, training deep-learning affinity predictors on many datasets from different sources therefore requires complex schemes (cite Boltz-2 paper)

#### Figures

![[Pasted-image-20240225100932.png]]
*Figure 1 from [@landrum2024]*

#### See also

* [[About 100k datapoints required to train accurate ddG predictor]]
* [[Spearman correlations of protein property prediction methods do not correlate perfectly with absolute error]]
* [[Kd differs from IC50, LD50, and GI50]]
