---
tags:
created: 2024-06-04T03:22:01
modified: 2024-06-04T03:22:01
---
#### Summary
**[[Transformer]] models will attend to gap tokens, such as \<bos\>, \<eos\>, etc., to avoid updates when calculating [[Attention (machine learning)|attention]]** [@bondarenko2023].

#### Details
This is also true of visual transformers and image data.

(Miller 2023) proposes using Quiet Attention AKA Softmax1 to avoid this:
$$
softmax_{1}(x_{i}) = \frac{\exp{x_{i}}}{1+\sum_{j}{\exp{x_{j}}}}
$$

This was used by [@billera2024] to modify the [[Invariant point attention]].
