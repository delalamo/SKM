---
tags:
  - protein-design/misc
created: "2026-04-05T17:26:46"
modified: "2026-04-05T23:14:54"
---

#### Summary

**Averaging logits from multiple DL models can lead to substantial improvements in fitness and stability prediction.** The method TranceptEVE, which combines probabilities from [[EVE]] and [[Tranception]], is the state of the art method for predicting protein [[Fitness prediction|fitness]] and [[Stability and thermostability|thermostability]] (as judged by [[ProteinGym]]; Notin et al 2022[^notin2022]). Likewise, adding probabilities from [[ESM-IF]] further improves this method ([[8PbTU4exnV|Paul et al 2023]]). Nijkamp et al 2023[^nijkamp2023] found that ensembles of [[ProGen]] models outperform individual models on a range of tasks.

#### Figures

| Model name | Expression | Binding | Activity | Stability | Organismal fitness | Mean |
|---|---|---|---|---|---|---|
| **N. Assays** | 6 | 10 | 31 | 68 | 69 | n/a |
| EVE (ens.) | 0.460 | 0.322 | 0.453 | 0.418 | 0.470 | 0.425 |
| GEMME | 0.382 | 0.361 | 0.490 | 0.518 | 0.469 | 0.444 |
| ProGen2 (ens.) | 0.459 | 0.298 | 0.417 | 0.422 | 0.446 | 0.408 |
| VESPA | 0.483 | 0.378 | 0.472 | 0.501 | 0.468 | 0.460 |
| ProteinMPNN | 0.162 | 0.148 | 0.213 | 0.555 | 0.177 | 0.251 |
| ESM-IF1 | 0.401 | 0.375 | 0.387 | 0.630 | 0.368 | 0.432 |
| Tranception L | 0.441 | 0.329 | 0.462 | 0.473 | 0.459 | 0.433 |
| TranceptEVE | 0.481 | 0.341 | 0.482 | 0.502 | **0.478** | 0.457 |
| StructSeq | **0.549** | **0.399** | **0.498** | **0.633** | 0.468 | **0.509** |

*Figure from [[8PbTU4exnV|Paul et al 2023]]*

#### See also

- [[Concatenating sequence and structural features is not effective for sequence recovery]]
- [[Structure-based methods outperform sequence-based methods on protein stability prediction of point mutants, but not full sequences]]

[^notin2022]: Notin et al. (2022) "TranceptEVE: Combining Family-specific and Family-agnostic Models of Protein Sequences for Improved Fitness Prediction." https://doi.org/10.1101/2022.12.07.519495
[^nijkamp2023]: Nijkamp et al. (2023) "ProGen2: Exploring the boundaries of protein language models." *Cell Systems*. https://doi.org/10.1016/j.cels.2023.10.002
