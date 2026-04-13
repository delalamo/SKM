---
tags:
  - protein-folding/misc
created: "2026-04-05T17:32:01"
modified: "2026-04-11T07:41:30"
---

#### Summary

**Deep learning models such as DiffDock are SOTA at finding pockets but are outperformed by traditional methods at getting the ligand pose right** [^yu2022]. These results are in ground truth pockets and do not look at ESMFold pockets. This is suspected to be due to their lack of inductive biases for identifying interactions that drive high affinity [^errington2024].

#### Figures

![[Pasted-image-20241105050419.png]]

*Figure from [^errington2024]*

| | Method | Top-1 RMSD(Å) % < 1Å (↑) | Top-1 RMSD(Å) % < 2Å (↑) | Top-1 RMSD(Å) Med. (↓) | Top-5 RMSD(Å) % < 1Å (↑) | Top-5 RMSD(Å) % < 2Å (↑) | Top-5 RMSD(Å) Med. (↓) |
|---|---|---|---|---|---|---|---|
| **Deep Learning** | EquiBind | - | 5.5 ± 1.2 | 6.2 ± 0.3 | - | - | - |
| | TANKBind | | 20.4 ± 2.1 | 4.0 ± 0.2 | | 24.5 ± 2.1 | 3.4 ± 0.1 |
| | TANKBind* | 2.66 ± 0.26 | 18.18 ± 0.6 | 4.2 ± 0.05 | 4.13 ± 0.0 | 20.39 ± 0.45 | 3.5 ± 0.04 |
| | DiffDock | | 38.2 ± 2.5 | 3.30 ± 0.3 | | 44.7 ± 2.6 | 2.40 ± 0.2 |
| | DiffDock* | 15.41 ± 0.49 | 36.62 ± 0.35 | 3.31 ± 0.03 | 21.58 ± 0.38 | 44.19 ± 0.49 | 2.37 ± 0.06 |
| **Traditional** | Fpocket + Uni-dock | 13.33 ± 0.4 | 18.7 ± 0.13 | 13.2 ± 0.26 | 19.16 ± 0.39 | 27.32 ± 0.69 | 8.3 ± 0.25 |
| | P2Rank + Uni-dock | 19.31 ± 1.07 | 28.6 ± 1.17 | 6.4 ± 0.22 | 27.76 ± 1.03 | 39.18 ± 1.03 | 3.76 ± 0.06 |
| | PointSite + Uni-dock | 21.36 ± 1.65 | 32.12 ± 0.93 | 5.54 ± 0.46 | 31.38 ± 0.86 | 46.06 ± 0.69 | 2.52 ± 0.18 |
| **Better Pocket + Traditional** | DiffDock* + Uni-dock | 25.49 ± 0.6 | 38.93 ± 0.23 | 4.14 ± 0.07 | 36.97 ± 1.05 | 51.07 ± 1.06 | 1.93 ± 0.12 |
| | GT pocket + Uni-dock | 32.77 ± 0.38 | 51.11 ± 0.6 | 1.89 ± 0.04 | 47.5 ± 0.23 | 67.59 ± 0.94 | 1.11 ± 0.02 |

*Figure from [^yu2022]*

#### See also

- [[DL ligand docking methods generate unrealistic poses]]
- [[The Evoformer can calculate ligand-binding residues]]
- [[Protein-ligand co-folding methods do not generalize beyond their training set]]

[^yu2022]: Yu et al. (2023) "Do Deep Learning Models Really Outperform Traditional Approaches in Molecular Docking?." https://doi.org/10.48550/arXiv.2302.07134
[^errington2024]: Errington et al. (2024) "Assessing interaction recovery of predicted protein-ligand poses." https://doi.org/10.48550/ARXIV.2409.20227
