---
title: Base PLMs must usually be fine-tuned to generate functionally active sequences
tags:
  - protein-language-models/training
created: "2026-03-18T07:59:23"
modified: "2026-04-20T08:16:13"
---
#### Summary
 **Base [[Protein language models|protein language models]] must usually be fine-tuned to generate functionally active sequences** [^madani2023][^munsamy2024]. [^bixby2026] showed that, in a head-to-head between an unspecified foundation model and its "evo-tuned" derivative, the latter was better at [[Variant effect prediction|variant effect prediction]]. Note that this is not true of models where functional annotations can be provided, such as ZymCTRL [^munsamy2024] and ESM3 [^hayes2025].

#### Details
Fannjiang and [^fannjiang2023] give several citations for how pan-protein data is unnecessary for generating novel sequences.
Evo-tuning was first presented by [^biswas2019]

#### Figures
![[Pasted-image-20240513202423.png]]
*Ref [^munsamy2024]*
![[Pasted-image-20260311082003.png]]
*Ref [^bixby2026]*

#### See also
* [[Protein language models make equally effective predictions when trained on individual proteins or protein families]]
* [[Pretraining contributes nearly nothing to performance when fine-tuning protein language models in data-rich situations]]
* [[Fine-tuning base models on test cases can improve the performance of variant effect and structure prediction]]

[^madani2023]: Madani et al. (2023) "Large language models generate functional protein sequences across diverse families." *Nature Biotechnology*. https://doi.org/10.1038/s41587-022-01618-2
[^munsamy2024]: Munsamy et al. (2024) "Conditional language models enable the efficient design of proficient enzymes." https://doi.org/10.1101/2024.05.03.592223
[^bixby2026]: Bixby et al. (2026) "What comes after
                  de novo
                  ? Automated lead optimization of proteins with CRADLE-1." https://doi.org/10.64898/2026.03.06.710001
[^hayes2025]: Hayes et al. (2025) "Simulating 500 million years of evolution with a language model." *Science*. https://doi.org/10.1126/science.ads0018
[^fannjiang2023]: Fannjiang & Listgarten (2023) "Is novelty predictable?." *arXiv*. https://doi.org/10.48550/arXiv.2306.00872
[^biswas2019]: Biswas et al. (2021) "Low-N protein engineering with data-efficient deep learning." *Nature Methods*. https://doi.org/10.1038/s41592-021-01100-y
