---
title: SimpleFold
created: 2026-04-10T14:30:55
modified: "2026-04-21T05:01:15"
---

**SimpleFold** is a [[Structure prediction|protein structure prediction]] method that exclusively relies on [[Transformer|transformer]] blocks and [[Flow matching|flow matching]] [@wang2025b]. It relies on embeddings from [[ESM]]2-3B and models from the [[AlphaFold2]] DB and [[ESMFold]] Atlas. Authors scaled it from several hundred million parameters to 3 billion parameters, observing improved performance with larger sizes. They also fine-tuned versions of all six models on ATLAS MD data.

#### Details

[@ouyangzhang2025] noted that transformer blocks are extremely inefficient relative to other approaches, although it isn't clear if these are the same.

#### See also

* [[Triangular updates are dispensable for structure prediction]]
