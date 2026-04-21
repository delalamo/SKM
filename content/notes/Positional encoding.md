---
tags:
created: 2024-06-04T03:24:54
modified: "2026-04-21T05:01:15"
---
#### Summary
**Positional encoding** refers to the process of adding information about a token's absolute or relative position in a sequence. This is particularly important for [[Transformer|transformers]] which lack any built-in knowledge of position.

#### Absolute positional encoding
**Sinusoidal positional encodings**: Used in the original transformer [@vaswani2017]. They found performance competitive with learned encodings.

> $PE(pos, 2i) = \sin \left (\frac{pos}{10000^{\frac{2i}{d_{model}}}} \right)$
> $PE(pos, 2i+1) = \cos \left (\frac{pos}{10000^{\frac{2i}{d_{model}}}} \right)$
> $i$: The index of the specific entry
> $pos$: The position of the token

![[Pasted-image-20240604083358.png]]
*Ref https://production-media.paperswithcode.com/methods/05577c08-d6ac-4b8b-9fd0-55739ba42383.png*

#### Relative positional encodings
**Rotational positional encodings**: Rotates the queries and keys prior to calculation of [[Attention (machine learning)|attention]].

![[Pasted-image-20240604084227.png]]
*Ref [@su2021]*
