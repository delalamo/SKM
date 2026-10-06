---
tags:
  - evidence/measurements
  - prediction/variant-effects
  - prediction/complexes
created: "2026-06-23"
modified: "2026-10-05T21:31:49"
---

#### Summary

**Aggregate benchmark correlations can mask weak within-category performance.** Correlations computed across broad benchmark aggregates can exceed correlations within a biologically or experimentally meaningful subset, so global rank-correlation metrics can overstate practical local usefulness [@woolley2026].

#### Figures

![[plms-poorly-rank-high-fitness-variants.png]]
*Ref [@woolley2026]*

| Method | RMSE ↓ | Global ρ ↑ | Per-complex ρ ↑ | AUC, DockQ > 0.23 ↑ | AUC, DockQ > 0.50 ↑ | AUC, DockQ > 0.80 ↑ | Seconds/sample ↓ |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Random | 0.489 | -0.000 | 0.004 | 0.500 | 0.502 | 0.495 | — |
| AlphaFold3 | 0.289 | 0.733 | 0.134 | 0.920 | 0.924 | 0.870 | — |
| DeepRank-Ab | 0.268 | 0.651 | 0.111 | 0.876 | 0.885 | 0.883 | 23.81 |
| ipSAE | 0.482 | 0.487 | 0.049 | 0.759 | 0.761 | 0.711 | 3.44 |
| pDockQ | 0.331 | 0.423 | 0.110 | 0.758 | 0.780 | 0.692 | 1.95 |
| pDockQ2 | 0.201 | 0.664 | 0.096 | 0.890 | 0.918 | **0.915** | — |
| ABAG-Rank | **0.175** | **0.804** | **0.178** | **0.935** | **0.946** | 0.910 | **≤ 0.05** |
*Ref [@tadiello2026] showing per-complex Spearman far lower than global Spearman values across a variety of metrics*

#### See also

- [[Increasing diffusion samples is sufficient to yield correctly predicted antibody-antigen complexes]]
- [[No one-size-fits-all approach to scoring antibody structures]]
- [[Protein structure prediction and design confidence metrics do not correlate with binding affinity]]
