---
tags:
  - structure-prediction/sampling
  - conformational-dynamics/modeling
  - tm-score
created: "2025-05-18T00:49:42"
modified: "2026-04-21T07:28:09"
---

#### Summary

**Structure prediction outputs from [[structure-prediction|Structure prediction]] methods using [[Protein dynamics|protein conformational samplers]] tend to be less accurate (i.e., higher RMSD, lower TM-score) than those from vanilla structure prediction neural networks like AlphaFold and ESMFold** [@kyrylenko2025; @jing2023b]. This also includes features like broken chains (what [@kyrylenko2025] calls "chain ruptures").

#### Figures

![[RMSD-Distribution-Across-Cluster-Representatives---BioEmu-vs-AFSample2.png]]

*Ref [@kyrylenko2025]*
