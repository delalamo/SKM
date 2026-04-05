---
tags:
  - protein-folding/misc
---

## Summary

**[[Protein language models|PLMs]] learn from a sequence context of about twenty to forty amino acids** ([Zhang et al 2024](https://doi.org/10.1073/pnas.2406285121)). This is evidence that they have not learned how proteins fold, but have rather memorized family-specific statistics of protein motif pairings. Evidence that they learned family-specific features was observed by [Adams et al 2025](https://doi.org/10.1101/2025.02.06.636901) using [[Sparse autoencoder|sparse autoencoders]]. Nevertheless, the observation that [[Protein language models and PLM-based structure prediction generalize to de novo designed proteins]] calls this conclusion into question, at least for small globular proteins.

## Details

BOS and EOS tokens help reduce the size of the window required.

Evidence of family-specific features in ESM2-650M was observed by [Adams et al 2025](https://doi.org/10.1101/2025.02.06.636901) (see below).

## Figures

![](/assets/Pasted-image-20240201071050.png)
*Excerpt from [Zhang et al 2024](https://doi.org/10.1073/pnas.2406285121)*

![](/assets/Family-specific-feature-beta-lactamase.png)
*Figure from [Adams et al 2025](https://doi.org/10.1101/2025.02.06.636901)*

## See also

* [[PLM embeddings contain enough information to align proteins without fine-tuning]]
