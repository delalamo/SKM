---
title: Adding smoothness losses during SAE training can improve motif identification
tags:
  - model-analysis/interpretability
  - training/objectives-and-optimization
created: "2026-10-07"
modified: "2026-10-07T08:57:06"
---

#### Summary

**Adding smoothness losses during [[Sparse autoencoder|SAE]] training can improve motif identification** [@hou2026_F]. In MotifAE, this was done by enforcing latent feature sharing between neighboring residues.

#### Figures

![[motifae-smoothness-loss.png]]

_Ref [@hou2026_F]_

#### See also

- [[Sparse autoencoders recover protein-family and gene-ontology features from PLM representations]]

#### Sources

- [Source issue #1036](https://github.com/delalamo/SKM/issues/1036).
