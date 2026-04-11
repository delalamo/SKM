---
tags:
  - conformational-dynamics/kinetics
created: "2024-07-15T03:47:57"
modified: "2026-04-11T07:27:50"
---
#### Summary
**Transition matrices between metastable states can accurately approximate a protein's kinetics if the lag time used to build those matrices exceeds the relaxation time within those states** [^zwanzig1983]. This informs the lag time used when running [[Time-lagged independent component analysis|tICA]] and building [[Markov State Models|Markov state models]]. A concrete test that can be run is the [[Chapman-Kolmogorov test]].

[^zwanzig1983]: Zwanzig (1983) "From classical dynamics to continuous time random walks." *Journal of Statistical Physics*. https://doi.org/10.1007/BF01012300
