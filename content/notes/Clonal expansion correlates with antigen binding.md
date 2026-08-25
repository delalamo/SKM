---
tags:
  - affinity-maturation
created: "2025-02-16T03:45:04"
modified: "2026-08-19T17:14:27"
---
#### Summary
**During [[affinity-maturation|affinity maturation]], clonal expansion correlates with antigen binding, and larger clonal families are more likely to bind with higher affinity than smaller ones** [@robinson2014]. Put another way, overrepresented [[antibodies|antibodies]] are more likely to be strong binders than weak binders. This fact was used to train AntiBERTy [@ruffolo2021].

#### Details
This is a repertoire-level enrichment, not a quantitative affinity measurement: raw sequence abundance after selection can correlate poorly with affinity [@paul2026; @makowski2022]. Quantitative NGS-based affinity estimates instead require titration and sorting across measurement bins [@adams2016].

#### Figures
![[Pasted-image-20250203043459.png]]
*Ref [@tan2014]*

#### See also
- [[PLMs cluster antibodies from the same repertoire by V gene and maturation status]]
- [[NGS sequence abundance does not correlate with binding affinity]]
