---
title: Sequence-based DL models learn intra-family phylogenetics of protein evolution
tags:
  - protein-folding/misc
---
#### Summary
 **DL models for protein sequences (including [[Protein language models|PLMs]]) learn the phylogenetics of protein evolution.** Detlefsen et al 2022[^detlefsen2022] showed this in the 2D latent space of protein family-specific [[Variational autoencoders]] (below); whereas Hie et al 2022[^hie2022] showed how repurposing [[Sequence perplexity|perplexity]] as velocities within a manifold of sequence embedding space from [[ESM]]-1b recapitulated evolutionary trajectories of viral and eukaryotic proteins

#### Figures
![](/assets/TSNE-phylogeny-overlap.png)
![](/assets/TSNE-phylogeny-overlap-2.png)
*Figures from Detlefsen et al 2022[^detlefsen2022]*

![](/assets/Pasted-image-20240430135746.png)
*Figure from Hie et al 2022[^hie2022]*

#### See also
* [[PLMs are biased by uneven distribution of sequence data in datasets such as UniRef and UniProt]]
* [[The latent space of VAEs can encode the conformational landscape of dynamic proteins]]

[^detlefsen2022]: Detlefsen et al. (2022) "Learning meaningful representations of protein sequences." *Nature Communications*. https://doi.org/10.1038/s41467-022-29443-w
[^hie2022]: Hie et al. (2022) "Evolutionary velocity with protein language models predicts evolutionary dynamics of diverse proteins." *Cell Systems*. https://doi.org/10.1016/j.cels.2022.01.003
