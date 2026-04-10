---
tags:
  - protein-design/misc
created: "2026-04-05T17:36:43"
modified: "2026-04-10T14:30:55"
---

#### Summary

Inverse folding methods outperform hallucination at designing proteins that can be refolded in silico ([10.48550__arXiv.2312.00080|Wang et al 2023], [10.1126__science.adq1741|Frank et al 2024]).

#### Figures

| | ESMFold TM | ESMFold pLDDT | OmegaFold TM | OmegaFold pLDDT | AlphaFold2 TM | AlphaFold2 pLDDT | Recovery% |
|---|---|---|---|---|---|---|---|
| **Uniform** | 0.05 | 27.68 | 0.05 | 31.53 | 0.06 | 33.68 | 5.00 |
| **Natural frequencies** | 0.07 | 30.53 | 0.07 | 35.59 | 0.06 | 35.02 | 5.84 |
| **StructTrans** | 0.72 | 68.85 | 0.64 | 70.35 | 0.79 | 80.66 | 35.89 |
| **GVP** | 0.73 | 69.67 | 0.67 | 74.33 | 0.83 | 84.29 | 39.46 |
| **ProteinMPNN** | **0.80** | **76.53** | **0.76** | **80.75** | **0.87** | **87.89** | 41.44 |
| **PiFold** | 0.71 | 67.55 | 0.64 | 70.21 | 0.82 | 82.54 | 44.86 |
| **ByProt** | 0.73 | 72.12 | 0.70 | 77.58 | 0.85 | 87.26 | **51.23** |
| **AF-Design** | 0.53 | 61.37 | 0.53 | 72.04 | 0.52 | 75.29 | 15.95 |
| **ESM-Design** | 0.38 | 59.65 | 0.38 | 62.66 | 0.37 | 60.02 | 17.33 |
| **Wildtype** | 0.80 | 74.91 | 0.75 | 78.39 | 0.90 | 89.87 | 100 |
*Table from [10.48550__arXiv.2312.00080|Wang et al 2023]*

\![[Pasted-image-20241025093149.png]]
*Figure from [10.1126__science.adq1741|Frank et al 2024]*
