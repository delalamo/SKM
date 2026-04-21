---
tags:
  - structure-prediction/limitations
  - ligand-docking
created: 2024-05-05T08:54:15
modified: "2026-04-21T07:28:09"
---

#### Summary

**Deep learning is significantly worse at maintaining the shape of the ligand in general than classical approaches** [@buttenschoen2023]. For [[diffusion-models|diffusion]]-based prediction, this can be partially fixed with m[[diffusion-guidance|guidance]].

#### Figures

![[Pasted-image-20231126101415.png|500]]
*Ref [@buttenschoen2023]*

#### See also

- [[DL models excel at finding pockets but not docking into them]]
- [[DL structure tools introduce chiral errors such as swapped chiral centers, D-amino acids, and cis-amide bonds]]
