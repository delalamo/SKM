---
title: Fitness prediction
created: 2026-04-10T14:02:57
modified: "2026-04-21T07:28:09"
---

**Fitness prediction** describes the problem of predicting a protein's fitness from its sequence, with or without structural data. It is affected by many other observables ([[thermostability|stability]], [[protein-folding|correct folding]], etc) which can lead to [[epistasis|epistasis]], which is the inability to model fitness as a linear combination of the effects of individual mutations.

![[Pasted-image-20241127045541.png]]
*Ref [@sandhu2024]*

#### Notes

* **Sequence-based predictors (e.g., PSSMs and [[Potts models]]) could miss high-fitness naturally occurring mutations** [@johnston2024].
* **Including nonfunctional sequences during training improves prediction of poor performers but not top performers** [@morenopaz2023]. This was demonstrated using several ML models.
* **Complex models are worse than ridge regression when the number of training examples is low** [@singh2025].
![[AbMAP-ridge-regression.png]]
	*Ref [@singh2025]*
* **Threshold robustness** refers to the fact that slightly deleterious mutations that negatively effect [[thermostability|stability]] might have no impact on fitness up to a certain point, and that the effects can be devastating beyond this point.
![[Fitness_sigmoidal.png]]
	*Ref [@sarkisyan2016]*

#### Evaluation

* The **Spearman correlation coefficient** is the most widely used metric for evaluating how well methods can predict protein fitness.
* **Non-Discounted Cumulative Gains** (NDCG) is used by other papers ([@paul2023; @ruffolo2024], others), and measures how well predictions at the top end of a distribution are predicted. The cutoff is user-defined.
	$$
	NDCG_p = \frac{DCG_p}{IDCG_p} = \frac{\sum_{i=1}^{p} \frac{rel_i}{\log_2(i+1)}}{\sum_{i=1}^{p} \frac{rel_i^{\text{ideal}}}{\log_2(i+1)}}
	$$

	$DCG_{p}$: Discount cumulative gain at rank $p$. This penalizes the appearance of important results far from the top of the distribution
	$IDCG_{p}$: Ideal discount cumulative gain at rank $p$; basically the above but the rank-ordering is perfect.
	$rel_{p}$: Relevance score of result ${i}$
	$rel^{ideal}_{p}$: Relevance score of result ${i}$ in its ideal position
