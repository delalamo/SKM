---
tags:
  - design/antibodies
  - training/fine-tuning
  - design/inverse-folding
created: 2024-05-01T07:08:10
modified: "2026-10-09T06:14:45"
---
#### Summary
**For [[notes/Inverse folding|inverse folding]] of antibody-antigen interfaces, pretraining on all monomeric protein structures prior to fine-tuning on antibody structures improves sequence recovery from 34.5% to 47.7%** [@mahajan2023]. General-protein pretraining particularly improved [[Complementarity-determining regions#CDRH3|CDRH3]] recovery, while antibody-specific fine-tuning gave the best overall performance. Pretraining on general [[notes/Protein-protein interactions|protein-protein interaction]] structures before antibody-specific fine-tuning did not improve sequence recovery over antibody-only training.

#### See also
- [[Structure prediction and design tools trained on monomers generalize to oligomers]]
