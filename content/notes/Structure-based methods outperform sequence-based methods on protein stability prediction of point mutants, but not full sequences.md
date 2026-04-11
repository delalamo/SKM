---
tags:
  - thermostability
created: "2026-04-05T17:45:06"
modified: "2026-04-11T06:06:39"
---

#### Summary

**Structure-based methods such as [[Inverse folding]] models outperform sequence-based methods such as [[Protein language models|PLMs]] on protein stability prediction of point mutants, but not full sequences** [^reeves2023]. Among those models, [[ESM-IF]] is the most effective ([^wang2023], [[Paul et al 2023]]). [^tan2023] found that embedding geometry into PLMs can improve stability prediction. In contrast, [^cho2024] found that the PLM [[ESM|ESM-2]] had better Spearman correlations than these inverse folding models to experimental stability measurements when comparing the *de novo* sequences with the same target fold.

#### Details

Comparisons carried out by [^wang2023] were carried out using data from [^rocklin2017] and [^tsuboyama2023].

Data are ambiguous about when [[Rosetta]] or [[ProteinMPNN]] is better ([^reeves2023]; the former was substantially improved by [^dieckhaus2024] following transfer learning on ddG data by [^tsuboyama2023]).

#### Figures

| Model name | Expression | Binding | Activity | Stability | Organismal fitness | Mean |
|---|---|---|---|---|---|---|
| **N. Assays** | 6 | 10 | 31 | 68 | 69 | |
| EVE (ens.) | 0.460 | 0.322 | 0.453 | 0.418 | 0.470 | 0.425 |
| GEMME | 0.382 | 0.361 | 0.490 | 0.518 | 0.469 | 0.444 |
| ProGen2 (ens.) | 0.459 | 0.298 | 0.417 | 0.422 | 0.446 | 0.408 |
| VESPA | 0.483 | 0.378 | 0.472 | 0.501 | 0.468 | 0.460 |
| ProteinMPNN | 0.162 | 0.148 | 0.213 | 0.555 | 0.177 | 0.251 |
| ESM-IF1 | 0.401 | 0.375 | 0.387 | 0.630 | 0.368 | 0.432 |
| Tranception L | 0.441 | 0.329 | 0.462 | 0.473 | 0.459 | 0.433 |
| TranceptEVE | 0.481 | 0.341 | 0.482 | 0.502 | **0.478** | 0.457 |
| StructSeq | **0.549** | **0.399** | **0.498** | **0.633** | 0.468 | **0.509** |

*Figure from [[Paul et al 2023]]*

| Design method | *De Novo* | Natural | All |
|---|---|---|---|
| **GVP** | 0.390 | 0.494 | 0.450 |
| **PiFold** | 0.448 | 0.556 | 0.511 |
| **ProteinMPNN** | 0.428 | 0.605 | 0.531 |
| **ESMIF** | **0.500** | **0.629** | **0.575** |
| **ByProt** | 0.468 | 0.586 | 0.536 |
| **AF-Design** | 0.354 | 0.292 | 0.318 |
| **ESM-Design** | 0.127 | 0.0004 | 0.053 |

*Figure from [^wang2023]*

| Model | Version | TPR↑ DTm 5% | TPR↑ DTm 25% | TPR↑ DTm 50% | TPR↑ DDG 5% | TPR↑ DDG 25% | TPR↑ DDG 50% |
|---|---|---|---|---|---|---|---|
| PROGEN2 | oas | 0.033 | 0.286 | 0.537 | 0.000 | 0.339 | 0.515 |
| | medium | 0.117 | 0.367 | 0.582 | 0.072 | 0.443 | 0.615 |
| | base | 0.212 | 0.362 | 0.585 | **0.231** | 0.408 | 0.621 |
| | large | 0.132 | 0.323 | 0.557 | 0.117 | 0.320 | 0.597 |
| | BFD90 | 0.178 | 0.333 | 0.589 | 0.206 | 0.451 | **0.644** |
| | xlarge | 0.118 | 0.353 | 0.578 | 0.144 | 0.383 | 0.603 |
| TRANCEPTION | medium | 0.188 | 0.359 | 0.564 | 0.083 | 0.367 | 0.527 |
| | large | 0.149 | 0.371 | 0.586 | 0.072 | 0.395 | 0.540 |
| PORTTRANS | bert | 0.131 | 0.364 | 0.586 | 0.122 | 0.424 | 0.635 |
| | bert_bfd | 0.168 | 0.336 | 0.579 | 0.136 | 0.423 | 0.589 |
| | t5_xl_uniref50 | 0.184 | 0.412 | 0.593 | 0.147 | 0.425 | 0.640 |
| | t5_xl_bfd | 0.136 | 0.350 | 0.587 | 0.106 | 0.419 | 0.610 |
| ESM-1V | - | 0.216 | 0.386 | 0.602 | **0.231** | 0.451 | 0.622 |
| ESM-1B | - | 0.151 | 0.402 | 0.606 | 0.211 | 0.424 | 0.642 |
| ESM-IF1 | - | 0.188 | **0.418** | 0.656 | 0.258 | 0.469 | 0.641 |
| ESM-2 | t30 | 0.139 | 0.397 | 0.598 | 0.172 | **0.453** | 0.646 |
| | t33 | 0.239 | 0.407 | 0.601 | 0.181 | 0.438 | 0.637 |
| | t36 | 0.152 | 0.408 | **0.634** | 0.169 | 0.405 | 0.641 |
| | t48 | **0.232** | 0.430 | 0.607 | 0.189 | 0.400 | 0.606 |
| P¹³LG | k20_h1280 | 0.304 | 0.419 | 0.642 | 0.267 | 0.454 | 0.676 |

*Figure from [^tan2023]*

\![[Pasted-image-20241231144322.png]]

*Figure from [^cho2024]*

#### See also

- [[MSA-based structure predictions outperform PLM-based methods]]

[^reeves2023]: Reeves & Kalyaanamoorthy (2023) "Zero-Shot Transfer of Protein Sequence Likelihood Models to Thermostability Prediction." https://doi.org/10.1101/2023.07.17.549396
[^wang2023]: Wang et al. (2023) "PDB-Struct: A Comprehensive Benchmark for Structure-based Protein Design." https://doi.org/10.48550/arXiv.2312.00080
[^tan2023]: Tan et al. (2023) "Multi-level Protein Representation Learning for Blind Mutational Effect Prediction." https://doi.org/10.48550/arXiv.2306.04899
[^cho2024]: Cho et al. (2024) "Implicit modeling of the conformational landscape and sequence allows scoring and generation of stable proteins." https://doi.org/10.1101/2024.12.20.629706
[^rocklin2017]: Rocklin et al. (2017) "Global analysis of protein folding using massively parallel design, synthesis, and testing." *Science*. https://doi.org/10.1126/science.aan0693
[^tsuboyama2023]: Tsuboyama et al. (2023) "Mega-scale experimental analysis of protein folding stability in biology and design." *Nature*. https://doi.org/10.1038/s41586-023-06328-6
[^dieckhaus2024]: Dieckhaus et al. (2024) "Transfer learning to leverage larger datasets for improved prediction of protein stability changes." *Proceedings of the National Academy of Sciences*. https://doi.org/10.1073/pnas.2314853121
