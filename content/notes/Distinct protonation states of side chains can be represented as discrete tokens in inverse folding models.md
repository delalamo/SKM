---
title: Distinct protonation states of side chains can be represented as discrete tokens in inverse folding models
tags:
  - design/inverse-folding
  - design/binders
created: "2026-10-07"
modified: "2026-10-09T04:56:38"
---

#### Summary

**Distinct protonation states of glutamate, aspartate, and histidine side chains can be represented as discrete tokens in [[Inverse folding|inverse folding]] models** [@jacobsen2026]. PD-L1 binders designed with these tokens implemented in PottsMPNN [@birnbaum2026] show pH-specific target binding.

#### Details

The training set for this protonation-aware inverse folding model was obtained by A) finding suitable protonation annotation examples in the PDB and B) training an XGBoost classifier on these labels and C) cross-referencing predictions from the rest of the PDB using physics-based scoring functions.

Sampling of pH-specific binders was done on RFDiffusion3-designed backbones by MCMC multi-parameter optimization of both target pH and overall sequence energy. [[Structure prediction|Forward folding]] filters were not applied.

#### Figures

![[proton-pottsmpnn-ph-binding.png]]

_Ref [@jacobsen2026]_

#### See also

- [[Sequence recovery in inverse folding models is not correlated with self-consistency of generated designs]]
