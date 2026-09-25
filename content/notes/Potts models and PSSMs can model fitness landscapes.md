---
title: Potts models and PSSMs can model fitness landscapes
tags:
  - prediction/variant-effects
  - evolution/mutation-effects
created: "2024-04-29T14:38:30"
modified: "2026-09-25"
---
#### Summary
 **[[Potts models]] derived from [[Multiple sequence alignments|MSAs]] can be used as the basis to model fitness landscapes** [@sesta2023]. This is proposed to take epistatic effects into account. Fannjiang and [@fannjiang2023] give several citations for these correlating with actual fitness landscapes. However, [[MSA Transformer]] seemed to outperform Potts in this regard [@lupo2022; @sgarbossa2023]. While PSSMs can also be used, they do not account for any higher-order interactions.

#### Altered specificity

A context-free PSSM can also be [[Differences between context-free and context-aware scores can enrich altered-specificity variants|combined with a negative context-aware contribution to prioritize specificity changes]], rather than simply averaging scores that favor the native function.
