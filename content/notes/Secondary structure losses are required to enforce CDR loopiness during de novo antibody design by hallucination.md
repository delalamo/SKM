---
tags:
  - antibodies/engineering-and-design
created: 2025-12-19T11:23:25
modified: "2026-04-20T08:16:13"
---

#### Summary
**Secondary structure losses are required to enforce [[Complementarity-determining regions|CDR]] loopiness during [[De novo antibody design|de novo antibody design]] by [[Inversion of protein folding neural networks|hallucination]]** [^millefragoso2025]. Note that the alpha-helical term was originally introduced in BindCraft [^pacesa2025].

#### Details
The alpha-helical loss penalizes beta carbon atoms in $i, i+3$ pairs from falling in the 2.0 to 6.2 Å range via the distogram, while the beta-sheet loss penalizes $i, i+3$ pairs from falling in the 9.75 to 11.5 Å range.

#### Figures
![[Pasted-image-20251027120357.png]]
*Ref [^millefragoso2025]*

#### See also
* [[Paratope losses are required to enforce CDR-mediated antigen binding during de novo antibody design by hallucination]]

[^millefragoso2025]: Mille-Fragoso et al. (2025) "Efficient generation of epitope-targeted de novo antibodies with Germinal." https://doi.org/10.1101/2025.09.19.677421
[^pacesa2025]: Pacesa et al. (2025) "One-shot design of functional protein binders with BindCraft." *Nature*. https://doi.org/10.1038/s41586-025-09429-6
