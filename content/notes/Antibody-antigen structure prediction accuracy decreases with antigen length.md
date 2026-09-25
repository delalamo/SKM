---
tags:
  - prediction/complexes
  - evidence/generalization
created: "2026-09-25"
modified: "2026-09-25"
---

#### Summary

**Antibody–antigen structure prediction accuracy decreases with antigen length across the predictors evaluated by TorchFold** [@torchfold2026, section 4.5]. This concerns recovery of experimentally observed interfaces, not merely a shift in confidence scores.

#### Details

For TorchFold, ranked success at DockQ > 0.23 fell across the following bins, pooled over five benchmarks:

| Antigen residues | Scored interfaces | Successful interfaces (%) |
| --- | ---: | ---: |
| ≤50 | 68 | 74 |
| 51–150 | 228 | 65 |
| 151–300 | 354 | 64 |
| 301–600 | 264 | 57 |
| >600 | 42 | 38 |

Length also covaries with target composition and training coverage; ASD distillation curation excluded antigens longer than 500 residues. This association therefore does not isolate length as a causal factor.

#### See also

- [[Antigen size biases AlphaFold3 antibody-antigen confidence]] — confidence distributions rather than DockQ recovery.
- [[ipTM is sensitive to construct length even when predicted interfaces are unchanged]] — score changes with an unchanged binding mode.
