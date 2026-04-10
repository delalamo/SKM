---
tags:
  - protein-folding/misc
created: "2024-12-31T08:39:36"
modified: "2026-04-05T23:36:09"
---

#### Summary

**Randomly masking residues prior to running [[ESMFold]] allows false positive folders to be identified** [^hermosilla2023]. This partially overcomes the limitation of ESMFold to [[AlphaFold2 outperforms ESMFold at distinguishing designable and undesignable protein backbones|fold everything]]. It also leads to marginal improvements in Spearman correlation between [[pLDDT]] and experimental [[Stability and thermostability|stability]] ($\Delta G$).

#### See also

* [[Masking ESMFold can sometimes sample alternate conformations]]

[^hermosilla2023]: Hermosilla et al. (2023) "Validation of
                  de novo
                  designed water-soluble and transmembrane proteins by
                  in silico
                  folding and melting." https://doi.org/10.1101/2023.06.06.543955
