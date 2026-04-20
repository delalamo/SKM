---
tags:
  - structure-prediction/limitations
created: "2024-06-04T01:01:27"
modified: "2026-04-20T08:16:13"
---

## Summary

**Protein folding neural networks do not extrapolate to new ligand binding sites** ([d'Oelsnitz et al 2024][^doelsnitz2024], [Dürr & Rothlisberger 2024][^drr2024]). [[AlphaFold2]] could not predict a new calcium-binding site in an engineered protein, and instead introduced a fictitious salt bridge[^doelsnitz2024]. Separately, neither [[AlphaFold3]] nor [[RosettaFold|RosettaFold-AA]] could predict that a binding site prefers cobalt over copper ([Dürr & Rothlisberger 2024][^drr2024]).

## Figures

![[Crystal-Structure.png]]
*Ref [d'Oelsnitz et al 2024][^doelsnitz2024]*

[^doelsnitz2024]: d’Oelsnitz et al. (2024) "Biosensor and machine learning-aided engineering of an amaryllidaceae enzyme." *Nature Communications*. https://doi.org/10.1038/s41467-024-46356-y
[^drr2024]: Dürr & Rothlisberger (2024) "Predicting metal-protein interactions using cofolding methods: Status quo." https://doi.org/10.1101/2024.05.28.596236
