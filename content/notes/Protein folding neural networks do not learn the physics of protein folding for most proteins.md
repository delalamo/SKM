---
tags:
  - structure-prediction/limitations
created: "2024-09-01T04:17:34"
modified: "2026-04-21T05:01:15"
---

## Summary

**[[Structure prediction|Protein folding]] neural networks do not model the physics of protein folding for most proteins** [@outeiral2022]. However, for small proteins, some processes of protein folding have been reproduced during repeated iterations with single-sequence prediction [@chang2024].

## Details

The authors use chain length as a null hypothesis and find that it is a better predictor of protein folding pathways than the current crop of methods ([[AlphaFold2]], [[RosettaFold]], trRosetta, Rosetta, others).
