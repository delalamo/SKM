---
tags:
created: 2024-05-08T17:45:39
modified: "2026-04-20T07:46:00"
---
#### Summary
**Dynamic time warping is used to compare antibody loops of different lengths** (Guloglu and [@guloglu2023]). It is analogous to the Needleman-Wunsch algorithm, and reduces to RMSD when loops are the same length. It is not designed to work with [[Complementarity-determining regions|CDRH3]]. When all CDRs are used, seventeen clusters result, four of which span multiple loop lengths.

#### Details
From [@nowak2016]:

> "The algorithm uses dynamic programming to find the optimum path through the low-cost areas of a cost matrix. When 2 loops of the same length are compared, the algorithm returns the RMSD between the backbone atoms of the loops. When two loops of different lengths are compared, the algorithm calculates the RMSD between backbone atoms of residues matched by the walk through the cost matrix."

#### See also
- [[Length independent clustering improves CDR prediction]]
