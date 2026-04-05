---
tags:
  - protein-folding/misc
---

#### Summary

**In training [[AlphaFold|OpenFold]], Ahdritz et al 2024[^ahdritz2024] found that excluding all sheet proteins or all helical proteins from the training set did not prevent it from learning to sample those topologies correctly.** Additionally, it could predict the structures of CATH domains removed from training, although that had a more dramatic effect on predictive performance than random subsampling of the training set.

#### Figures

![](/assets/Pasted-image-20231211070606.png)

*Figure from Ahdritz et al 2024[^ahdritz2024]*

#### See also

- [[DL structure prediction methods cannot predict CDR conformations unseen during training]]

[^ahdritz2024]: Ahdritz et al. (2022) "OpenFold: Retraining AlphaFold2 yields new insights into its learning mechanisms and capacity for generalization." https://doi.org/10.1101/2022.11.20.517210
