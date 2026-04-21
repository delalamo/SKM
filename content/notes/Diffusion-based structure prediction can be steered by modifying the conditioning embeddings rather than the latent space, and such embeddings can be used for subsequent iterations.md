---
tags:
  - diffusion-models/structure-prediction
  - diffusion-guidance/structure-prediction
  - protein-folding/structure-prediction
created: "2026-04-10T15:35:05"
modified: "2026-04-21T07:03:26"
---

#### Summary

**[[tags/diffusion-models|Diffusion]]-based [[tags/structure-prediction|structure prediction]] can be [[tags/diffusion-guidance|steered]] into specific conformations by modifying conditioning embeddings rather than the latent-space embeddings used for diffusion** [@li2026robust; @maddipatla2026]. This has the added advantage of being reused, and therefore facilitating improvements, in sequential diffusion runs. This was done using [[cryo-EM]] and [[NMR]] data and was shown to slightly outperform standard Diffusion Posterior Sampling.

#### Figures
![[Pasted-image-20260306093401.png]]
![[Pasted-image-20260306093452.png]]

*Figures from [@maddipatla2026]*

![[Pasted-image-20260220170148.png]]

*Ref [@li2026robust]*

#### Publication history
* 18 March 2026: https://biomlzk.ghost.io/diffusion-based-structure-prediction-can-be-guided-by-backpropagating-the-conditioning-embeddings-rather-than-the-atomic-coordinates-directly-and-such-embeddings-can-be-used-for-subsequ/
