---
tags: [protein-design/misc]
created: "2024-05-02T04:41:27"
modified: "2026-04-10T14:02:57"
---

---
summary: Subquadratic scaling for protein backbone diffusion
tags:
 - protein-backbone-design/diffusion
---
#### Summary
**The [[Protein backbone design]] method (Chroma) uses sub-quadratic scaling for calculating attention** [^ingraham2023]. In practice, this leads to attention between a residue and its 20 nearest neighbors plus 40 randomly selected residues obtained using an inverse cubic formula ($O(n)$ scaling). This led to favorable results compared to *k*-nearest neighbor.

#### Figures
\![[Pasted-image-20240204113315.png]]
*Figure S4 from [^ingraham2023]*

\![[Pasted-image-20240204121153.png]]
*Figure S22 from [^ingraham2023]*

[^ingraham2023]: Ingraham et al. (2023) "Illuminating protein space with a programmable generative model." *Nature*. https://doi.org/10.1038/s41586-023-06728-8
