---
tags:
  - design/sequence-generation
  - inference/sampling-and-search
  - model-analysis/interpretability
created: "2026-09-25"
modified: "2026-09-25"
---

#### Summary

**Sequence design by [[Flow matching|flow matching]] can resolve different residue identities at different time steps, with some positions revising their preferred amino acid late in generation** [@tartici2026]. Solvent-exposed positions can remain less committed than buried positions.

#### Figures

![[inverse-folddir-residue-convergence.png]]
*Ref [@tartici2026]*

#### See also

- [[Running inverse folding in a random order leads to greater sequence recovery than running in a fixed-order]]
