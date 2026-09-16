---
tags:
  - design/inverse-folding
  - inference/sampling-and-search
  - model-analysis/interpretability
created: "2026-09-15"
modified: "2026-09-16T12:00:34"
---

#### Summary

**[[Inverse FoldDir]] resolves amino-acid identities asynchronously during [[Flow matching|flow matching]], and positions can revise their preferred residue late in generation** [@tartici2026]. Solvent-exposed positions undergo more updates than buried positions, consistent with weaker structural constraints on their identities.

#### Details

The model updates a probability distribution over amino acids at every designable position. In a representative bromodomain (PDB 2D9E, chain A), maximum probabilities rise and entropy falls at different rates across the sequence (Figure 2A-C).

Across 1,120 CATH test proteins, more than one-quarter of positions changed the direction of their predicted Dirichlet flow during generation; approximately 7% changed more than once. Approximately 4% of predicted residue changes occurred in the second half of denoising. Positions with unresolved experimental coordinates showed the most identity changes, while solvent exposure was associated with more probability updates (Figure 3; Figure S1).

These are observations about model inference, not a temporal ordering of physical protein folding. They concern sequence design on a fixed backbone, whereas [[Joint sequence-structure diffusion or flow matching models show superior performance when designing structure at the beginning and sequence near the end|delaying sequence design in joint sequence-structure models]] is a separate scheduling result.

#### Figures

![[inverse-folddir-residue-convergence.png]]
*Figure 2A-C from [@tartici2026]: maximum amino-acid probability, margin between the top two probabilities, and entropy over the denoising trajectory.*

#### See also

- [[Running inverse folding in a random order leads to greater sequence recovery than running in a fixed-order]]
- [[Sequence recovery in inverse folding models is not correlated with self-consistency of generated designs]]
