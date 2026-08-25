---
tags:
  - alphafold3
  - protein-protein-interactions
  - variant-effect-prediction
created: "2026-08-25"
modified: "2026-08-25T10:16:02"
---
#### Summary
**Intermediate [[alphafold3|Boltz-2]] representations can support a separate predictor of [[protein-protein-interactions|protein-protein]] $\Delta G$ and $\Delta\Delta G$ even though the native affinity module transfers poorly** [@park2026prefold]. PreFold-dG aggregates residue-level embeddings with inter-residue-distance weighting and predicts $\Delta G$ directly. It achieved state-of-the-art results on established benchmarks and remained robust on independent test sets; ablations indicated that all intermediate representations contributed, with different importance for $\Delta G$ and $\Delta\Delta G$.

#### See also
- [[The Boltz-2 affinity module cannot be effectively repurposed for PPI affinity prediction]]
- [[Structure prediction uncertainty metrics as energy functions]]
