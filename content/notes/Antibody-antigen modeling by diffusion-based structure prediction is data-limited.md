---
tags:
  - prediction/complexes
  - evidence/datasets
created: 2026-04-05T17:25:38
modified: "2026-07-17T10:38:09"
publicationHistory:
  "2026-03-16": "https://biomlzk.ghost.io/antibody-antigen-complex-prediction-by-af3-generation-methods-is-data-limited/"
---

#### Summary

**[[Antibody-antigen interactions|Antibody-antigen]] [[notes/Structure prediction|complex prediction]] by [[notes/Diffusion models|diffusion]]-based [[notes/Structure prediction|structure prediction]] methods is data-limited** [@zhang2026]. This is not true of other poor-performing tasks, such as small molecule docking. This was observed using a version of Protenix trained on four additional years of public data.

#### Figures

| Model | Ab-Ag DQ SR(%) | Ab-Ag lDDT |
|---|---|---|
| Chai-1 | 21.12 | 0.1972 |
| Boltz-1 | 12.02 | 0.1577 |
| Boltz-2 | 19.20 | 0.1606 |
| Protenix-v0.5.0 | 15.58 | 0.1713 |
| Protenix-v1 | 24.11 | 0.2488 |
| Protenix-v1-20250630 | **39.49** | **0.3574** |

*Ref [@zhang2026]*
