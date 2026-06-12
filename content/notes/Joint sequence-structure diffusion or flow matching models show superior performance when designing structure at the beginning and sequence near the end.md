---
title: Joint sequence-structure diffusion or flow matching models show superior performance when designing structure at the beginning and sequence near the end
tags:
  - diffusion-models/protein-design
  - protein-design/design
  - inverse-folding/evaluation
created: "2026-06-12T09:32:33"
modified: "2026-06-12T10:33:23"
---

#### Summary
**Joint sequence/structure [[diffusion-models|diffusion models]] or [[Flow matching|flow matching models]] show best performance when structure design is done at the beginning and sequence design is left to the end [@didi2026a; @staerk2025; @rectorbrooks2026; @qiu2026].** DISCO specifically found that including entropy-adaptive temperature annealing throughout the diffusion process improved both the number of viable clusters and the designability fraction, particularly when the sequence sampling temperature was fixed at a specific value [@rectorbrooks2026]. 

#### Figures
![[DISCO-temperature-switch-ablation.png]]
*Ref [@rectorbrooks2026]*

#### See also
* [[Coupling sidechain and main chain prediction or design does not always lead to improvements]]

#### References
