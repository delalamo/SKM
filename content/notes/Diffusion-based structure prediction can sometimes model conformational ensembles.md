---
tags:
  - diffusion-models/structure-prediction
  - protein-folding/structure-prediction
  - tm-score
created: "2026-04-10T15:35:05"
modified: "2026-04-11T07:27:50"
---

#### Summary

**[[Structure prediction|Protein structure prediction]] methods reliant on [[Diffusion models|diffusion]] can sometimes predict conformational heterogeneity** [^fan2024]. Authors of Diffold had to reweigh the PDB by [[Clustering|clustering]] by [[TM-score]]. Prior efforts by others were not successful: the conformational diversity of EigenFold was more representative of error than actual dynamics [^jing2023], whereas authors of [[AlphaFold|AlphaFold3]] found that it predicted the same (incorrect) conformation of [[E3 ubiquitin ligases]], rather than an ensemble of states [^abramson2024].

#### See also
* [[Biomolecular diffusion models cannot reproduce the equilibrium dynamics of the simulations they are trained on]]

[^fan2024]: Fan et al. (2024) "Accurate Conformation Sampling via Protein Structural Diffusion." https://doi.org/10.1101/2024.05.20.594916
[^jing2023]: Jing et al. (2023) "EigenFold: Generative Protein Structure Prediction with Diffusion Models." https://doi.org/10.48550/arxiv.2304.02198
[^abramson2024]: Abramson et al. (2024) "Accurate structure prediction of biomolecular interactions with AlphaFold 3." *Nature*. https://doi.org/10.1038/s41586-024-07487-w
