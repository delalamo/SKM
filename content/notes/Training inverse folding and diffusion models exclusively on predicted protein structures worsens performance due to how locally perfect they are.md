---
tags:
  - inverse-folding/training
---
#### Summary
**Training machine learning models for either [[Inverse folding|inverse folding]] or [[Protein backbone design|protein backbone design]] via [[Diffusion models|diffusion]] exclusively on predicted models worsens performance** (Hsu et al 2022[^hsu2022], Su et al 2023[^su2023]). This was observed when training [[ESM-IF]] and [[Geometric Vector Perceptrons|GVP]] as well as when training using the [[Evoformer]] or the [[Hybrid sequence-structure models|hybrid sequence-structure method]] MIF-ST, but not [[SaProt]] (which uses tokens from the [[Foldseek]] alphabet). This was shown to be because predicted models are "too perfect" at a local level (Tan et al 2025[^tan2025]).

#### Details
Huguet et al 2024[^huguet2024] found that training their diffusion model on both predicted models and experimental structures worsened designability and novelty relative to a model trained on experimental structures only.

Lin et al 2023a[^lin2023] trained a version of the [[Protein backbone design|backbone]] [[Diffusion models|diffusion model]] GENIE on [[AlphaFold|AlphaFold2]] models from SwissProt and found that although designability increased was greater than a model trained on the PDB, diversity was lower.

#### See also
- [[Inverse folding models trained on all proteins outperform those trained on Abs for CDR prediction]]
- [[Adding noise while training non-Ab inverse folding models improves self-consistency while worsening sequence recovery]]
- [[Focused protein sequence libraries are poor training sets]]

[^hsu2022]: Hsu et al. (2022) "Learning inverse folding from millions of predicted structures." https://doi.org/10.1101/2022.04.10.487779
[^su2023]: Su et al. (2023) "SaProt: Protein Language Modeling with Structure-aware Vocabulary." https://doi.org/10.1101/2023.10.01.560349
[^tan2025]: Tan et al. (2025) "AlphaFold Database Debiasing for Robust Inverse Folding." https://doi.org/10.48550/arxiv.2506.08365
[^huguet2024]: Huguet et al. (2024) "Sequence-Augmented SE(3)-Flow Matching For Conditional Protein Backbone Generation." https://doi.org/10.48550/ARXIV.2405.20313
[^lin2023]: Lin & AlQuraishi (2023) "Generating Novel, Designable, and Diverse Protein Structures by Equivariantly Diffusing Oriented Residue Clouds." https://doi.org/10.48550/arXiv.2301.12485