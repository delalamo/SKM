---
tags:
  - design/developability
  - design/binders
  - cell-biology/immune-signaling
created: "2026-09-15"
modified: "2026-09-16T12:00:34"
---

#### Summary

**Redesigning residues outside the intended binding interface can reduce off-target activation by de novo chimaeric antigen receptor (CAR) binders while preserving on-target activity** [@chow2026]. This extends [[Affinity maturation of de novo minibinders introduces mutations far from the active site|non-interface engineering of minibinders]] to specificity.

#### Details

The CARPNN workflow uses a soluble-protein version of [[ProteinMPNN]] and structure-based filtering. Starting from the CD22 binder D1, the authors generated 10,000 sequences and selected 23 for screening. The non-interface variant D1.N0 retained recombinant CD22 binding and CD22-dependent activation while reducing CD69 activation on two CD22-negative cell lines (Figure 6):

| CD22-negative cell line | Parental D1 | D1.N0 |
| --- | ---: | ---: |
| RPMI-8226 | 42% | 19% |
| HeLa | 48.8% | 8.2% |

These are percentages of activated CAR Jurkat cells, not binding affinities. Primary CAR T-cell experiments also supported reduced off-target activity. The responsible off-target antigen remained unidentified.

The cited estimate that approximately 28% of clinical-stage antibodies have off-target reactivity comes from a separate study; a comparable rate for de novo binders is the authors' hypothesis, not a measurement in this screen.

#### See also

- [[Net charge of CDRs strongly predicts nonspecific binding]]
- [[Antibody developability]]
- [[Protein structure prediction and design confidence metrics do not correlate with binding affinity]]
