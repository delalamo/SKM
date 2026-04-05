---
title: Inversion of protein folding neural networks
tags:
  - inversion-of-protein-folding-neural-networks
---

**Inversion of protein folding neural networks**, such as [[AlphaFold|AlphaFold2]], [[RosettaFold]], [[ESMFold]], and trRosetta, has been used for protein design by hallucination as well as adversarial attacks. It involves inversion of the networks and backpropagation to input sequence using a custom loss.

#### Mentions

* **Designing proteins by hallucination can be improved by Markov chain Monte Carlo sampling at the end** ([[10.1002__pro.4653|Goverde et al 2023]]). This is in contrast to just gradient descent.
	![](/assets/Pasted-image-20231206155349.png)
	*Figure 2A from [[10.1002__pro.4653|Goverde et al 2023]]*

#### Examples

* **[[10.1021__acssynbio.3c00674|Hansen et al 2024]] designed a [[Stability and thermostability|thermostable]] glycoside hydrolase using [[Inversion of protein folding neural networks|hallucination]].** Although the proteins folded, they were inactive due to misplacement of the active site side chains.
	![](/assets/Pasted-Graphic-2-copy.png)
	*Figure from [[10.1021__acssynbio.3c00674|Hansen et al 2024]]*

<!-- generated -->
