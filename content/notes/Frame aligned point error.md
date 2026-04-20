---
tags:
created: 2024-07-24T05:19:43
modified: "2026-04-20T07:16:03"
---
#### Summary
**Frame aligned point error** (FAPE) is a loss function used to train [[Structure prediction|protein structure prediction]] deep learning models such as [[AlphaFold2]] and [[RosettaFold]]. It avoids the instabilities of training with RMSD. A modified version, frame-aligned frame error, was presented by [^wu2024] and fixes some problems regarding [[Vanishing gradient problem|vanishing gradients]] when evaluating poses with large rotational deviations.

#### See also
- [[FAPE can be extended to ligands]]
- [[RMSD is a poor training objective for structure prediction]]

[^wu2024]: Wu et al. (2024) "FAFE: Immune Complex Modeling with Geodesic Distance Loss on Noisy Group Frames." ICML. https://proceedings.mlr.press/v235/wu24g.html
