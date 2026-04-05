---
title: ESM
tags:
  - esm
---

**ESM** is series of a [[Protein language models|protein language models]] that use the [[BERT]] masking training objectives (introduced in [[10.1073__pnas.2016239118|Rives et al 2021]], [[10.1126__science.ade2574|Lin et al 2023]], and [[10.1126__science.ads0018|Hayes et al 2025]]). Embeddings from a 3B ESM2 model (which was sequence-only) were used to train [[ESMFold]] ([[10.1126__science.ade2574|Lin et al 2023]]). ESM3 directly uses input and output structure tokens as training objectives ([[10.1126__science.ads0018|Hayes et al 2025]]).

#### Details

* ESM1b used dropout in the attention matrices during training, but ESM2 did not.
* [[10.1101__2022.12.21.521521|Verkuil et al 2022]] argue that it generalizes beyond natural proteins. Its training set excludes artificial proteins.
* ESM-1v is a variant effect prediction model trained on [[MSA Transformer]] logits ([[10.1101__2021.07.09.450648|Meier et al 2022]]).

<!-- generated -->
