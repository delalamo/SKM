---
tags:
  - structure-prediction/misc
  - alphafold2
created: "2024-10-25T03:26:40"
modified: "2026-04-10T14:02:57"
---

#### Summary

**Changing [[AlphaFold|AlphaFold2]]'s starting position for the protein structure from the "black hole" initialization dramatically improves the [[Structure prediction]] accuracy** [^bennett2023][^frank2024]. Monomer prediction was improved by starting from an initial guess (like a [[Rosetta]] model), and [^praetorius2023] used this to design dynamic proteins in multiple conformations. [^schweke2023] modeled homo-oligomers starting from the structure of a monomer.

#### Figures

\![[Pasted-image-20241025092618.png]]

*Figure from [^frank2024]; AA_IG refers to AlphaFold2 with initial guess; ESM refers to [[ESMFold]]*

[^bennett2023]: Bennett et al. (2023) "Improving de novo protein binder design with deep learning." *Nature Communications*. https://doi.org/10.1038/s41467-023-38328-5
[^frank2024]: Frank et al. (2024) "Scalable protein design using optimization in a relaxed sequence space." *Science*. https://doi.org/10.1126/science.adq1741
[^praetorius2023]: Praetorius et al. (2023) "Design of stimulus-responsive two-state hinge proteins." *Science*. https://doi.org/10.1126/science.adg7731
[^schweke2023]: Schweke et al. (2023) "An atlas of protein homo-oligomerization across domains of life." https://doi.org/10.1101/2023.06.09.544317
