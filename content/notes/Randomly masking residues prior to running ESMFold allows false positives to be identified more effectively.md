---
tags:
  - evidence/design-validation
  - prediction/stability-expression
  - prediction/confidence
created: "2024-12-31T08:39:36"
modified: "2026-04-21T07:28:09"
---

#### Summary

**Randomly masking residues prior to running [[ESMFold]] allows false positive folders to be identified** [@hermosilla2023]. This partially overcomes the limitation of ESMFold to [[AlphaFold2 outperforms ESMFold at distinguishing designable and undesignable protein backbones|fold everything]]. It also leads to marginal improvements in Spearman correlation between [[notes/plddt|pLDDT]] and experimental [[notes/thermostability|stability]] ($\Delta G$).

#### See also

* [[Masking ESMFold can sometimes sample alternate conformations]]
