---
tags:
  - design/developability
  - design/binders
  - biophysics/interactions
created: "2026-09-25"
modified: "2026-09-25"
---

#### Summary

**Redesigning residues outside the intended binding interface can reduce off-target reactivity while preserving on-target recognition** [@chow2026]. This provides a specificity-engineering strategy distinct from improving affinity at the intended interface.

#### Details

The demonstrated example is CARPNN redesign of a de novo CD22 binder. A soluble-protein version of [[ProteinMPNN]] redesigned non-interface residues, followed by structural filtering. The D1.N0 variant retained recombinant CD22 binding and CD22-dependent activation while reducing activation on CD22-negative cells:

| CD22-negative cell line | Parental D1 activation | D1.N0 activation |
| --- | ---: | ---: |
| RPMI-8226 | 42% | 19% |
| HeLa | 48.8% | 8.2% |

These are percentages of activated CAR Jurkat cells, not binding affinities. Primary CAR T-cell experiments also supported reduced off-target activity; the responsible off-target antigen was not identified. The general strategy is not intrinsically limited to a CAR format, but this experiment directly establishes its effect in that setting.

#### See also

- [[Affinity maturation of de novo minibinders introduces mutations far from the active site]] — non-interface changes can affect specificity as well as affinity.
- [[Net charge of CDRs strongly predicts nonspecific binding]]
- [[notes/Antibody developability|Antibody developability]]
