---
tags:
  - protein-folding/misc
---

## Summary

**[[Structure prediction|Protein folding]] neural networks can be combined with [[Variational autoencoders|VAEs]] for conformational modeling** ([Mansoor et al 2023](https://doi.org/10.1101/2023.08.01.551540)). Authors used [[RosettaFold]] in conjunction with the VAE to sample cryptic pockets in K-Ras.

## Details

* Used RMSD loss ([[RMSD is a poor training objective for structure prediction]])
* Resulting models were more amenable to ligand docking ([[High-accuracy computational models might not always be effective for ligand docking]])
