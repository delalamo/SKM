---
tags:
  - protein-folding/misc
---
#### Summary
**[[Transformer]] models will attend to gap tokens, such as \<bos\>, \<eos\>, etc., to avoid updates when calculating [[Attention (machine learning)|attention]]** ([[10.48550__arxiv.2306.12929|Bondarenko et al 2023]]).

#### Details
This is also true of visual transformers and image data.

(Miller 2023) proposes using Quiet Attention AKA Softmax1 to avoid this:
$$
softmax_{1}(x_{i}) = \frac{\exp{x_{i}}}{1+\sum_{j}{\exp{x_{j}}}}
$$

This was used by [[10.1101__2024.05.11.593685|Billera et al 2024]] to modify the [[Invariant point attention]].
