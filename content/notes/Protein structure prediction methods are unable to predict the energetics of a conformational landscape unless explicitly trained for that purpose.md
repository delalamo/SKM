---
tags:
  - protein-folding/misc
created: "2025-09-01T04:55:07"
modified: "2026-04-05T23:36:09"
---

#### Summary

**Protein [[Structure prediction|structure prediction]] methods are unable to predict the energetics of a [[Protein dynamics|conformational landscape]] unless explicitly trained for that purpose** ([[yQcebEgQfH|Jing et al 2023]], [^vani2023], [^riccabona2024], [^del2022]), although Monteiro da [^monteiro2024] disagrees and provides some anecdotal examples. [^schafer2024] show that at least for [[Fold-switching proteins|fold-switching proteins]], the sampled conformation is memorized by the exact protein folding method, whi[^lazou2024] show the same for binders that alternate between open-closed conformations. A step in the right direction is how [[BioEmu]] reproduces $\Delta G$ values to within 1 kcal/mol when modeling folded and unfolded states and comparing their populations [^lewis2024]; however, later results showed that it [[Inverse folding NNs are better predictors of equilibrium dynamics than protein folding NNs|isn't as effective at predicting the equilibrium dynamics of mutated enzymes as well as inverse folding NNs]].

[^vani2023]: Vani et al. (2023) "Exploring Kinase Asp-Phe-Gly (DFG) Loop Conformational Stability with AlphaFold2-RAVE." *Journal of Chemical Information and Modeling*. https://doi.org/10.1021/acs.jcim.3c01436
[^riccabona2024]: Riccabona et al. (2024) "Assessing AF2’s ability to predict structural ensembles of proteins." https://doi.org/10.1101/2024.04.16.589792
[^del2022]: del Alamo et al. (2022) "Sampling alternative conformational states of transporters and receptors with AlphaFold2." *eLife*. https://doi.org/10.7554/eLife.75751
[^monteiro2024]: Monteiro da Silva et al. (2024) "High-throughput prediction of protein conformational distributions with subsampled AlphaFold2." *Nature Communications*. https://doi.org/10.1038/s41467-024-46715-9
[^schafer2024]: Schafer & Porter (2024) "AlphaFold2’s training set powers its predictions of fold-switched conformations." https://doi.org/10.1101/2024.10.11.617857
[^lazou2024]: Lazou et al. (2024) "Predicting multiple conformations of ligand binding sites in proteins suggests that AlphaFold2 may remember too much." *Proceedings of the National Academy of Sciences*. https://doi.org/10.1073/pnas.2412719121
[^lewis2024]: Lewis et al. (2024) "Scalable emulation of protein equilibrium ensembles with generative deep learning." https://doi.org/10.1101/2024.12.05.626885
