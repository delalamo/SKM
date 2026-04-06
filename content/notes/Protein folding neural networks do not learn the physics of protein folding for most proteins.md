---
tags:
  - protein-folding/misc
created: "2024-09-01T04:17:34"
modified: "2026-04-05T23:14:54"
---

## Summary

**[[Structure prediction|Protein folding]] neural networks do not model the physics of protein folding for most proteins** ([Outeiral et al 2022](https://doi.org/10.1093/bioinformatics/btab881)). However, for small proteins, some processes of protein folding have been reproduced during repeated iterations with single-sequence prediction ([Chang & Perez 2024](https://doi.org/10.1101/2024.08.25.609581)).

## Details

The authors use chain length as a null hypothesis and find that it is a better predictor of protein folding pathways than the current crop of methods ([[AlphaFold|AlphaFold2]], [[RosettaFold]], trRosetta, Rosetta, others).
