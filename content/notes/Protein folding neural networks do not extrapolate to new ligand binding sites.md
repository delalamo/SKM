---
tags:
  - structure-prediction/limitations
created: "2024-06-04T01:01:27"
modified: "2026-04-20T07:46:00"
---

## Summary

**Protein folding neural networks do not extrapolate to new ligand binding sites** (d'Oelsnitz et al 2024 [@doelsnitz2024], Dürr & Rothlisberger 2024 [@drr2024]). [[AlphaFold2]] could not predict a new calcium-binding site in an engineered protein, and instead introduced a fictitious salt bridge[@doelsnitz2024]. Separately, neither [[AlphaFold3]] nor [[RosettaFold|RosettaFold-AA]] could predict that a binding site prefers cobalt over copper (Dürr & Rothlisberger 2024 [@drr2024]).

## Figures

![[Crystal-Structure.png]]
*Figure from d'Oelsnitz et al 2024 [@doelsnitz2024]*
