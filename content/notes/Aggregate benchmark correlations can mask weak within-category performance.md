---
tags:
  - evidence/measurements
  - prediction/variant-effects
  - prediction/complexes
created: "2026-06-23"
modified: "2026-09-25"
---

#### Summary

**Aggregate benchmark correlations can mask weak within-category performance.** Correlations computed across broad benchmark aggregates can exceed correlations within a biologically or experimentally meaningful subset, so global rank-correlation metrics can overstate practical local usefulness [@woolley2026].

#### Figures

![[plms-poorly-rank-high-fitness-variants.png]]

*Ref [@woolley2026]*

#### Antibody-antigen model ranking

The same distinction appears when ranking [[AlphaFold3]] antibody-antigen decoys by [[DockQ]] [@tadiello2026]. On a matched held-out subset of 1,009 complexes and 50,433 predictions, ABAG-Rank achieved global Spearman ρ = 0.804 but per-complex ρ = 0.178. AlphaFold3's corresponding values were 0.733 and 0.134. Strong pooled correlations therefore coexist with weak ordering within an individual target's ensemble.

| Method | RMSE ↓ | Global ρ ↑ | Per-complex ρ ↑ | AUC, DockQ > 0.23 ↑ | AUC, DockQ > 0.50 ↑ | AUC, DockQ > 0.80 ↑ | Seconds/sample ↓ |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Random | 0.489 | -0.000 | 0.004 | 0.500 | 0.502 | 0.495 | — |
| AlphaFold3 | 0.289 | 0.733 | 0.134 | 0.920 | 0.924 | 0.870 | — |
| DeepRank-Ab | 0.268 | 0.651 | 0.111 | 0.876 | 0.885 | 0.883 | 23.81 |
| ipSAE | 0.482 | 0.487 | 0.049 | 0.759 | 0.761 | 0.711 | 3.44 |
| pDockQ | 0.331 | 0.423 | 0.110 | 0.758 | 0.780 | 0.692 | 1.95 |
| pDockQ2 | 0.201 | 0.664 | 0.096 | 0.890 | 0.918 | **0.915** | — |
| ABAG-Rank | **0.175** | **0.804** | **0.178** | **0.935** | **0.946** | 0.910 | **≤ 0.05** |

*Numerical values from Table 1 of [@tadiello2026], transcribed as text; significance symbols omitted. DeepRank-Ab uses its published default settings. ABAG-Rank timing includes preparation and inference with batch size 10. A dash means no timing was reported.*

Low within-complex correlation does not by itself imply useless top-candidate selection: small DockQ differences can make exact ordering unimportant. The paper separately evaluates top-K retrieval. These are structural-quality metrics, not binding-affinity measurements.

#### See also

- [[Increasing diffusion samples is sufficient to yield correctly predicted antibody-antigen complexes]]
- [[No one-size-fits-all approach to scoring antibody structures]]
- [[Protein structure prediction and design confidence metrics do not correlate with binding affinity]]
