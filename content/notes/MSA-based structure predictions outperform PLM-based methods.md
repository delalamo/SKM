---
tags:
  - protein-folding/misc
created: "2024-07-02T05:21:45"
modified: "2026-04-10T14:30:55"
---

#### Summary

**Protein [[Structure prediction|structure prediction]] methods reliant on [[Multiple sequence alignments|MSAs]] outperform those that use [[Protein language models|PLMs]]**. This was observed in [[CASP15]] and documented by [^hu2022] and [^barrett2022].

#### Details

This may stem from the superior performance of these methods on contact prediction (documented by the authors of [[MSA Transformer]]; [^rao2021]) and structure interface scoring [^liu2023].

[^hu2022]: Hu et al. (2022) "Exploring evolution-aware &amp; -free protein language models as protein function predictors." https://doi.org/10.48550/arXiv.2206.06583
[^barrett2022]: Barrett et al. (2022) "So ManyFolds, So Little Time: Efficient Protein Structure Prediction With pLMs and MSAs." https://doi.org/10.1101/2022.10.15.511553
[^rao2021]: Rao et al. (2021) "MSA Transformer." https://doi.org/10.1101/2021.02.12.430858
[^liu2023]: Liu et al. (2023) "GraphCPLMQA: Assessing protein model quality based on deep graph coupled networks using protein language model." https://doi.org/10.1101/2023.05.16.540981
