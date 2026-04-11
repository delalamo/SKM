---
title: Backbone diffusion works best on small protein sizes
tags:
  - diffusion-models/protein-design
  - protein-design/design
created: "2024-05-08T17:59:48"
modified: "2026-04-11T06:15:31"
---
#### Summary
 **Protein [[Protein backbone design#Diffusion|structure diffusion]] works best on small protein sizes.** [^watson2023] tried to refold proteins generated using RF-diffusion and [[ProteinMPNN]] and using [[AlphaFold|AlphaFold2]] (single sequence) and found that they generally disagreed if they were too big. Likewise, [^ingraham2023] could not reliably refold proteins *in silico* if they were greater than ~200-300 residues.

#### Figures
\![[Pasted-image-20231203094326.png]]
*Figures 2B and 2C from [^watson2023]*

\![[Pasted-image-20240204121659.png]]
*Figure S14 from [^ingraham2023]*

[^watson2023]: Watson et al. (2023) "De novo design of protein structure and function with RFdiffusion." *Nature*. https://doi.org/10.1038/s41586-023-06415-8
[^ingraham2023]: Ingraham et al. (2023) "Illuminating protein space with a programmable generative model." *Nature*. https://doi.org/10.1038/s41586-023-06728-8
