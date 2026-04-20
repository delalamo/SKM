---
tags:
  - structure-prediction/sampling
  - conformational-dynamics/modeling
  - tm-score
created: "2025-05-18T00:49:42"
modified: "2026-04-20T08:16:13"
---

#### Summary

**Structure prediction outputs from [[Structure prediction]] methods using [[Protein dynamics|protein conformational samplers]] tend to be less accurate (i.e., higher RMSD, lower TM-score) than those from vanilla structure prediction neural networks like AlphaFold and ESMFold** ([^kyrylenko2025], [[Jing et al 2023]]). This also includes features like broken chains (what [^kyrylenko2025] calls "chain ruptures").

#### Figures

![[RMSD-Distribution-Across-Cluster-Representatives---BioEmu-vs-AFSample2.png]]

*Ref [^kyrylenko2025]*

[^kyrylenko2025]: Stratiichuk et al. (2025) "Sampling and Ranking of Protein Conformations Using Machine Learning Techniques Do Not Improve the Quality of Rigid Protein–Protein Docking." Journal of Chemical Information and Modeling. https://doi.org/10.1021/acs.jcim.5c01765
