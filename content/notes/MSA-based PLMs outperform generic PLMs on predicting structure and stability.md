---
tags:
  - protein-design/misc
created: "2026-04-05T17:51:40"
modified: "2026-04-05T23:36:09"
---
#### Summary
 **MSA-based [[Protein language models|PLMs]] such as [[MSA Transformer]] and the [[Evoformer]] are more effective than generic PLMs at predicting [[Structure prediction|structure]]** [^hu2022]** and [[Stability and thermostability|stability]]** [^tan2023]. [^notin2023] found that [[MSA Transformer]] outperformed [[Protein language models|PLMs]] like [[ESM]]2-15B on almost all benchmarks in [[ProteinGym]].

#### Details
Conclusions from [^hu2022] about the representations from [[Evoformer]] as a standalone ML model:
* Structure prediction (superior to [[ESM]]-1b and [[MSA Transformer]])
* Miniprotein stability prediction (superior to ESM-1b and MSA transformer)
* Function annotation prediction (ESM-1b outperforms EvoFormer and MSA-Transformer)
* Fitness score prediction (worse than ESM-1b and MSA-transformer)
* Residue-level prediction

#### Figures
| Category | Model | Version | # Params (M) | ρ Single | ρ Double | ρ All | ρ Prokaryote | ρ Human | ρ Eukaryote | ρ Virus |
|---|---|---|---|---|---|---|---|---|---|---|
| MSA | SITEINDEP | - | - | 0.378 | 0.322 | 0.378 | 0.343 | 0.375 | 0.401 | **0.406** |
| | EVMUTATION | - | - | 0.423 | `0.401` | 0.423 | 0.499 | 0.396 | 0.429 | 0.381 |
| | WAVENET | - | - | 0.399 | 0.344 | 0.400 | 0.492 | 0.373 | 0.442 | 0.321 |
| | DEEPSEQUENCE | - | - | **0.411** | 0.357 | **0.415** | 0.497 | 0.396 | 0.461 | 0.332 |
| | MSA-TRANSFORMER | msa1 | 100 | 0.310 | 0.232 | 0.308 | 0.292 | 0.302 | 0.392 | 0.278 |
| | | msa1b | 100 | 0.291 | 0.275 | 0.290 | 0.268 | 0.282 | 0.365 | 0.279 |
| non-MSA | RITA | small | 85 | 0.324 | 0.211 | 0.329 | 0.311 | 0.314 | 0.330 | 0.372 |
| | | medium | 300 | 0.372 | 0.237 | 0.377 | 0.356 | 0.370 | 0.399 | 0.398 |
| | | large | 680 | 0.372 | 0.227 | 0.383 | 0.353 | 0.380 | 0.404 | 0.405 |
| | | xlarge | 1,200 | 0.385 | 0.234 | 0.389 | 0.405 | 0.364 | 0.393 | `0.407` |
| | PROGEN2 | small | 151 | 0.346 | 0.249 | 0.352 | 0.364 | 0.376 | 0.396 | 0.273 |
| | | medium | 764 | 0.394 | 0.274 | 0.395 | 0.434 | 0.393 | 0.411 | 0.346 |
| | | base | 764 | 0.389 | 0.323 | 0.394 | 0.426 | 0.396 | 0.427 | 0.335 |
| | | large | 2,700 | 0.396 | 0.333 | 0.396 | 0.431 | 0.396 | 0.436 | 0.336 |
| | | xlarge | 6,400 | 0.404 | 0.358 | 0.404 | 0.480 | 0.349 | 0.452 | 0.383 |
| | PORTTRANS | bert | 420 | 0.339 | 0.279 | 0.336 | 0.403 | 0.300 | 0.345 | 0.317 |
| | | bert_bfd | 420 | 0.311 | 0.336 | 0.308 | 0.471 | 0.328 | 0.338 | 0.087 |
| | | t5_xl_uniref50 | 3,000 | 0.384 | 0.284 | 0.378 | 0.485 | 0.375 | 0.369 | 0.277 |
| | | t5_xl_bfd | 3,000 | 0.355 | 0.356 | 0.351 | 0.490 | 0.399 | 0.349 | 0.131 |
| | TRANCEPTION | large | 700 | 0.399 | 0.398 | 0.406 | 0.447 | 0.369 | 0.426 | 0.407 |
| | ESM-1V | - | 650 | 0.376 | 0.290 | 0.372 | 0.496 | 0.409 | 0.398 | 0.233 |
| | ESM-1B | - | 650 | 0.371 | 0.325 | 0.366 | **0.507** | 0.416 | 0.360 | 0.150 |
| | ESM-IF1 | - | 142 | 0.359 | 0.279 | 0.368 | 0.445 | 0.358 | 0.339 | 0.322 |
| | ESM-2 | t30 | 150 | 0.345 | 0.296 | 0.344 | 0.437 | **0.419** | 0.401 | 0.045 |
| | | t33 | 650 | 0.392 | 0.317 | 0.389 | 0.515 | `0.433` | **0.454** | 0.155 |
| | | t36 | 3,000 | 0.384 | 0.261 | 0.383 | 0.495 | 0.419 | 0.429 | 0.195 |
| | | t48 | 15,000 | 0.394 | 0.313 | 0.391 | 0.457 | 0.402 | 0.442 | 0.251 |
| | P¹³LG | k20_h512 | 148 | `0.424` | **0.395** | `0.426` | `0.516` | 0.425 | `0.480` | 0.297 |
*Figure from [^tan2023]*

[^hu2022]: Hu et al. (2022) "Exploring evolution-aware &amp; -free protein language models as protein function predictors." https://doi.org/10.48550/arXiv.2206.06583
[^tan2023]: Tan et al. (2023) "Multi-level Protein Representation Learning for Blind Mutational Effect Prediction." https://doi.org/10.48550/arXiv.2306.04899
[^notin2023]: Notin et al. (2023) "ProteinGym: Large-Scale Benchmarks for Protein Design and Fitness Prediction." https://doi.org/10.1101/2023.12.07.570727
