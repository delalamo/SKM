---
tags:
  - protein-folding/misc
created: "2024-06-14T11:53:23"
modified: "2026-04-10T14:02:57"
---
#### Summary
**Layer normalization** is a procedure to normalize the values of each token to a gaussian with mean $\beta$ and width $\gamma$: $y=\frac{x-\mu}{\sqrt{\sigma+\epsilon}}*\gamma+\beta$ where $\mu$ and $\sigma$ are the per-token mean and standard deviations, respectively. In the original [[Transformer]] paper [^vaswani2017], the Post-LN approach was used where layer normalization followed [[Attention (machine learning)|multi-head attention]] and again after the feed-forward network, but more recent methods (as of June 2024) use the Pre-LN approach where layer normalization precedes attention and the feed-forward network [^xiong2020].

#### Figures
\![[Pasted-image-20240614175222.png]]
*Figure from [^xiong2020]*

[^vaswani2017]: Vaswani et al. (2017) "Attention Is All You Need." https://doi.org/10.48550/ARXIV.1706.03762
[^xiong2020]: Xiong et al. (2020) "On Layer Normalization in the Transformer Architecture." *arXiv*. https://doi.org/10.48550/ARXIV.2002.04745
