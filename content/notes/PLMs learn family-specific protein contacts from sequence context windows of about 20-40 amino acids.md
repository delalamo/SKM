---
tags:
  - protein-language-models/representations
created: "2025-09-01T08:38:43"
modified: "2026-04-11T06:06:39"
---

## Summary

**[[Protein language models|PLMs]] learn from a sequence context of about twenty to forty amino acids** ([Zhang et al 2024][^zhang2024]). This is evidence that they have not learned how proteins fold, but have rather memorized family-specific statistics of protein motif pairings. Evidence that they learned family-specific features was observed by [Adams et al 2025][^adams2025] using [[Sparse autoencoder|sparse autoencoders]]. Nevertheless, the observation that [[Protein language models and PLM-based structure prediction generalize to de novo designed proteins]] calls this conclusion into question, at least for small globular proteins.

## Details

BOS and EOS tokens help reduce the size of the window required.

Evidence of family-specific features in ESM2-650M was observed by [Adams et al 2025][^adams2025] (see below).

## Figures

\![[Pasted-image-20240201071050.png]]
*Excerpt from [Zhang et al 2024][^zhang2024]*

\![[Family-specific-feature-beta-lactamase.png]]
*Figure from [Adams et al 2025][^adams2025]*

## See also

* [[PLM embeddings contain enough information to align proteins without fine-tuning]]

[^zhang2024]: Zhang et al. (2024) "Protein language models learn evolutionary statistics of interacting sequence motifs." *Proceedings of the National Academy of Sciences*. https://doi.org/10.1073/pnas.2406285121
[^adams2025]: Adams et al. (2025) "From Mechanistic Interpretability to Mechanistic Biology: Training, Evaluating, and Interpreting Sparse Autoencoders on Protein Language Models." https://doi.org/10.1101/2025.02.06.636901
