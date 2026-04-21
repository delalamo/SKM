---
tags:
  - structure-prediction/limitations
created: "2024-06-04T01:01:27"
modified: "2026-04-21T05:01:15"
---

## Summary

**Protein folding neural networks do not extrapolate to new ligand binding sites** ([@doelsnitz2024], [@drr2024]). [[AlphaFold2]] could not predict a new calcium-binding site in an engineered protein, and instead introduced a fictitious salt bridge [@doelsnitz2024]. Separately, neither [[AlphaFold3]] nor [[RosettaFold|RosettaFold-AA]] could predict that a binding site prefers cobalt over copper [@drr2024].

## Figures

![[Crystal-Structure.png]]
*Ref [@doelsnitz2024]*
