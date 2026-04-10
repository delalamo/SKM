---
title: Sequence-based DL models learn intra-family phylogenetics of protein evolution
tags:
  - protein-folding/misc
created: "2024-07-02T05:24:12"
modified: "2026-04-10T14:30:55"
---
#### Summary
 **DL models for protein sequences (including [[Protein language models|PLMs]]) learn the phylogenetics of protein evolution.** [^detlefsen2022] showed this in the 2D latent space of protein family-specific [[Variational autoencoders]] (below); whereas [^hie2022] showed how repurposing [[Sequence perplexity|perplexity]] as velocities within a manifold of sequence embedding space from [[ESM]]-1b recapitulated evolutionary trajectories of viral and eukaryotic proteins

#### Figures
\![[TSNE-phylogeny-overlap.png]]
\![[TSNE-phylogeny-overlap-2.png]]
*Figures from [^detlefsen2022]*

\![[Pasted-image-20240430135746.png]]
*Figure from [^hie2022]*

#### See also
* [[PLMs are biased by uneven distribution of sequence data in datasets such as UniRef and UniProt]]
* [[The latent space of VAEs can encode the conformational landscape of dynamic proteins]]

[^detlefsen2022]: Detlefsen et al. (2022) "Learning meaningful representations of protein sequences." *Nature Communications*. https://doi.org/10.1038/s41467-022-29443-w
[^hie2022]: Hie et al. (2022) "Evolutionary velocity with protein language models predicts evolutionary dynamics of diverse proteins." *Cell Systems*. https://doi.org/10.1016/j.cels.2022.01.003
