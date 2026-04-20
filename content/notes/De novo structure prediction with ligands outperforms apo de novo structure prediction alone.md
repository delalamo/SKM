---
tags:
  - protein-backbone-design/designability
created: "2024-05-08T18:00:00"
modified: "2026-04-20T07:16:03"
---

#### Summary

***De novo* structure prediction with ligands leads to more accurate prediction of structure compared to prediction without ligands** [^qiao2022][^krishna2024]. Predictions of ligand-bound structures using RosettaFold all-atom were on average more accurate than those using default RosettaFold. [^qiao2022] found that predicted structures without ligands adopted the apo conformation, while those with the ligand adopted the holo conformation. In contrast, AlphaFold2 predictions were somewhere in the middle, and had worse RMSDs/TM-scores for holo but not apo state.

#### Figures

![[Pasted-image-20240419125413.png]]

*Figure S4E from [^krishna2024]*

#### See also

- [[AlphaFold2 predicts the holo form of proteins in most cases]]
- [[AlphaFold2 predicts Apo conformations with poorer RMSD than holo conformations]]
- [[Including ligands restrains design of catalytically active residues]]

[^qiao2022]: Qiao et al. (2024) "State-specific protein–ligand complex structure prediction with a multiscale deep generative model." Nature Machine Intelligence. https://doi.org/10.1038/s42256-024-00792-z
[^krishna2024]: Krishna et al. (2024) "Generalized biomolecular modeling and design with RoseTTAFold All-Atom." *Science*. https://doi.org/10.1126/science.adl2528
