---
tags: [protein-design/misc]
created: "2024-04-30T03:21:35"
modified: "2026-04-05T23:14:54"
---

---
summary: Inverse folding substitution matrices closely align with BLOSUM matrix, except proline
tags: inverse-folding/execution
---
#### Summary
**Substitution matrices from [[Inverse folding]] closely match the (BLOSUM62) matrix, except proline** (Hsu et al 2022[^hsu2022], Castorina et al 2023[^castorina2023], Zhou et al 2024[^zhou2024]). Akpinaroglu et al 2023[^akpinaroglu2023] found that predicted proline residue embeddings distinguish from others earlier in the network than other residues.

#### Figures
![](/assets/BLOSUM_v_inverse_folding.png)
*Figure from Hsu et al 2022[^hsu2022]*

![](/assets/Predicted.png)
*Figure 1B from Castorina et al 2023[^castorina2023]*

![](/assets/Pasted-image-20240105112648.png)
*Figure 1H from Akpinaroglu et al 2023[^akpinaroglu2023]*

[^hsu2022]: Hsu et al. (2022) "Learning inverse folding from millions of predicted structures." https://doi.org/10.1101/2022.04.10.487779
[^castorina2023]: Castorina et al. (2023) "PDBench: evaluating computational methods for protein-sequence design." *Bioinformatics*. https://doi.org/10.1093/bioinformatics/btad027
[^zhou2024]: Zhou et al. (2024) "Protein Engineering with Lightweight Graph Denoising Neural Networks." *Journal of Chemical Information and Modeling*. https://doi.org/10.1021/acs.jcim.4c00036
[^akpinaroglu2023]: Akpinaroglu et al. (2023) "Structure-conditioned masked language models for protein sequence design generalize beyond the native sequence space." https://doi.org/10.1101/2023.12.15.571823
