---
tags:
  - transformers
created: 2026-04-05T17:19:25
modified: "2026-04-21T05:01:15"
---
#### Summary
**On fixed compute budgets, sparse models (e.g., [[Mixture-of-experts|mixture-of-experts]] models) outperform dense models** [@bhatnagar2025].

#### Figures
| Architecture | Parameters | Active Parameters | FLOPs | Validation Loss |
|---|---|---|---|---|
| Dense | 1,386,084,352 | 1,386,084,352 | 1.10 × 10^20 | 1.920 |
| Sparse | 1,355,871,232 | 393,174,016 | 3.14 × 10^19 | 1.948 |
| Sparse | 2,989,920,000 | 866,369,280 | 6.93 × 10^19 | 1.849 |
*Table from [@bhatnagar2025]*
