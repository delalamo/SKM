---
tags:
  - alphafold2
  - structure-prediction/sampling
created: "2025-04-09T10:01:58"
modified: "2026-04-20T08:32:20"
---

#### Summary

**In training [[AlphaFold2|OpenFold]], [^ahdritz2024] found that excluding all sheet proteins or all helical proteins from the training set did not prevent it from learning to sample those topologies correctly.** Additionally, it could predict the structures of CATH domains removed from training, although that had a more dramatic effect on predictive performance than random subsampling of the training set.

#### Figures

![[Pasted-image-20231211070606.png]]

*Ref [^ahdritz2024]*

#### See also

- [[DL structure prediction methods cannot predict CDR conformations unseen during training]]

[^ahdritz2024]: Ahdritz et al. (2024) "OpenFold: retraining AlphaFold2 yields new insights into its learning mechanisms and capacity for generalization." Nature Methods. https://doi.org/10.1038/s41592-024-02272-z
