---
tags:
  - antibodies/engineering-and-design
created: 2025-12-19T11:23:25
modified: "2026-04-21T05:01:15"
---

#### Summary
**Secondary structure losses are required to enforce [[Complementarity-determining regions|CDR]] loopiness during [[De novo antibody design|de novo antibody design]] by [[Inversion of protein folding neural networks|hallucination]]** [@millefragoso2025]. Note that the alpha-helical term was originally introduced in BindCraft [@pacesa2025].

#### Details
The alpha-helical loss penalizes beta carbon atoms in $i, i+3$ pairs from falling in the 2.0 to 6.2 Å range via the distogram, while the beta-sheet loss penalizes $i, i+3$ pairs from falling in the 9.75 to 11.5 Å range.

#### Figures
![[Pasted-image-20251027120357.png]]
*Ref [@millefragoso2025]*

#### See also
* [[Paratope losses are required to enforce CDR-mediated antigen binding during de novo antibody design by hallucination]]
