---
tags:
  - protein-folding/misc
---
#### Summary
**[[AlphaFold|AlphaFold3]]-generation [[Protein-ligand co-folding|protein-ligand co-folding]] prediction methods can be substantially reduced in size without adversely affecting prediction quality** (Gong et al 2025[^gong2025]). This was found using Protenix. The model was shrunk by reducing the number of blocks and changing how models are sampled, as it was noticed that most blocks do not affect prediction accuracy in any substantial way. The exception is prediction of [[Protein-protein interactions|protein-protein interactions]], which do not work well without [[Multiple sequence alignments|MSAs]].

#### Figures
![](/assets/Pasted-image-20250722105406.png)
*Figure from Gong et al 2025[^gong2025]*

[^gong2025]: Gong et al. (2025) "Protenix-Mini: Efficient Structure Predictor via Compact Architecture, Few-Step Diffusion and Switchable pLM." https://doi.org/10.48550/ARXIV.2507.11839
