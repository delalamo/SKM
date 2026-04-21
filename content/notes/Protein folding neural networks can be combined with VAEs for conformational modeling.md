---
tags:
  - structure-prediction/sampling
  - conformational-dynamics/modeling
created: "2024-05-29T10:29:14"
modified: "2026-04-21T05:01:15"
---

## Summary

**[[Structure prediction|Protein folding]] neural networks can be combined with [[Variational autoencoders|VAEs]] for conformational modeling** [@mansoor2023]. Authors used [[RosettaFold]] in conjunction with the VAE to sample cryptic pockets in K-Ras.

## Details

* Used RMSD loss ([[RMSD is a poor training objective for structure prediction]])
* Resulting models were more amenable to ligand docking ([[High-accuracy computational models might not always be effective for ligand docking]])
