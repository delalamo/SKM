---
tags:
  - ligand-docking
  - structure-prediction/limitations
  - alphafold3
created: 2025-10-27T12:58:04
modified: "2026-04-21T07:03:26"
---

#### Summary

**[[tags/structure-prediction|Protein-ligand co-folding]] methods such as AlphaFold3 struggle to generalize beyond their training sets** (Škrinjar et al 2025 [@krinjar2025; @masters2025]). They continue to dock ligands into the training set poses even when active site residues are heavily mutated [@masters2025].

#### Figures

![[Pasted-image-20250208161420.png]]
*Ref Škrinjar et al 2025 [@krinjar2025]*

![[Pasted-image-20251027125753.png]]
*Ref [@masters2025]*

#### See also

* [[Protein folding neural networks do not extrapolate to new ligand binding sites]]
* [[All-atom structure prediction of RNA is driven by memorization]]
