---
tags:
  - structure-prediction/metrics
  - plddt
  - pae
created: "2026-02-20T18:08:22"
modified: "2026-04-20T07:46:00"
---

#### Summary

**[[DiffDock]] confidence is inversely correlated with RMSD** [@corso2023]. Note that the training objective is different: simple cross-entropy training on whether a pose is within 2Å RMSD. A follow-up paper by [[Corso et al 2023b]] found that the confidence of these models is actually a more accurate predictor than the diffusion model itself.

#### See also
* [[pLDDT and PAE inversely correlated with protein dynamics in dynamic naturally occurring proteins, but not de novo proteins]]
