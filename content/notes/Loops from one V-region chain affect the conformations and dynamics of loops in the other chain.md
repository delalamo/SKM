---
tags:
  - antibody-structure-prediction/cdr
created: "2026-03-16T11:53:13"
modified: "2026-04-21T07:28:09"
---
#### Summary
**Loops from one V-region chain affect the conformations and dynamics of loops in the other chain** (Guloglu and [@guloglu2023; @tharp2026]). For example, light chain loops can affect the dynamics of [[Complementarity-determining regions#CDRH3|CDRH3]] (Guloglu and [@guloglu2023]). Longer CDRL1 loops and shorter CDRL3 loops correlate with restricted CDRH3 dynamics. In contrast, lengths of other loops had a lesser impact and were less dynamic albeit not entirely static. This is also consistent with observations from MD simulations [@fernandezquintero2020]. [@tharp2026] show an example of strong [[epistasis|epistasis]] between light chain residues that facilitate a reconfiguration of CDRH2.

#### Details
Only CDRH3 is flexible based on [[Metadynamics]] simulations on 8 antibody structures (Guloglu and [@guloglu2023]). The least flexible H3 loop out of those simulations is found in 45% of frames, whereas the most flexible ones never revisit the crystallized conformation.

#### See also
- [[Deep learning methods produce different CDRH3 conformers]]
- [[Light chain coherence]]
- [[Inclusion of adjacent loops can improve CDRH3 structural modeling]]
