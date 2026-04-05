---
tags:
  - protein-folding/misc
---
#### Summary
**Positional encoding** refers to the process of adding information about a token's absolute or relative position in a sequence. This is particularly important for [[Transformer|transformers]] which lack any built-in knowledge of position.

#### Absolute positional encoding
**Sinusoidal positional encodings**: Used in the original transformer (Vaswani et al 2017[^vaswani2017]). They found performance competitive with learned encodings.

> $PE(pos, 2i) = \sin \left (\frac{pos}{10000^{\frac{2i}{d_{model}}}} \right)$
> $PE(pos, 2i+1) = \cos \left (\frac{pos}{10000^{\frac{2i}{d_{model}}}} \right)$
> $i$: The index of the specific entry
> $pos$: The position of the token

![](/assets/Pasted-image-20240604083358.png)
*Figure from https://production-media.paperswithcode.com/methods/05577c08-d6ac-4b8b-9fd0-55739ba42383.png*

#### Relative positional encodings
**Rotational positional encodings**: Rotates the queries and keys prior to calculation of [[Attention (machine learning)|attention]].

![](/assets/Pasted-image-20240604084227.png)
*Figure from Su et al 2021[^su2021]*

[^vaswani2017]: Vaswani et al. (2017) "Attention Is All You Need." https://doi.org/10.48550/ARXIV.1706.03762
[^su2021]: Su et al. (2021) "RoFormer: Enhanced Transformer with Rotary Position Embedding." https://doi.org/10.48550/ARXIV.2104.09864
