---
title: Markov State Models
created: 2026-04-10T14:02:57
modified: "2026-04-21T05:01:15"
---

**Markov state models** (MSMs) are a framework for assigning frames of an [[MD simulations|MD simulation]] to a small number of specific states.

#### Details
[@glielmo2021] describe the process of building an MSM as follows: (1) featurize data (e.g., dihedral angles, contact maps) such that roto-translational invariance is maintained; (2) preprocess the data by transforming using methods such as [[Time-lagged independent component analysis|time-lagged independent component analysis]] with a chosen lag time; (3) [[Clustering|cluster]] the data to obtain discrete, disjoint states; (4) estimate a transition matrix using the prespecified lag time; (5) assess correctness using the [[Chapman-Kolmogorov test]].

#### Figures
![[Pasted-Graphic-15.png]]
*Ref [@husic2018]*
