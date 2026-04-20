---
title: Invariant point attention
tags:
created: 2026-04-10T14:02:57
modified: "2026-04-20T07:16:03"
---

The **invariant point attention** module of [[AlphaFold2]] is a widely used SE(3)-invariant module used to process protein structures. It's used for other tasks including error estimation (IgFold; [[10.1038__s41467-023-38063-x|Ruffolo et al 2023]]), processing of [[cryo-EM]] density (ModelAngelo, [[10.1038__s41586-024-07215-4|Jamali et al 2024]]), [[Inverse folding|inverse folding]] ([[10.1101__2023.12.15.571823|Akpinaroglu et al 2023]], [[ProteinMPNN#Variations|ProteinIPMP]]), [[Protein backbone design|protein backbone design]] ([[10.1101__2024.05.11.593685|Billera et al 2024]], [[10.48550__ARXIV.2405.20313|Huguet et al 2024]]), and conformational sampling ([[C4BikKsgmK|Lu et al 2024a]]). [[10.48550__arxiv.2505.11580|Liu et al 2025b]] released a faster version of this called FlashIPA.

#### Notes

* **The invariant point attention can be retrained and used for domain segmentation** ([[10.1038__s41467-023-43934-4|Lau et al 2023]]).
* **Training [[RosettaFold]]2 with invariant point attention instead of the [[SE3-transformer]] led to "unstable training performance"** ([[10.1101__2023.05.24.542179|Baek et al 2023]]).
* **Each of the three attention matrices in IPA are scaled (divided) by ** $3 * \sqrt{d_{head}}$ **instead of the normal ** $\sqrt{d_{head}}$ **found in [[Transformer|transformers]].**
* **[[10.1101__2024.05.11.593685|Billera et al 2024]] found that for protein backbone design, the layer norm benefited by moving to after the IPA/feed-forward layer but before the residual connection.** Pre-norm led to early plateauing during training, whereas post-norm (after the residual connection) "prevented scaling the number of layers in the model".
* **FlashIPA** is a faster version of IPA:
![[GPU-run-time-(s).png]]

<!-- generated -->
