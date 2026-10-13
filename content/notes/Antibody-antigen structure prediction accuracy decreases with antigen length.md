---
tags:
  - prediction/complexes
  - evidence/generalization
created: "2026-09-25"
modified: "2026-10-09T06:13:32"
---

#### Summary

**[[tags/antibodies|Antibody]]–antigen [[notes/Structure prediction|structure prediction]] accuracy decreases with antigen length across the predictors evaluated by TorchFold** (section 4.5) [@torchfold2026].

#### Details

For TorchFold, ranked success at [[DockQ]] > 0.23 fell across the following bins, pooled over five benchmarks:

| Antigen residues | Scored interfaces | Successful interfaces (%) |
| --- | ---: | ---: |
| ≤50 | 68 | 74 |
| 51–150 | 228 | 65 |
| 151–300 | 354 | 64 |
| 301–600 | 264 | 57 |
| >600 | 42 | 38 |

#### See also

- [[Antigen size biases AlphaFold3 antibody-antigen confidence]] — confidence distributions rather than DockQ recovery.
- [[ipTM is sensitive to construct length even when predicted interfaces are unchanged]] — score changes with an unchanged binding mode.
- [[Protein-protein interactions]]
