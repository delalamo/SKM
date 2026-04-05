---
tags:
  - protein-folding/misc
---

#### Summary

**Ruffolo et al 2023[^ruffolo2023] used RMSD as the error function of [[IgFold]]** (as opposed to [[pLDDT|LDDT]]) **and noticed that it was weighted toward lower RMSDs.** They speculate that is due to imbalance in the training data, due to framework residues typically having low RMSD values. They suggest this can be addressed with a weighted loss function.

#### See also

* [[RMSD is a poor training objective for structure prediction]]
* [[pLDDT]]

[^ruffolo2023]: Ruffolo et al. (2023) "Fast, accurate antibody structure prediction from deep learning on massive set of natural antibodies." *Nature Communications*. https://doi.org/10.1038/s41467-023-38063-x
