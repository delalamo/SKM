---
tags:
  - protein-language-models/antibodies
created: "2024-08-22T05:38:08"
modified: "2026-04-20T08:16:13"
---
#### Summary
**[[Developability]] properties of [[Antibodies|antibodies]], such as [[Stability and thermostability|thermostability]], can be predicted with higher accuracy using features derived from [[MD simulations]] compared to those obtained from either static structures or [[Protein language models|language model embeddings]]** [^rollins2024]. [^bashour2024] found that developability predictions made from trajectories starting from either experimental structures or [[Antibody structure prediction|predicted structures]] tended to correlate with each other better than predictions made from just the experimental structures or predicted structures.

#### Figures
![[Structure-DP-correlations-before-and-after-MD.png]]
*Ref [^bashour2024]*

#### See also
- [[Antibody developability predictions from computational models are sensitive to the structure prediction method]]
- [[Abs modeled using MD are better for featurization than those modeled using homology modeling]]

[^rollins2024]: Rollins et al. (2024) "AbMelt: Learning antibody thermostability from molecular dynamics." *Biophysical Journal*. https://doi.org/10.1016/j.bpj.2024.06.003
[^bashour2024]: Bashour et al. (2024) "Biophysical cartography of the native and human-engineered antibody landscapes quantifies the plasticity of antibody developability." *Communications Biology*. https://doi.org/10.1038/s42003-024-06561-3
