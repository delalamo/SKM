---
tags:
  - alphafold2
  - structure-prediction/sampling
created: "2024-10-25T03:26:40"
modified: "2026-04-21T07:28:09"
---

#### Summary

**Changing [[alphafold2|AlphaFold2]]'s starting position for the protein structure from the "black hole" initialization dramatically improves the [[structure-prediction|Structure prediction]] accuracy** [@bennett2023; @frank2024]. Monomer prediction was improved by starting from an initial guess (like a [[Rosetta]] model), and [@praetorius2023] used this to design dynamic proteins in multiple conformations. [@schweke2023] modeled homo-oligomers starting from the structure of a monomer.

#### Figures

![[Pasted-image-20241025092618.png]]

*Ref [@frank2024]; AA_IG refers to AlphaFold2 with initial guess; ESM refers to [[ESMFold]]*
