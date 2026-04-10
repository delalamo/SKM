---
tags:
  - protein-folding/misc
created: "2025-02-27T04:19:52"
modified: "2026-04-10T14:30:55"
---

#### Summary

**Confidence metrics for structure prediction, such as pLDDT and pTM, correlate with prediction accuracy, even in the absence of coevolutionary data** [^roney2022]. This was also observed when modeling CDRH3 loops, which lack any meaningful coevolutionary signal [^chen2024]. This has been suggested to indicate that an energy function is being learned.

#### Figures

\![[Pasted-image-20240716092658.png]]

*Figure from [^roney2022]*

\![[Confidence.png]]

*Figure from [^chen2024]*

#### See also

- [[Sequence- and structure-derived ML quality metrics from ML do not correlate with each other]]
- [[Protein folding neural networks make local optimizations in the absence of coevolutionary information]]

[^roney2022]: Roney & Ovchinnikov (2022) "State-of-the-Art Estimation of Protein Model Accuracy Using AlphaFold." *Physical Review Letters*. https://doi.org/10.1103/PhysRevLett.129.238101
[^chen2024]: Chen et al. (2024) "Accurate prediction of CDR-H3 loop structures of antibodies with deep learning." *eLife*. https://doi.org/10.7554/eLife.91512.4
