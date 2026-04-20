---
tags:
  - structure-prediction/sampling
created: "2024-07-02T05:21:45"
modified: "2026-04-20T07:16:03"
---

#### Summary

**Protein [[Structure prediction|structure prediction]] methods reliant on [[Multiple sequence alignments|MSAs]] outperform those that use [[Protein language models|PLMs]]**. This was observed in [[CASP15]] and documented by [^hu2022] and [^barrett2022].

#### Details

This may stem from the superior performance of these methods on contact prediction (documented by the authors of [[MSA Transformer]]; [^rao2021]) and structure interface scoring [^liu2023].

[^hu2022]: Hu et al. (2022) "Exploring evolution-aware & -free protein language models as protein function predictors." NeurIPS. http://papers.nips.cc/paper_files/paper/2022/hash/fe066022bab2a6c6a3c57032a1623c70-Abstract-Conference.html
[^barrett2022]: Barrett et al. (2022) "So ManyFolds, So Little Time: Efficient Protein Structure Prediction With pLMs and MSAs." https://doi.org/10.1101/2022.10.15.511553
[^rao2021]: Rao et al. (2021) "MSA Transformer." https://doi.org/10.1101/2021.02.12.430858
[^liu2023]: Liu et al. (2023) "Assessing protein model quality based on deep graph coupled networks using protein language model." Briefings in Bioinformatics. https://doi.org/10.1093/bib/bbad420
