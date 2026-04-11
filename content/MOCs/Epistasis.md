---
title: Epistasis
tags:
  - epistasis
created: "2026-04-10T14:02:57"
modified: "2026-04-11T07:42:59"
---

**Epistasis** refers to the non-additivity of fitness effects arising from specific combinations of mutations. [[10.1101__2024.06.23.600144|Johnston et al 2024]] outline three types of epistasis: magnitude epistasis ("same direction as expected but are not perfectly additive"), sign epistasis ("effect of one of the substitutions changes direction in the context of the other"), and reciprocal epistasis ("effects of both substitutions change direction when they are made together").

![[types_of_epistasis.png]]
*Figure from [[10.1101__2024.06.23.600144|Johnston et al 2024]]*

![[Pasted-image-20231015155209.png]]
*Figure from [[10.1038__s41586-023-06328-6|Tsuboyama et al 2023]]*

#### Notes

* **Negative epistasis is approximately 100x more common than positive epistasis** ([[10.1038__nature17995|Sarkisyan et al 2016]]).
* **Rates of magnitude, sign, and reciprocal epistasis are constant across positions** ([[10.1101__2024.06.23.600144|Johnston et al 2024]]). These differed from a null additive-only model with noise, which had 74% magnitude, 22% sign, and 4% reciprocal sign epistasis.
![[Pasted-Graphic-25.png]]
	*Figure from [[10.1101__2024.06.23.600144|Johnston et al 2024]]*

#### Examples

* **The S373P mutation in the [[Spike protein]] is disadvantageous in pre-[[Omicron-variant]] versions of [[SARS-CoV-2]] but advantageous in Omicron.** Mentioned in [[bloomFitnessEffectsMutations2023]].
* **The combination of N501Y and Q498R in the [[Spike protein]] of [[SARS-CoV-2]] increases the binding affinity to [[ACE2]] by 387-fold.** This is believed to have led to the immune-evasive mutations in the [[Omicron-variant]] and was observed *in vitro* by [[10.1038__s41564-021-00954-4|Zahradník et al 2021]] prior to the emergence of Omicron:
* **One example of third-order epistasis is the J-domain, where strong non-additivity is observed among a triad, but disappears if any of the three are mutated to alanine** ([[10.1038__s41586-023-06328-6|Tsuboyama et al 2023]]).
![[Pasted-image-20231015155618.png]]
	*Figure from [[10.1038__s41586-023-06328-6|Tsuboyama et al 2023]]*

#### Measuring epistasis

![[Pasted-image-20241127060038.png]]
*Figure from [[10.48550__ARXIV.2411.12957|Sandhu et al 2024]]*
* **Graph Fourier Transform:** A decomposition that breaks down the signal (here, fitness) into distinct "epistatic orders"
* **Dirichlet energy:** quantifies how variable (i.e., rugged) the landscape is, with high energy corresponding to high ruggedness
	$$DE=\mathbf{f^{T}Lf}=\frac{1}{2}\sum_{u \sim v}{(f_{u}-f{v})^{2}}$$
* **NK model:** A linear model where $N$ is the number of sites and $K$ is the number of interacting sites; when $K=0$, effect of all mutations is linear, whereas larger $K$ indicates more interactions and therefore more epistasis

<!-- generated -->
