---
title: Epistasis is rare during evolution
tags:
  - epistasis
created: 2026-03-16T11:36:47
modified: "2026-04-21T05:01:15"
---
#### Summary
 **[[Epistasis]], in which protein fitness changes in a non-additive way, is rare in natural evolution and laboratory evolution.** Simple statistical models with only additive effects can explain most (80-95%) of changes in activity between variants [@ding2024; @faure2024; @beltran2024; @alcantar2025]. This has been suggested by multiple studies, which found that the effect of mutations that improve [[Stability and thermostability]] was basically entirely additive (see figure below). [@peleg2021; @escobedo2024; @alcantar2025] Park et al. were able to model 92-96% of variance in genome fitness by accounting exclusively for single-point and pairwise interactions plus a sigmoid nonlinearity; e.g., less than <5% of genomes in their test set showed third-order interactions. [@park2023] That said, there are examples where linear models are unable to accurately model fitness ([@faure2024; @ding2024; @tonner2022] with [[Spike protein]]/[[ACE2]]), so the type of statistical model still matters. 

#### Details
Sarkisyan et al. found that some mutations killed fluorescence in some GFP backbones but not others, and that pre-existing evolutionary propensity (e.g., from a PSSM) could not predict this. [@sarkisyan2016] They conclude that this is the result of destabilization. this made an additive model of fluorescence inappropriate; from that perspective epistasis occurred in 30% of multi-substitution variants. They conclude that this is largely due to threshold robustness, and that these mutations are destabilizing. See [[Mutation memory half life]]. Anecdotally [@tonner2022] came to a similar conclusion.

Beltran et al. measured >500k pathogenic variants in human diseases across 500 domains and found that additive models were sufficient to model almost all fitness changes. [@beltran2024]

Escobedo et al. found that the effects of substitutions in the hydrophobic core of proteins could be explained by linear models. [@escobedo2024]

Alcantar et al. carried out a "combinatorially complete" analysis of mutations introduced during [[Affinity maturation|affinity maturation]] of *de novo* designed minibinders and found that the binding improvements were basically entirely additive, which is similar to [[Antibodies|antibodies]] ([[Mutations obtained by antibodies during affinity maturation show epistasis in biophysical properties but not binding]]). [@alcantar2025]

#### Figures
![[Pasted-image-20231015161415.png]]
*Ref [@peleg2021]*

![[Epistasis_frequency.png]]
*Ref [@sarkisyan2016]*

![[Pasted-image-20240223071500.png]]
*Figure 2 from [@ding2024]*

#### See also
* [[Stability-activity trade-off during enzyme design and evolution is highly local and not global]]
* [[Mutations obtained by antibodies during affinity maturation show epistasis in biophysical properties but not binding]]
