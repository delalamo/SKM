---
tags:
  - protein-language-models/training
  - thermostability/prediction
created: "2026-04-05T17:40:10"
modified: "2026-04-21T07:03:26"
---

#### Summary

**Residue conservation and solvent exposure data perform comparably to [[tags/protein-language-models|PLMs]] at some property prediction tasks** [@tsishyn2025]. The former was assessed using position-specific scoring matrices. However, [[Structure-based methods outperform sequence-based methods on protein stability prediction of point mutants, but not full sequences|as with language models]], they perform worse than [[tags/inverse-folding|inverse folding]] on [[tags/thermostability#Prediction|stability prediction]].

#### Figures

| Method | Model type | All | Stability | Binding | Expression | Activity | Fitness |
|---|---|---|---|---|---|---|---|
| −RSA | STR* | 0.356 | 0.480 | 0.281 | 0.323 | 0.330 | 0.286 |
| LOR | ALI* | 0.427 | 0.447 | 0.375 | 0.390 | 0.452 | 0.414 |
| **RSALOR** | STR & ALI | 0.473 | 0.551 | 0.455 | 0.428 | 0.472 | 0.419 |
| ProSST-2048 [13] | STR & pLM | 0.522 | 0.638 | 0.527 | 0.527 | 0.486 | 0.441 |
| PoET [14] | ALI & pLM | 0.470 | 0.458 | 0.440 | 0.459 | 0.495 | 0.474 |
| SaProt (650M) [19] | STR & pLM | 0.462 | 0.565 | 0.441 | 0.482 | 0.459 | 0.375 |
| VespaG [20] | pLM | 0.461 | 0.479 | 0.415 | 0.450 | 0.489 | 0.440 |
| TranceptEVE (L) [21] | ALI & pLM | 0.450 | 0.424 | 0.405 | 0.447 | 0.489 | 0.458 |
| GEMME [22] | ALI | 0.447 | 0.452 | 0.367 | 0.430 | 0.477 | 0.444 |
| EVE (ensemble) [23] | ALI | 0.431 | 0.410 | 0.382 | 0.398 | 0.466 | 0.446 |
| ESM2 (650M) [24] | pLM | 0.428 | 0.496 | 0.382 | 0.409 | 0.431 | 0.381 |

*Table from [@tsishyn2025]*

#### See also

* [[A subset of residues is sufficient to predict protein dG]]
