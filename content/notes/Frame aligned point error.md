---
tags:
  - protein-folding/misc
---
#### Summary
**Frame aligned point error** (FAPE) is a loss function used to train [[Structure prediction|protein structure prediction]] deep learning models such as [[AlphaFold|AlphaFold2]] and [[RosettaFold]]. It avoids the instabilities of training with RMSD. A modified version, frame-aligned frame error, was presented by Wu et al 2024b[^wu2024] and fixes some problems regarding [[Vanishing gradient problem|vanishing gradients]] when evaluating poses with large rotational deviations.

#### See also
- [[FAPE can be extended to ligands]]
- [[RMSD is a poor training objective for structure prediction]]

[^wu2024]: Wu et al. (2024) "FAFE: Immune Complex Modeling with Geodesic Distance Loss on Noisy Group Frames." https://doi.org/10.48550/ARXIV.2407.01649
