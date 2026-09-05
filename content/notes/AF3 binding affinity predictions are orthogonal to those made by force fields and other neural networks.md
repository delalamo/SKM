---
tags:
  - prediction/binding
  - inference/ensembling
created: 2024-07-02T05:07:14
modified: "2026-07-28T14:12:17"
---
#### Summary
**Predicted changes in binding affinity of [[notes/protein-protein-interactions|PPIs]] by [[notes/alphafold3|AlphaFold3]] are orthogonal to those made by other methods, and can be ensembled with favorable results** [@lu2024]. AF3 outperforms other deep learning-based methods such as [[notes/inverse-folding|Inverse folding]] methods and [[notes/protein-language-models|Protein language models]]. Its predictions can be improved by ensembling with those from force fields, but not other deep learning methods. It is unclear if those predictions are better than those from force fields alone.

#### Figures
![[Pasted-image-20240529105729.png]]
*Figure 2 from [@lu2024]*

#### See also

- [[All-atom structure and affinity predictors partially generalize to point mutants]]
