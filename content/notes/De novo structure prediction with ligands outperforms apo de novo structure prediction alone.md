---
tags:
  - protein-backbone-design/designability
created: "2024-05-08T18:00:00"
modified: "2026-04-20T07:46:00"
---

#### Summary

***De novo* structure prediction with ligands leads to more accurate prediction of structure compared to prediction without ligands** [@qiao2022; @krishna2024]. Predictions of ligand-bound structures using RosettaFold all-atom were on average more accurate than those using default RosettaFold. [@qiao2022] found that predicted structures without ligands adopted the apo conformation, while those with the ligand adopted the holo conformation. In contrast, AlphaFold2 predictions were somewhere in the middle, and had worse RMSDs/TM-scores for holo but not apo state.

#### Figures

![[Pasted-image-20240419125413.png]]

*Figure S4E from [@krishna2024]*

#### See also

- [[AlphaFold2 predicts the holo form of proteins in most cases]]
- [[AlphaFold2 predicts Apo conformations with poorer RMSD than holo conformations]]
- [[Including ligands restrains design of catalytically active residues]]
