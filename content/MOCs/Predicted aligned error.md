---
title: Predicted aligned error
tags:
  - pae
  - structure-prediction/metrics
created: "2026-04-10T14:02:57"
modified: "2026-04-17T06:40:29"
---

**Predicted aligned error** (PAE) is a measurement calculated by protein [[Structure prediction|structure prediction]] neural networks to capture positional errors between two amino acids in a computational model. It was introduced by [[AlphaFold|AlphaFold2]]. A derivative metric, ipSAE, has been shown to be more robust at identifying potential binders.

![[Pasted-image-20260327091043.png]]
*Figure from [^chow2025]*

<!-- generated -->

## General

- [[AF2 RMSD to ground truth correlated with RMSD between conformations]]
- [[AlphaFold2 and RosettaFold sometimes produce different conformations]]
- [[AlphaFold2 predicts the holo form of proteins in most cases]]
- [[AlphaFold3 ipTM can distinguish between antibody binders and nonbinders]]
- [[DiffDock confidence is inversely correlated with RMSD]]
- [[High predicted aligned error correlates with violation of experimental distance measurements]]
- [[PAE weakly correlates with Ab-Ag binding]]
- [[Sequence- and structure-derived ML quality metrics from ML do not correlate with each other]]
- [[Structure prediction uncertainty metrics as energy functions]]
- [[pLDDT and PAE in protein folding neural networks are correlated]]
- [[pLDDT and PAE inversely correlated with protein dynamics in dynamic naturally occurring proteins, but not de novo proteins]]
- [[pLDDT is inversely correlated with CDRH3 length]]
