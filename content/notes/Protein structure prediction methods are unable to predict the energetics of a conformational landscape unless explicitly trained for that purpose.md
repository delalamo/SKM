---
tags:
  - structure-prediction/limitations
  - conformational-dynamics/modeling
created: "2025-09-01T04:55:07"
modified: "2026-04-20T07:46:00"
---

#### Summary

**Protein [[Structure prediction|structure prediction]] methods are unable to predict the energetics of a [[Protein dynamics|conformational landscape]] unless explicitly trained for that purpose** ([[yQcebEgQfH|Jing et al 2023]], [@vani2023exploring; @riccabona2024; @delalamo2022sampling]), although Monteiro da [@monteiro2024] disagrees and provides some anecdotal examples. [@schafer2024] show that at least for [[Fold-switching proteins|fold-switching proteins]], the sampled conformation is memorized by the exact protein folding method, whi[@lazou2024] show the same for binders that alternate between open-closed conformations. A step in the right direction is how [[BioEmu]] reproduces $\Delta G$ values to within 1 kcal/mol when modeling folded and unfolded states and comparing their populations [@lewis2024]; however, later results showed that it [[Inverse folding NNs are better predictors of equilibrium dynamics than protein folding NNs|isn't as effective at predicting the equilibrium dynamics of mutated enzymes as well as inverse folding NNs]].
