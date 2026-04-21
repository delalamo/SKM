---
tags:
  - protein-language-models/antibodies
  - alignment/sequence-based
created: "2025-02-16T03:31:21"
modified: "2026-04-21T07:20:46"
---
#### Summary
**[[tags/antibodies|Antibody]] [[tags/protein-language-models|language models]] learn about both V gene usage and [[tags/affinity-maturation|affinity maturation]] status (how far antibody sequences are from [[Germline|germline]]).** This has been observed in AntiBERTy, AbLang, and PALM [@ruffolo2021; @olsen2022; @jing2024]. Progression of sequences in [[tags/immune-repertoires|immune repertoires]] can be observed in [[Dimensionality reduction|dimensionality reduction]] of AntiBERTy embeddings (t-SNE). This was also shown with AntiBERTa but not SAPIENS or ProtBERT.

#### Figures
![[Repertoire-AntiBERTy-PCA.png]]
*Ref [@ruffolo2021]*

![[Intra-repertoire-Ab-clustering.png]]
*Ref [@leem2022]*

![[Pasted-image-20231017145000.png]]
*Ref [@olsen2022]*

#### See also
- [[PLM-derived antibody representations can distinguish engineered from human-derived Abs]]
- [[CDR representations segregate into distinct clusters]]
