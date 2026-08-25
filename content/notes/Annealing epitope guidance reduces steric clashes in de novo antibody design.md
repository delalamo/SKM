---
tags:
  - diffusion-models/protein-design
  - diffusion-guidance/protein-design
  - antibody-antigen-interactions/complex-prediction
created: "2026-08-25"
modified: "2026-08-25T10:55:31"
---
#### Summary
**In epitope-guided [[De novo antibody design|de novo antibody design]], applying strong [[diffusion-guidance|guidance]] early and annealing it to zero can preserve epitope recall while reducing steric clashes** [@kim2026tideab].

#### Details
Static classifier-free guidance in TiDE-Ab gave heavy-chain epitope recall of 0.934 and 43.35 clashes per design. Combining cosine annealing with truncation at $t = 0.5$ preserved recall at 0.935, increased epitope precision from 0.777 to 0.889, and reduced clashes to 8.14. These results are in silico and await experimental validation.

#### Figures

| Guidance configuration | HC-Prec (↑) | HC-Rec (↑) | F. Dev (↓) | Binding mode (↑) | Clashes (↓) |
| --- | ---: | ---: | ---: | ---: | ---: |
| Static CFG | 0.777 ± 0.044 | 0.934 ± 0.041 | 0.2238 ± 0.0742 | 4.25 ± 1.24 | 43.35 ± 35.17 |
| CFG w/Early Truncation | 0.874 ± 0.042 | 0.937 ± 0.041 | 0.2103 ± 0.0681 | 4.27 ± 1.30 | 10.62 ± 14.59 |
| CFG w/Cosine Annealing | 0.876 ± 0.043 | **0.939 ± 0.042** | 0.2100 ± 0.0674 | 4.15 ± 1.17 | 9.76 ± 13.84 |
| TiDE-Ab (Final) | **0.889 ± 0.042** | 0.935 ± 0.041 | **0.2083 ± 0.0677** | **4.42 ± 1.17** | **8.14 ± 11.93** |

*Ref [@kim2026tideab]; TiDE-Ab uses both cosine annealing and early truncation*

#### See also
- [[Stronger diffusion guidance reduces diversity of generated outputs]]
