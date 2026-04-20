---
tags:
  - inverse-folding/evaluation
  - thermostability/design
created: "2025-02-17T06:26:27"
modified: "2026-04-20T08:32:20"
---
#### Summary
 **[[Inverse folding]] can generate more [[Stability and thermostability|stable]] sequences when jointly run with a [[Structure prediction|protein folding]] model** [^cho2024]. This was achieved using trRosetta and backpropagated trRosetta. The authors formulate this design approach by jointly considering the inverse folding model $p(sequence|structure)$ and the forward-folding model $p(structure|sequence)$, as the former does not guarantee that the sequence preferentially folds into other states.

#### Figures
![[Pasted-image-20241231142119.png]]
*Ref [^cho2024]*

[^cho2024]: Cho et al. (2024) "Implicit modeling of the conformational landscape and sequence allows scoring and generation of stable proteins." https://doi.org/10.1101/2024.12.20.629706
