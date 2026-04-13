#### Summary

**[^li2024] use a specialized form of [[Disentangled attention]] when training the [[Hybrid sequence-structure models|hybrid sequence/structure model]] DeProt.** The main difference is that they include structure in addition to info about sequence-derived representations and position. As with the NLP-derived disentangled attention which ignores position-position attention matrices, they also ignore structure-position, position-structure, structure-structure, and position-position.

#### Details
Structure-based embeddings were derived using [[Geometric Vector Perceptrons|GVP]] and quantized into one of several thousand categories. The number strongly affected performance of zero-shot [[Stability and thermostability|stability]] prediction.

#### Figures
![[Pasted-image-20240517171742.png]]

*Figure 1 from [^li2024]*

[^li2024]: Li et al. (2024) "ProSST: Protein Language Modeling with Quantized Structure and Disentangled Attention." https://doi.org/10.1101/2024.04.15.589672
