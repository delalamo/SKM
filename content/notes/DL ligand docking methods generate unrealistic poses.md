---
tags:
  - structure-prediction/limitations
  - ligand-docking
created: 2024-05-05T08:54:15
modified: "2026-04-20T07:16:03"
---

#### Summary

**Deep learning is significantly worse at maintaining the shape of the ligand in general than classical approaches** [^buttenschoen2023]. For [[Diffusion models|diffusion]]-based prediction, this can be partially fixed with m[[Diffusion guidance|guidance]].

#### Figures

![[Pasted-image-20231126101415.png|500]]
*Ref [^buttenschoen2023]*

#### See also

- [[DL models excel at finding pockets but not docking into them]]
- [[DL structure tools introduce chiral errors such as swapped chiral centers, D-amino acids, and cis-amide bonds]]

[^buttenschoen2023]: Buttenschoen et al. (2024) "PoseBusters: AI-based docking methods fail to generate physically valid poses or generalise to novel sequences." Chemical Science. https://doi.org/10.1039/d3sc04185a
