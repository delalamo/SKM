---
tags:
  - structure-prediction/sampling
  - conformational-dynamics/modeling
  - tm-score
created: "2025-05-18T00:49:42"
modified: "2026-04-20T07:46:00"
---

#### Summary

**Structure prediction outputs from [[Structure prediction]] methods using [[Protein dynamics|protein conformational samplers]] tend to be less accurate (i.e., higher RMSD, lower TM-score) than those from vanilla structure prediction neural networks like AlphaFold and ESMFold** ([@kyrylenko2025], [[Jing et al 2023]]). This also includes features like broken chains (what [@kyrylenko2025] calls "chain ruptures").

#### Figures

![[RMSD-Distribution-Across-Cluster-Representatives---BioEmu-vs-AFSample2.png]]

*Figure from [@kyrylenko2025]*
