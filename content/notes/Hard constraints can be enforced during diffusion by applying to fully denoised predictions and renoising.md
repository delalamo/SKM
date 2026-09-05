---
tags:
  - inference/guidance
  - design/backbones
---
#### Summary
Hard constraints applied with [[notes/diffusion-guidance|guidance]] can be better enforced during [[notes/diffusion-models|diffusion]] by applying them to the fully denoised predictions and renoising them[@christopher2025]. In [[notes/protein-backbone-design|protein backbone design]], this outperformed other guidance strategies reliant on intermediate predictions.