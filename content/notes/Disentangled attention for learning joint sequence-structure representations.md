#### Summary

** [@li2024prosst] use a specialized form of [[Disentangled attention]] when training the [[Hybrid sequence-structure models|hybrid sequence/structure model]] DeProt.** The main difference is that they include structure in addition to info about sequence-derived representations and position. As with the NLP-derived disentangled attention which ignores position-position attention matrices, they also ignore structure-position, position-structure, structure-structure, and position-position.

#### Details
Structure-based embeddings were derived using [[Geometric Vector Perceptrons|GVP]] and quantized into one of several thousand categories. The number strongly affected performance of zero-shot [[tags/thermostability|stability]] prediction.

#### Figures
![[Pasted-image-20240517171742.png]]

*Figure 1 from [@li2024prosst]*
