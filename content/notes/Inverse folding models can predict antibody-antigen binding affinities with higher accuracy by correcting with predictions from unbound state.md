---
tags:
  - antibody-structure-prediction/complex-prediction
  - antibody-antigen-interactions/binding-affinity
title: Accounting for the unbound state improves inverse-folding prediction of binding-affinity changes
created: "2025-02-04T03:00:01"
modified: "2026-08-19T16:32:04"
---

#### Summary

**Accounting explicitly for both bound and unbound states improves [[inverse-folding|inverse-folding]] estimates of mutation-induced changes in protein-protein binding free energy** [@jiao2025]. 

#### Details
Boltzmann Alignment subtracts unbound-state log-likelihood contributions and improved unsupervised and supervised Spearman correlations on SKEMPI v2 from 0.2632 to 0.3201 and from 0.4324 to 0.5134, respectively [@jiao2025]. The method was also evaluated for [[antibodies|antibody]] optimization.

#### See also

* [[Zero-shot protein stability prediction using inverse folding models can be improved by subtracting predictions from residue in isolation]]
