---
tags:
  - alphafold3
created: 2025-07-22T10:57:10
modified: "2026-04-21T05:01:15"
---
#### Summary
**[[AlphaFold3]]-generation [[Protein-ligand co-folding|protein-ligand co-folding]] prediction methods can be substantially reduced in size without adversely affecting prediction quality** [@gong2025]. This was found using Protenix. The model was shrunk by reducing the number of blocks and changing how models are sampled, as it was noticed that most blocks do not affect prediction accuracy in any substantial way. The exception is prediction of [[Protein-protein interactions|protein-protein interactions]], which do not work well without [[Multiple sequence alignments|MSAs]].

#### Figures
![[Pasted-image-20250722105406.png]]
*Ref [@gong2025]*
