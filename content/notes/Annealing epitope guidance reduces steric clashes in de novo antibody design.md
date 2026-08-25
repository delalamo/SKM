---
tags:
  - diffusion-models/protein-design
  - diffusion-guidance/protein-design
  - antibody-antigen-interactions/complex-prediction
created: "2026-08-25"
modified: "2026-08-25T10:16:02"
---
#### Summary
**In epitope-guided [[De novo antibody design|de novo antibody design]], applying strong guidance early and annealing it to zero can preserve epitope recall while reducing steric clashes** [@kim2026tideab]. 

#### Details
Static classifier-free guidance in TiDE-Ab gave heavy-chain epitope recall of 0.934 and 43.35 clashes per design. Combining cosine annealing with truncation at $t = 0.5$ preserved recall at 0.935, increased epitope precision from 0.777 to 0.889, and reduced clashes to 8.14. These results are in silico and await experimental validation.

#### See also
- [[Stronger diffusion guidance reduces diversity of generated outputs]]
