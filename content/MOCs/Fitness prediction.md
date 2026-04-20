---
title: Fitness prediction
tags:
created: 2026-04-10T14:02:57
modified: "2026-04-20T08:16:13"
---

**Fitness prediction** describes the problem of predicting a protein's fitness from its sequence, with or without structural data. It is affected by many other observables ([[Stability and thermostability|stability]], [[Protein folding|correct folding]], etc) which can lead to [[Epistasis|epistasis]], which is the inability to model fitness as a linear combination of the effects of individual mutations.

![[Pasted-image-20241127045541.png]]
*Ref [^sandhu2024]*

#### Notes

* **Sequence-based predictors (e.g., PSSMs and [[Potts models]]) could miss high-fitness naturally occurring mutations** ([[10.1073__pnas.2400439121|Johnston et al 2024]]).
* **Including nonfunctional sequences during training improves prediction of poor performers but not top performers** ([[10.1021__acssynbio.4c00035|Moreno-Paz et al 2024]]). This was demonstrated using several ML models.
* **Complex models are worse than ridge regression when the number of training examples is low** ([[10.1073__pnas.2418918121|Singh et al 2025]]).
![[AbMAP-ridge-regression.png]]
	*Ref [^singh2023]*
* **Threshold robustness** refers to the fact that slightly deleterious mutations that negatively effect [[Stability and thermostability|stability]] might have no impact on fitness up to a certain point, and that the effects can be devastating beyond this point.
![[Fitness_sigmoidal.png]]
	*Ref [^sarkisyan2016]*

#### Evaluation

* The **Spearman correlation coefficient** is the most widely used metric for evaluating how well methods can predict protein fitness.
* **Non-Discounted Cumulative Gains** (NDCG) is used by other papers ([[8PbTU4exnV|Paul et al 2023]], [[10.1101__2024.08.03.606485|Ruffolo et al 2024b]], others), and measures how well predictions at the top end of a distribution are predicted. The cutoff is user-defined.
	$$
	NDCG_p = \frac{DCG_p}{IDCG_p} = \frac{\sum_{i=1}^{p} \frac{rel_i}{\log_2(i+1)}}{\sum_{i=1}^{p} \frac{rel_i^{\text{ideal}}}{\log_2(i+1)}}
	$$
	
	$DCG_{p}$: Discount cumulative gain at rank $p$. This penalizes the appearance of important results far from the top of the distribution
	$IDCG_{p}$: Ideal discount cumulative gain at rank $p$; basically the above but the rank-ordering is perfect.
	$rel_{p}$: Relevance score of result ${i}$
	$rel^{ideal}_{p}$: Relevance score of result ${i}$ in its ideal position

<!-- generated -->

[^sandhu2024]: Sandhu et al. (2025) "Computational and Experimental Exploration of Protein Fitness Landscapes: Navigating Smooth and Rugged Terrains." Biochemistry. https://doi.org/10.1021/acs.biochem.4c00673

[^sarkisyan2016]: Sarkisyan et al. (2016) "Local fitness landscape of the green fluorescent protein." *Nature*. https://doi.org/10.1038/nature17995
[^singh2023]: Singh et al. (2025) "Learning the language of antibody hypervariability." Proceedings of the National Academy of Sciences. https://doi.org/10.1073/pnas.2418918121
