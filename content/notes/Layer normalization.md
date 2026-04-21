---
tags:
created: 2024-06-14T11:53:23
modified: "2026-04-21T05:01:15"
---
#### Summary
**Layer normalization** is a procedure to normalize the values of each token to a gaussian with mean $\beta$ and width $\gamma$: $y=\frac{x-\mu}{\sqrt{\sigma+\epsilon}}*\gamma+\beta$ where $\mu$ and $\sigma$ are the per-token mean and standard deviations, respectively. In the original [[Transformer]] paper [@vaswani2017], the Post-LN approach was used where layer normalization followed [[Attention (machine learning)|multi-head attention]] and again after the feed-forward network, but more recent methods (as of June 2024) use the Pre-LN approach where layer normalization precedes attention and the feed-forward network [@xiong2020].

#### Figures
![[Pasted-image-20240614175222.png]]
*Ref [@xiong2020]*
