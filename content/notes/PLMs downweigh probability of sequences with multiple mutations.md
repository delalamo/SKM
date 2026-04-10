---
tags:
  - protein-folding/misc
created: "2024-07-02T05:23:04"
modified: "2026-04-10T14:30:55"
---

## Summary

**[[Protein language models|PLMs]] are biased against sequences with multiple mutations** ([Shaw et al 2023][^shaw2023]).

## Details

The authors propose normalizing these by generating large quantities ($10^{4}$) of mutants with equal number of mutations and ranking them that way.

## Figures

\![[Effect-of-sequence-distance-on-variant-prediction.png]]
\![[Debiasing-PLMs.png]]
*Figures from [Shaw et al 2023][^shaw2023]*

[^shaw2023]: Shaw et al. (2023) "Removing bias in sequence models of protein fitness." https://doi.org/10.1101/2023.09.28.560044
