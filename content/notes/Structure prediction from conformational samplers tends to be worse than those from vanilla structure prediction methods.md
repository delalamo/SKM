---
tags:
  - protein-folding/misc
created: "2025-05-18T00:49:42"
modified: "2026-04-05T23:36:09"
---

#### Summary

**Structure prediction outputs from [[Structure prediction]] methods using [[Protein dynamics|protein conformational samplers]] tend to be less accurate (i.e., higher RMSD, lower TM-score) than those from vanilla structure prediction neural networks like AlphaFold and ESMFold** ([^kyrylenko2025], [[Jing et al 2023]]). This also includes features like broken chains (what [^kyrylenko2025] calls "chain ruptures").

#### Figures

![](/assets/RMSD-Distribution-Across-Cluster-Representatives---BioEmu-vs-AFSample2.png)

*Figure from [^kyrylenko2025]*

[^kyrylenko2025]: Kyrylenko et al. (2025) "Sampling and ranking of protein conformations using machine learning techniques do not improve the quality of rigid protein-protein docking." https://doi.org/10.1101/2025.05.13.652389
