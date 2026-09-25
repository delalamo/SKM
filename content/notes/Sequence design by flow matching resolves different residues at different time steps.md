---
tags:
  - design/sequence-generation
  - inference/sampling-and-search
  - model-analysis/interpretability
created: "2026-09-25"
modified: "2026-09-25"
---

#### Summary

**Sequence design by flow matching can resolve different residue identities at different time steps, with some positions revising their preferred amino acid late in generation** [@tartici2026]. Solvent-exposed positions can remain less committed than buried positions.

#### Details

Inverse FoldDir provides a structure-conditioned example: it updates amino-acid probability distributions at all designable positions. In a representative bromodomain (PDB 2D9E, chain A), confidence rises and entropy falls at different rates along the sequence.

Across 1,120 CATH test proteins, more than one-quarter of positions changed their predicted flow direction, and approximately 7% changed more than once. Approximately 4% of predicted residue changes occurred in the second half of generation. Unresolved positions changed most often, while solvent exposure was associated with more updates.

These are inference trajectories, not the temporal order of physical protein folding. They differ from [[Joint sequence-structure diffusion or flow matching models show superior performance when designing structure at the beginning and sequence near the end|scheduling sequence after structure in joint models]].

#### Benchmark scope

The released model used CATH chains plus about 2.8 million filtered predicted structures, versus about 12 million for [[ESM-IF]] [@tartici2026; @hsu2022]. The training corpora differ, and the baselines were not retrained on matched data. Better reported refolding scores therefore do not isolate an architectural advantage.

#### Figures

![[inverse-folddir-residue-convergence.png]]
*Figure 2A–C from [@tartici2026]: maximum amino-acid probability, the gap between the top two probabilities, and entropy across generation.*

#### See also

- [[Flow matching]]
- [[Running inverse folding in a random order leads to greater sequence recovery than running in a fixed-order]]
