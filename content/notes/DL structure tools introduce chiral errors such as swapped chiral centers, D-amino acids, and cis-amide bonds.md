---
tags:
  - structure-prediction/limitations
  - diffusion-guidance/structure-prediction
created: 2024-05-05T08:53:40
modified: "2026-04-20T10:13:23"
---
#### Summary
**Deep learning [[Structure prediction|structure prediction]] tools introduce errors such as swapped chiral centers, steric clashes, and cis-amide bonds**[^abramson2024][^fernandezquintero2023]. [[Diffusion models|Diffusion]]-based structure prediction methods are able to overcome this with [[Diffusion guidance|guidance]].

#### Details
Antibody-specific tools include AbLooper, DeepAb, [[IgFold]], [[ImmuneBuilder]], and MOE homology modeler. Only DeepAb and ImmuneBuilder did not introduce D-amino acids.

#### See also
- [[DL ligand docking methods generate unrealistic poses]]

[^abramson2024]: Abramson et al. (2024) "Accurate structure prediction of biomolecular interactions with AlphaFold 3." *Nature*. https://doi.org/10.1038/s41586-024-07487-w
[^fernandezquintero2023]: Fernández-Quintero et al. (2023) "Challenges in antibody structure prediction." *mAbs*. https://doi.org/10.1080/19420862.2023.2175319
