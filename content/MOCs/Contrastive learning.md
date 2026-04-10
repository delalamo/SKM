---
title: Contrastive learning
tags:
  - contrastive-learning
created: "2026-04-10T14:30:55"
modified: "2026-04-10T14:30:55"
---

**Contrastive learning** is a supervised method for driving the latent representations of data points towards or away from each other by adding custom losses.

#### Implementations

* The **triplet margin loss** used by [[10.1126__science.adf2465|Yu et al 2023a]]:
		$$L^{TM}=||z_{a}-z_{p}||^{2} - ||z_{a}-z_{n}||^{2}+\alpha$$
		$z_{a}$: Enzyme embedding
		$z_{p}$: Positive case
		$z_{n}$: Negative case, selected to have EC numbers close in Euclidean space to the positive case
		$\alpha$: Margin; set to 1
* The **supercon hard loss** used by [[10.1126__science.adf2465|Yu et al 2023a]]:		
		$$L^{sup} = \sum_{e \in E}{\frac{-1}{|P(E)|}} \sum_{z_{p} \in P(e)}{log \frac{ \exp (z_{e}z_{p}/\tau)}{\sum_{z_{a} \in A(e)} \exp (z_{i} z_{a} / \tau)}}$$ 
		$\tau$: temperature, set to 0.1 in the paper
* **Noise contrastive estimation** (variant 1): 
	$$L_{B} ( \theta, \gamma )=\log \sigma (s(x_{i}, a^{+}_{i,0}; \theta), \gamma) + \sum^{K}_{k=1} \log (1 - \sigma ( s ( x_{i}, a^{-}_{i,k}; \theta), \gamma)$$
	$x_{i}$: Input text
	$a_{i, \circ}$: Another example (either positive or negative)
	$s(x_{i}, a_{i, \circ}; \theta)$ : Scoring function, usually cosine similarity, dot product, or logit "produced by input-sample matcher sub-network" (from Rethmeier and Augenstein 2021)
	$\sigma(z, \gamma)$: Scaling function, usually sigmoid
* **Noise contrastive estimation** (variant 2, ranks a single positive pair over $K$ negative pairs):
Variant 2 ranks a single positive pair over $K$ negative pairs
	 $$L_{R}= \log \frac{\exp (\bar{s} * (x_{I}, a^{+}_{i,0}; \theta_))}{\exp (\bar{s} * (x_{I}, a^{+}_{i,0}; \theta_)) + \sum^{K}_{k=1} \exp (\bar{s} * (x_{I}, a^{-}_{i,k}; \theta))}$$

<!-- generated -->
