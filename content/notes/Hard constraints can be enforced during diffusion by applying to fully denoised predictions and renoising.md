---
tags:
  - inference/guidance
  - design/backbones
---
#### Summary
Hard constraints applied with [[notes/Diffusion guidance|guidance]] can be better enforced during [[notes/Diffusion models|diffusion]] by applying them to the fully denoised predictions and renoising them[@christopher2025]. In [[notes/Protein backbone design|protein backbone design]], this outperformed other guidance strategies reliant on intermediate predictions.