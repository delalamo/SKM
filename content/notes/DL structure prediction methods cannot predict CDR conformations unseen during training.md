---
tags:
  - cdrh3
  - structure-prediction/limitations
  - antibodies/engineering-and-design
created: 2024-04-25T00:43:05
modified: "2026-04-21T07:28:09"
---

#### Summary
The structures of [[antibodies|antibody]] [[Complementarity-determining regions|CDRH3]] conformations absent from training sets cannot be accurately [[structure-prediction|predicted]] by deep learning methods [@greenshieldswatson2023]. An inability to extrapolate to new CDRH3 conformations may be why fine-tuned versions of RF-diffusion for antibody design supplement their training datasets with those of other loop-mediated [[protein-protein-interactions|PPIs]] [@peng2023generative; @bennett2024], although no ablations have been done to my knowledge.

#### See also
- [[Focused protein sequence libraries are poor training sets]]
- [[Deep learning methods cannot generalize T-cell receptor binding to new epitopes]]
