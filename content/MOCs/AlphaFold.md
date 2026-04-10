---
title: AlphaFold
tags:
  - alphafold
created: "2026-04-10T14:02:57"
modified: "2026-04-10T14:02:57"
---

*(OpenFold redirects here)*
**AlphaFold** is a series of protein [[Structure prediction|structure prediction]] methods. The most widely used and studied method is AlphaFold2, which was unveiled in late 2020, released in late 2021, and is the first to make extensive use of the [[Transformer]] architecture, consisting of 97 million parameters. [[AlphaMissense]] is a derivative of this method. AlphaFold3 was released in early May 2024.

\![[Pasted-image-20231029184254.png]]
*Architecture of AlphaFold2 from [[10.1038__s41586-021-03819-2|Jumper et al 2021]]*

\![[Pasted-Graphic-4.png]]
*Architecture of AlphaFold3 from [[10.1038__s41586-024-07487-w|Abramson et al 2024]]*

#### Architectural and ML contributions
###### AlphaFold2

* [[Evoformer]]
* [[Invariant point attention]]
* [[Frame aligned point error]]
* [[Distillation|Self-distillation]] for protein structures
* [[Predicted aligned error]]
* [[Triangular update]]

###### AlphaFold3

* PairFormer
* PDE: predicted distance error
* Non-equivariant per-atom prediction, which leads to occasional errors when predicting chirality
* [[Distillation|Cross-distillation]] from AlphaFold2-Multimer v2.3 to avoid hallucination of low-[[pLDDT]] regions

#### Conformational modeling

* **Most sets of predictions of [[Fold-switching proteins|fold-switching proteins]] from the five AlphaFold2 monomer-ptm models are the same conformation** ([[10.1002__pro.4353|Chakravarty and Porter 2022]]).
* **Alternative conformations of proteins can be sampled using constraints by fine-tuning the [[Invariant point attention|invariant point attention]] of AlphaFold2 on those constraints** ([[10.1101__2023.12.01.569498|Zhang et al 2023c]]). Additional constraints include intra-domain [[Frame aligned point error|frame aligned point error]], torsion angle losses, and structural violation losses.
* **AlphaFold2 can predict different conformations of a given sequence depending on if a single chain is predicted vs. multiple chains** ([[10.1101__2021.10.11.463937|Jendrusch et al 2021]]; [[10.1002__pro.4368|Cummins et al 2022]]).
* **AlphaFold3 can sometimes model alternate conformations without prompting** ([[10.1101__2025.05.22.655600|Xu et al 2025]]).

#### Extensions and other applications

*See [[Inversion of protein folding neural networks]]*
* **The pipeline FAAST iterates between a modified version of AlphaFold2 that has been changed to accept [[NMR]] restraints, and NOE peak assignment** ([[10.1101__2023.04.14.536890|Liu et al 2023b]]). Twenty models are made per iteration. The modifications were introduced to both the [[Evoformer]] and [[Invariant point attention]].

#### Training and backpropagation

* **[[AlphaFold|OpenFold]] training proceeds sequentially along XYZ principal components**([[10.1101__2022.11.20.517210|Ahdritz et al 2024]]).
* **AlphaFold3 was estimated to take 15 million CPU hours and 10 million GPU hours to setup the data and train from start to finish** (Jennifer Wei, PEGS Europs 2024).

<!-- generated -->

## Extensions

- [[Structure prediction with AlphaFold improved when starting from an initial guess, rather than default initialization]]
