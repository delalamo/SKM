---
tags:
  - protein-folding/misc
created: "2024-05-29T10:29:14"
modified: "2026-04-10T14:30:55"
---

## Summary

**[[Structure prediction|Protein folding]] neural networks can be combined with [[Variational autoencoders|VAEs]] for conformational modeling** ([Mansoor et al 2023][^mansoor2023]). Authors used [[RosettaFold]] in conjunction with the VAE to sample cryptic pockets in K-Ras.

## Details

* Used RMSD loss ([[RMSD is a poor training objective for structure prediction]])
* Resulting models were more amenable to ligand docking ([[High-accuracy computational models might not always be effective for ligand docking]])

[^mansoor2023]: Mansoor et al. (2023) "Protein Ensemble Generation through Variational Autoencoder Latent Space Sampling." https://doi.org/10.1101/2023.08.01.551540
