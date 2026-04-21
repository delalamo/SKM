---
tags:
  - structure-prediction/training
created: "2024-05-05T09:14:54"
modified: "2026-04-21T07:03:26"
---

#### Summary

**RMSD is a poor training objective for protein [[tags/structure-prediction|structure prediction]].** For proteins, [[Frame aligned point error|FAPE]] is better [@baek2021]. For ligands, the fraction of models predicted under a certain RMSD is better [@corso2023]. However, it was used by [@ruffolo2023] to train [[IgFold]] and was apparently effective.
