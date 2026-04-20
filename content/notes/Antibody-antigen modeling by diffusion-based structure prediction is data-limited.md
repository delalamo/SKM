---
tags:
  - alphafold3
  - structure-prediction/complex-prediction
  - diffusion-models/structure-prediction
  - plddt
created: 2026-04-05T17:25:38
modified: "2026-04-20T08:16:13"
---

#### Summary

**[[Antibody-antigen interactions|Antibody-antigen]] [[Structure prediction|complex prediction]] by [[Diffusion models|diffusion]]-based [[Structure prediction|structure prediction]] methods is data-limited** [^zhang2026]. This is not true of other poor-performing tasks, such as small molecule docking. This was observed using a version of Protenix trained on four additional years of public data.

#### Figures

| Model | Ab-Ag DQ SR(%) | Ab-Ag lDDT |
|---|---|---|
| Chai-1 | 21.12 | 0.1972 |
| Boltz-1 | 12.02 | 0.1577 |
| Boltz-2 | 19.20 | 0.1606 |
| Protenix-v0.5.0 | 15.58 | 0.1713 |
| Protenix-v1 | 24.11 | 0.2488 |
| Protenix-v1-20250630 | **39.49** | **0.3574** |

*Ref [^zhang2026]*

#### Publication history

- 16 March 2026: https://biomlzk.ghost.io/antibody-antigen-complex-prediction-by-af3-generation-methods-is-data-limited/

[^zhang2026]: Unknown et al. (2026) "Protenix-v1: Toward High-Accuracy Open-Source Biomolecular Structure Prediction." https://doi.org/10.64898/2026.02.05.703733
