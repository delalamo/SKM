#### Summary

**[[Diffusion models|Diffusion]]-based [[Structure prediction|structure prediction]] can be [[Guidance sampling of all-atom diffusion|steered]] into specific conformations by modifying conditioning embeddings rather than the latent-space embeddings used for diffusion** [^li2026][^maddipatla2026]. This has the added advantage of being reused, and therefore facilitating improvements, in sequential diffusion runs. This was done using [[cryo-EM]] and [[NMR]] data and was shown to slightly outperform standard Diffusion Posterior Sampling.

#### Figures
![](/assets/Pasted-image-20260306093401.png)
![](/assets/Pasted-image-20260306093452.png)

*Figures from [^maddipatla2026]*

![](/assets/Pasted-image-20260220170148.png)

*Figure from [^li2026]*

#### Publication history
* 18 March 2026: https://biomlzk.ghost.io/diffusion-based-structure-prediction-can-be-guided-by-backpropagating-the-conditioning-embeddings-rather-than-the-atomic-coordinates-directly-and-such-embeddings-can-be-used-for-subsequ/

[^li2026]: Li et al. (2026) "Robust Inference-Time Steering of Protein Diffusion Models via Embedding Optimization." https://doi.org/10.48550/ARXIV.2602.05285
[^maddipatla2026]: Maddipatla et al. (2026) "Inference-time optimization for experiment-grounded protein ensemble generation." https://doi.org/10.48550/ARXIV.2602.24007
