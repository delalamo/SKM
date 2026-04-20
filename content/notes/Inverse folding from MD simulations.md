---
tags:
  - inverse-folding/evaluation
created: 2025-05-23T04:29:43
modified: "2026-04-20T10:13:23"
---
#### Summary
 **The combination of [[MD simulations]] with [[Inverse folding|inverse folding]] was explored by [^brotzakis2025] in redesigning a [[Nanobodies|nanobody]] to have slower dissociation from its [[Antibody-antigen interactions|antigen]].**

#### Details
Brotzakis et al. use a Bayesian framework to link exploration of the conformational space by MD ($p(struct|seq)$) with exploration of sequence space by inverse folding ($p(seq|struct)$). For a single sequence, comparison of the latter to the former would be as follows.[^brotzakis2025]
$$
p(seq|struct) = \frac{p(struct|seq)p(seq)}{p(struct)}
$$

They rearrange this formula by only considering the conformational space of mutants relative to the starting sequence:

$$
p(struct|seq_{mut}) = p(struct|seq_{wt}) \frac{p(seq_{mut}|struct)p(seq_{wt})}{p(seq_{wt}|struct)p(seq_{mut})}
$$

#### See also
* [[Protein language models and PLM-based structure prediction generalize to de novo designed proteins]]
* [[Inverse folding can generate more stable sequences when jointly run alongside a protein folding model]]
* [[Inverse folding NNs are better predictors of equilibrium dynamics than protein folding NNs]]

[^brotzakis2025]: Brotzakis et al. (2025) "Design of Protein Sequences with Precisely Tuned Kinetic Properties." https://doi.org/10.1101/2025.02.13.638027
