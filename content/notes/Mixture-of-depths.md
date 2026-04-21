---
title: Mixture-of-depths
created: 2026-04-10T14:02:57
modified: "2026-04-21T05:01:15"
---

The mixture-of-depths method enforces a fixed-size compute budget for variable-length inputs to individual layers of a [[Transformer]] [@raposo2024]. In other words, only the top $k$ tokens will be used for [[Attention (machine learning)|multi-head attention]]. Raposo et al. [@raposo2024] also combined this with [[Mixture-of-experts]].

#### Figures
![[Pasted-image-20240416125054.png]]
*Ref [@raposo2024]*
