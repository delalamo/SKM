---
tags:
  - inverse-folding/evaluation
  - thermostability/design
created: "2025-02-17T06:26:27"
modified: "2026-04-21T07:03:26"
---
#### Summary
 **[[tags/inverse-folding|Inverse folding]] can generate more [[tags/thermostability|stable]] sequences when jointly run with a [[tags/structure-prediction|protein folding]] model** [@cho2024]. This was achieved using trRosetta and backpropagated trRosetta. The authors formulate this design approach by jointly considering the inverse folding model $p(sequence|structure)$ and the forward-folding model $p(structure|sequence)$, as the former does not guarantee that the sequence preferentially folds into other states.

#### Figures
![[Pasted-image-20241231142119.png]]
*Ref [@cho2024]*
