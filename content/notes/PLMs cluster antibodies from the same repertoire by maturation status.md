---
tags:
  - antibodies/misc
created: "2025-02-16T03:31:21"
modified: "2026-04-10T14:30:55"
---
#### Summary
**[[Antibody language models]] learn about [[Affinity maturation|affinity maturation]] and how far antibody sequences are from [[Germline]].** This has been observed in AntiBERTy, AbLang, and PALM [^ruffolo2021][^olsen2022][^jing2023]. Progression of sequences in [[Immune repertoires]] can be observed in [[Dimensionality reduction|dimensionality reduction]] of AntiBERTy embeddings (t-SNE). This was also shown with AntiBERTa but not SAPIENS or ProtBERT.

#### Figures
\![[Repertoire-AntiBERTy-PCA.png]]
*Figure from [^ruffolo2021]*

\![[Intra-repertoire-Ab-clustering.png]]
*Figure from [^leem2022]*

#### See also
- [[Ab embeddings can distinguish engineered from human-derived Abs]]
- [[CDR representations segregate into distinct clusters]]

[^ruffolo2021]: Ruffolo et al. (2021) "Deciphering antibody affinity maturation with language models and weakly supervised learning." https://doi.org/10.48550/arXiv.2112.07782
[^olsen2022]: Olsen et al. (2022) "AbLang: an antibody language model for completing antibody sequences." *Bioinformatics Advances*. https://doi.org/10.1093/bioadv/vbac046
[^jing2023]: Jing et al. (2023) "Accurate Prediction of Antibody Function and Structure Using Bio-Inspired Antibody Language Model." https://doi.org/10.48550/ARXIV.2308.16713
[^leem2022]: Leem et al. (2022) "Deciphering the language of antibodies using self-supervised learning." *Patterns*. https://doi.org/10.1016/j.patter.2022.100513