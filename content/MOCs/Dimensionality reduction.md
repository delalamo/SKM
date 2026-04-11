---
title: Dimensionality reduction
tags:
  - dimensionality-reduction
created: "2026-04-10T14:02:57"
modified: "2026-04-11T07:41:30"
---

**Dimensionality reduction** refers to the process of compressing $N$ input features into $M$ dimensions, where $M<N$.

#### Notes

* **t-SNE and UMAP distort input values** ([[10.1371__journal.pcbi.1011288|Chari & Pachter 2023]]). There are other examples of this in the single-cell omics field.
	\![[tSNE-UMAP-distortions.png]]
	*Figure from [[10.1371__journal.pcbi.1011288|Chari & Pachter 2023]]*

#### Approaches
###### Principal component analysis

**Principal component analysis** (PCA) is a standard dimensionality reduction tool widely used in data science. Per [[10.1073__pnas.2311420120|Shinn 2023]], its interpretation requires the following assumptions:
* The underlying patterns exist
* The patterns exhibited in the data are independent of one another
* The patterns combine linearly to form the data
* The data contain exclusively these patterns and additive, uncorrelated noise
* The observations are independent

![[Image-05.12.23-at-12.13.jpg]]
*Figure 1 from [[10.1073__pnas.2311420120|Shinn 2023]]*

###### t-Stochastic Neighbor Embedding

* Anecdotally, this is better for local [[Clustering|clustering]] and patterns

###### Uniform Manifold Approximation and Projection

* Anecdotally, this is better for finding global clustering and patterns

###### Autoencoders

These are in practice not used very often.
![[Pasted-image-20260126135420.png]]

###### Variational autoencoders

See [[Variational autoencoders]]

<!-- generated -->
