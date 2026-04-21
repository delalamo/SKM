---
title: ESM
created: 2026-04-10T14:30:55
modified: "2026-04-21T07:28:09"
---

**ESM** is series of a [[protein-language-models|protein language models]] that use the [[BERT]] masking training objectives (introduced in [@rives2021; @lin2023], and [@hayes2025]). Embeddings from a 3B ESM2 model (which was sequence-only) were used to train [[ESMFold]] [@lin2023]. ESM3 directly uses input and output structure tokens as training objectives [@hayes2025].

#### Details

* ESM1b used dropout in the attention matrices during training, but ESM2 did not.
* Verkuil et al. [@verkuil2022] argue that it generalizes beyond natural proteins. Its training set excludes artificial proteins.
* ESM-1v is a variant effect prediction model trained on [[MSA Transformer]] logits [@meier2022].
