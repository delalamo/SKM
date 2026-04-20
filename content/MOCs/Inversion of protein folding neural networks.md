---
title: Inversion of protein folding neural networks
tags:
created: 2026-04-10T14:02:57
modified: "2026-04-20T08:16:13"
---

**Inversion of protein folding neural networks**, such as [[AlphaFold2]], [[RosettaFold]], [[ESMFold]], and trRosetta, has been used for protein design by hallucination as well as adversarial attacks. It involves inversion of the networks and backpropagation to input sequence using a custom loss.

#### Mentions

* **Designing proteins by hallucination can be improved by Markov chain Monte Carlo sampling at the end** ([[10.1002__pro.4653|Goverde et al 2023]]). This is in contrast to just gradient descent.
![[Pasted-image-20231206155349.png]]
	*Figure 2A from [^goverde2023]*

#### Examples

* **[[10.1021__acssynbio.3c00674|Hansen et al 2024]] designed a [[Stability and thermostability|thermostable]] glycoside hydrolase using [[Inversion of protein folding neural networks|hallucination]].** Although the proteins folded, they were inactive due to misplacement of the active site side chains.
![[Pasted-Graphic-2-copy.png]]
	*Ref [^hansen2024]*

<!-- generated -->

[^goverde2023]: Goverde et al. (2023) "De novo protein design by inversion of the AlphaFold structure prediction network." *Protein Science*. https://doi.org/10.1002/pro.4653

[^hansen2024]: Hansen et al. (2024) "Carving out a Glycoside Hydrolase Active Site for Incorporation into a New Protein Scaffold Using Deep Network Hallucination." *ACS Synthetic Biology*. https://doi.org/10.1021/acssynbio.3c00674
