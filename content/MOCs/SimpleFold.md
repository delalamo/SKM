---
title: SimpleFold
tags:
  - simplefold
---

**SimpleFold** is a [[Structure prediction|protein structure prediction]] method that exclusively relies on [[Transformer|transformer]] blocks and [[Flow matching|flow matching]] ([[10.48550__ARXIV.2509.18480|Wang et al 2025]]). It relies on embeddings from [[ESM]]2-3B and models from the [[AlphaFold]] DB and [[ESMFold]] Atlas. Authors scaled it from several hundred million parameters to 3 billion parameters, observing improved performance with larger sizes. They also fine-tuned versions of all six models on ATLAS MD data.

#### Details

[[10.48550__ARXIV.2510.18870|Ouyang-Zhang et al 2025]] noted that transformer blocks are extremely inefficient relative to other approaches, although it isn't clear if these are the same.

#### See also

* [[Triangular updates are dispensable for structure prediction]]

<!-- generated -->
