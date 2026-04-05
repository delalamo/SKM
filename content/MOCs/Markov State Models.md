---
title: Markov State Models
tags:
  - markov-state-models
---

**Markov state models** (MSMs) are a framework for assigning frames of an [[MD simulations|MD simulation]] to a small number of specific states.

#### Details
[[10.1021__acs.chemrev.0c01195|Glielmo et al 2021]] describe the process of building an MSM as follows: (1) featurize data (e.g., dihedral angles, contact maps) such that roto-translational invariance is maintained; (2) preprocess the data by transforming using methods such as [[Time-lagged independent component analysis|time-lagged independent component analysis]] with a chosen lag time; (3) [[Clustering|cluster]] the data to obtain discrete, disjoint states; (4) estimate a transition matrix using the prespecified lag time; (5) assess correctness using the [[Chapman-Kolmogorov test]].

#### Figures
![](/assets/Pasted-Graphic-15.png)
*Figure from [[10.1021__jacs.7b12191|Husic & Pande 2018]]*

<!-- generated -->
