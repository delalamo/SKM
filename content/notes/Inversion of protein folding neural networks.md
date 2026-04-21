---
title: Inversion of protein folding neural networks
created: 2026-04-10T14:02:57
modified: "2026-04-20T08:32:20"
---

**Inversion of protein folding neural networks**, such as [[AlphaFold2]], [[RosettaFold]], [[ESMFold]], and trRosetta, has been used for protein design by hallucination as well as adversarial attacks. It involves inversion of the networks and backpropagation to input sequence using a custom loss.

#### Mentions

* **Designing proteins by hallucination can be improved by Markov chain Monte Carlo sampling at the end** [@goverde2023]. This is in contrast to just gradient descent.
![[Pasted-image-20231206155349.png]]
	*Figure 2A from [@goverde2023]*

#### Examples

* **Hansen et al. [@hansen2024] designed a [[Stability and thermostability|thermostable]] glycoside hydrolase using [[Inversion of protein folding neural networks|hallucination]].** Although the proteins folded, they were inactive due to misplacement of the active site side chains.
![[Pasted-Graphic-2-copy.png]]
	*Ref [@hansen2024]*
