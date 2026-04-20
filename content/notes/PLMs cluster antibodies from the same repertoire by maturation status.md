---
tags:
  - protein-language-models/antibodies
  - alignment/sequence-based
created: "2025-02-16T03:31:21"
modified: "2026-04-20T08:24:12"
---
#### Summary
**[[Antibodies|Antibody]] [[Protein language models|language models]] learn about [[Affinity maturation|affinity maturation]] and how far antibody sequences are from [[Germline]].** This has been observed in AntiBERTy, AbLang, and PALM [^ruffolo2021][^olsen2022][^jing2023]. Progression of sequences in [[Immune repertoires|immune repertoires]] can be observed in [[Dimensionality reduction|dimensionality reduction]] of AntiBERTy embeddings (t-SNE). This was also shown with AntiBERTa but not SAPIENS or ProtBERT.

#### Figures
![[Repertoire-AntiBERTy-PCA.png]]
*Figure from [^ruffolo2021]*

![[Intra-repertoire-Ab-clustering.png]]
*Figure from [^leem2022]*

#### See also
- [[PLM-derived antibody representations can distinguish engineered from human-derived Abs]]
- [[CDR representations segregate into distinct clusters]]

[^ruffolo2021]: Ruffolo et al. (2021) "Deciphering antibody affinity maturation with language models and weakly supervised learning." https://doi.org/10.48550/arXiv.2112.07782
[^olsen2022]: Olsen et al. (2022) "AbLang: an antibody language model for completing antibody sequences." *Bioinformatics Advances*. https://doi.org/10.1093/bioadv/vbac046
[^jing2023]: Jing et al. (2024) "Accurate prediction of antibody function and structure using bio-inspired antibody language model." Briefings Bioinform.. https://doi.org/10.1093/BIB/BBAE245
[^leem2022]: Leem et al. (2022) "Deciphering the language of antibodies using self-supervised learning." *Patterns*. https://doi.org/10.1016/j.patter.2022.100513
