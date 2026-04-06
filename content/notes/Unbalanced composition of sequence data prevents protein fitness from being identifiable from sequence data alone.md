---
tags:
  - protein-folding/misc
created: "2026-01-22T12:38:44"
modified: "2026-04-05T23:14:54"
---

#### Summary

**Unbalanced composition of protein sequence databases prevents prediction of [[Fitness prediction|fitness]] from sequence data alone, or from models derived from such data such as [[Protein language models|PLMs]]** (Weinstein et al 2022[^weinstein2022]). Those authors argue that bigger models and datasets do not guarantee improvements in fitness prediction.

#### Details

Phylogenetic effects - how sequences have evolved over time - plays a huge role in the data distribution $p_{0}$, and the ideal distribution $p^{\infty}$ and model $f$ are non-identifiable, even with infinite data. This is because it is impossible to differentiate imbalances in sampling related sequences from fitness peaks. They claim that a better data representation can be obtained by fitting a generative model $\mathcal{M} = \set{q_{\theta}: \theta \in \Theta}$ such that $p^{\infty} \in \mathcal{M}$ and $p_{0} \notin \mathcal{M}$; e.g., fitting the data distribution $p_{0}$ more poorly by making the fitting model parametric instead of non-parametric.

#### See also

- [[Protein property prediction using PLMs does not benefit from scale except when predicting inferring features of either structural or sparsely populated sequence families]]
- [[PLMs are biased by uneven distribution of sequence data in datasets such as UniRef and UniProt]]

[^weinstein2022]: Weinstein et al. (2022) "Non-identifiability and the Blessings of Misspecification in Models of Molecular Fitness." https://doi.org/10.1101/2022.01.29.478324
