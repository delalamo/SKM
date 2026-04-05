---
tags:
  - protein-folding/misc
---

#### Summary

**RMSD is a poor training objective for protein [[Structure prediction|structure prediction]].** For proteins, [[Frame aligned point error|FAPE]] is better (Baek et al 2021[^baek2021]). For ligands, the fraction of models predicted under a certain RMSD is better (Corso et al 2023[^corso2023]). However, it was used by Ruffolo et al 2023[^ruffolo2023] to train [[IgFold]] and was apparently effective.

#### See also

* [[RMSD is a partially effective error function]]

[^baek2021]: Baek et al. (2021) "Accurate prediction of protein structures and interactions using a three-track neural network." *Science*. https://doi.org/10.1126/science.abj8754
[^corso2023]: Corso et al. (2022) "DiffDock: Diffusion Steps, Twists, and Turns for Molecular Docking." https://doi.org/10.48550/arXiv.2210.01776
[^ruffolo2023]: Ruffolo et al. (2023) "Fast, accurate antibody structure prediction from deep learning on massive set of natural antibodies." *Nature Communications*. https://doi.org/10.1038/s41467-023-38063-x
