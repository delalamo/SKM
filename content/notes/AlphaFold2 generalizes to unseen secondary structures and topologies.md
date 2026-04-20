---
tags:
  - alphafold2
  - structure-prediction/sampling
created: "2025-04-09T10:01:58"
modified: "2026-04-20T07:46:00"
---

#### Summary

**In training [[AlphaFold2|OpenFold]], [@ahdritz2024] found that excluding all sheet proteins or all helical proteins from the training set did not prevent it from learning to sample those topologies correctly.** Additionally, it could predict the structures of CATH domains removed from training, although that had a more dramatic effect on predictive performance than random subsampling of the training set.

#### Figures

![[Pasted-image-20231211070606.png]]

*Figure from [@ahdritz2024]*

#### See also

- [[DL structure prediction methods cannot predict CDR conformations unseen during training]]
