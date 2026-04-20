---
title: Mixture-of-depths
tags:
created: 2026-04-10T14:02:57
modified: "2026-04-20T08:00:05"
---

The mixture-of-depths method enforces a fixed-size compute budget for variable-length inputs to individual layers of a [[Transformer]] ([[10.48550__arXiv.2404.02258|Raposo et al 2024]]). In other words, only the top $k$ tokens will be used for [[Attention (machine learning)|multi-head attention]]. [[10.48550__arXiv.2404.02258|Raposo et al 2024]] also combined this with [[Mixture-of-experts]].

#### Figures
![[Pasted-image-20240416125054.png]]
*Figure from [@raposo2024]*

<!-- generated -->
