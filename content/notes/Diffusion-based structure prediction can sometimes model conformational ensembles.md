---
tags:
  - diffusion-models/structure-prediction
  - protein-folding/structure-prediction
  - tm-score
created: "2026-04-10T15:35:05"
modified: "2026-04-21T07:28:09"
---

#### Summary

**[[structure-prediction|Protein structure prediction]] methods reliant on [[diffusion-models|diffusion]] can sometimes predict conformational heterogeneity** [@fan2024]. Authors of Diffold had to reweigh the PDB by [[Clustering|clustering]] by [[tm-score|TM-score]]. Prior efforts by others were not successful: the conformational diversity of EigenFold was more representative of error than actual dynamics [@jing2023], whereas authors of [[alphafold3|AlphaFold3]] found that it predicted the same (incorrect) conformation of [[E3 ubiquitin ligases]], rather than an ensemble of states [@abramson2024].

#### See also
* [[Biomolecular diffusion models cannot reproduce the equilibrium dynamics of the simulations they are trained on]]
