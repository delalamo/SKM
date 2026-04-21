---
title: Base PLMs must usually be fine-tuned to generate functionally active sequences
tags:
  - protein-language-models/training
created: "2026-03-18T07:59:23"
modified: "2026-04-21T07:28:09"
---
#### Summary
 **Base [[protein-language-models|protein language models]] must usually be fine-tuned to generate functionally active sequences** [@madani2023; @munsamy2024]. [@bixby2026] showed that, in a head-to-head between an unspecified foundation model and its "evo-tuned" derivative, the latter was better at [[variant-effect-prediction|variant effect prediction]]. Note that this is not true of models where functional annotations can be provided, such as ZymCTRL [@munsamy2024] and ESM3 [@hayes2025].

#### Details
Fannjiang and [@fannjiang2023] give several citations for how pan-protein data is unnecessary for generating novel sequences.
Evo-tuning was first presented by [@biswas2019]

#### Figures
![[Pasted-image-20240513202423.png]]
*Ref [@munsamy2024]*
![[Pasted-image-20260311082003.png]]
*Ref [@bixby2026]*

#### See also
* [[Protein language models make equally effective predictions when trained on individual proteins or protein families]]
* [[Pretraining contributes nearly nothing to performance when fine-tuning protein language models in data-rich situations]]
* [[Fine-tuning base models on test cases can improve the performance of variant effect and structure prediction]]
