---
title: Mutation memory half life
tags:
  - epistasis
created: 2024-05-02T05:15:27
modified: "2026-04-20T08:32:20"
---
#### Summary
 **Mutation memory half-life refers to the number of mutations required to observe changes in a mutation's effect on fitness.** The term mutation memory half-life was coined by Park et al [^park2022].

#### Details
Mutations that have a fitness effect in a sequence may not have the same effect if a sufficient number of additional mutations are allowed to accumulate in the background [^hie2022]. Put another way, mutations with an effect on an ancestral sequence would, after some evolution, fail to have the same effect. The mutation-memory half-life captures the amount of background evolution that needs to happen before this has a 50% chance of happening. 

In the context of their model system, about a quarter of mutations had memory half-lives of <50% sequence divergence. Over half have near-infinite memories, meaning that they retain their effects regardless of global sequence changes, and the extant sequence can successfully recapitulate the effects of those changes in ancestral sequences.

This correlates poorly with the following:
* Solvent accessibility
* Substitution rate
* Substitution rate of adjacent residues
* Distance to active site residues or interfaces

An earlier study in $beta$-lactamase found that not all mutational paths to an certain sequence are equally accessible; e.g., some of the mutations close off paths if accessed prematurely [^weinreich2006].

#### Figures
![[darwinian_evolution.png]]
*Ref [^weinreich2006]*

#### See also
* [[Ancestral sequence reconstruction]]
* [[Epistasis]]
* [[Not all sequences with improved activity have plausible evolutionary paths via stepwise introduction of mutations]]

[^park2022]: Park et al. (2022) "Epistatic drift causes gradual decay of predictability in protein evolution." *Science*. https://doi.org/10.1126/science.abn6895
[^hie2022]: Hie et al. (2022) "Evolutionary velocity with protein language models predicts evolutionary dynamics of diverse proteins." *Cell Systems*. https://doi.org/10.1016/j.cels.2022.01.003
[^weinreich2006]: Weinreich et al. (2006) "Darwinian Evolution Can Follow Only Very Few Mutational Paths to Fitter Proteins." *Science*. https://doi.org/10.1126/science.1123539
