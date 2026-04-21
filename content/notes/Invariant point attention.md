---
title: Invariant point attention
created: 2026-04-10T14:02:57
modified: "2026-04-21T07:03:26"
---

The **invariant point attention** module of [[tags/alphafold2|AlphaFold2]] is a widely used SE(3)-invariant module used to process protein structures. It's used for other tasks including error estimation (IgFold; [@ruffolo2023]), processing of [[cryo-EM]] density (ModelAngelo, [@jamali2024]), [[tags/inverse-folding|inverse folding]] ([@akpinaroglu2023], [[ProteinMPNN#Variations|ProteinIPMP]]), [[tags/protein-backbone-design|protein backbone design]] [@billera2024; @huguet2024], and conformational sampling [@lu2024a]. Liu et al. [@liu2025b] released a faster version of this called FlashIPA.

#### Notes

* **The invariant point attention can be retrained and used for domain segmentation** [@lau2023].
* **Training [[tags/rosettafold|RosettaFold]]2 with invariant point attention instead of the [[SE3-transformer]] led to "unstable training performance"** [@baek2023].
* **Each of the three attention matrices in IPA are scaled (divided) by ** $3 * \sqrt{d_{head}}$ **instead of the normal ** $\sqrt{d_{head}}$ **found in [[Transformer|transformers]].**
* **Billera et al. [@billera2024] found that for protein backbone design, the layer norm benefited by moving to after the IPA/feed-forward layer but before the residual connection.** Pre-norm led to early plateauing during training, whereas post-norm (after the residual connection) "prevented scaling the number of layers in the model".
* **FlashIPA** is a faster version of IPA:
![[GPU-run-time-(s).png]]
