---
tags:
  - antibodies/misc
created: "2024-05-08T17:45:39"
modified: "2026-04-05T23:14:54"
---
#### Summary
**Dynamic time warping is used to compare antibody loops of different lengths** (Guloglu and Deane 2023[^guloglu2023]). It is analogous to the Needleman-Wunsch algorithm, and reduces to RMSD when loops are the same length. It is not designed to work with [[Complementarity-determining regions|CDRH3]]. When all CDRs are used, seventeen clusters result, four of which span multiple loop lengths.

#### Details
From Nowak et al 2016[^nowak2016]:

> "The algorithm uses dynamic programming to find the optimum path through the low-cost areas of a cost matrix. When 2 loops of the same length are compared, the algorithm returns the RMSD between the backbone atoms of the loops. When two loops of different lengths are compared, the algorithm calculates the RMSD between backbone atoms of residues matched by the walk through the cost matrix."

#### See also
- [[Length independent clustering improves CDR prediction]]

[^guloglu2023]: Guloglu & Deane (2023) "Specific attributes of the VL domain influence both the structure and structural variability of CDR-H3 through steric effects." *Frontiers in Immunology*. https://doi.org/10.3389/fimmu.2023.1223802
[^nowak2016]: Nowak et al. (2016) "Length-independent structural similarities enrich the antibody CDR canonical class model." *mAbs*. https://doi.org/10.1080/19420862.2016.1158370
