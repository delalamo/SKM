---
tags:
  - cdrh3
  - structure-prediction/limitations
  - antibodies/engineering-and-design
created: 2024-04-25T00:43:05
modified: "2026-04-20T07:16:03"
---

#### Summary
The structures of [[Antibodies|antibody]] [[Complementarity-determining regions|CDRH3]] conformations absent from training sets cannot be accurately [[Structure prediction|predicted]] by deep learning methods[^greenshieldswatson2023]. An inability to extrapolate to new CDRH3 conformations may be why fine-tuned versions of RF-diffusion for antibody design supplement their training datasets with those of other loop-mediated [[Protein-protein interactions|PPIs]] [^peng2024][^bennett2024], although no ablations have been done to my knowledge.

#### See also
- [[Focused protein sequence libraries are poor training sets]]
- [[Deep learning methods cannot generalize T-cell receptor binding to new epitopes]]

[^greenshieldswatson2023]: Greenshields-Watson et al. (2024) "Investigating the ability of deep learning-based structure prediction to extrapolate and/or enrich the set of antibody CDR canonical forms." Frontiers in Immunology. https://doi.org/10.3389/fimmu.2024.1352703
[^peng2024]: Peng et al. (2023) "Generative Diffusion Models for Antibody Design, Docking, and Optimization." https://doi.org/10.1101/2023.09.25.559190
[^bennett2024]: Bennett et al. (2026) "Atomically accurate de novo design of antibodies with RFdiffusion." Nature. https://doi.org/10.1038/s41586-025-09721-5