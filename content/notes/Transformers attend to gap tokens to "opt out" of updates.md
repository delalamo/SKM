---
tags:
created: 2024-06-04T03:22:01
modified: 2024-06-04T03:22:01
---
#### Summary
**[[Transformer]] models will attend to gap tokens, such as \<bos\>, \<eos\>, etc., to avoid updates when calculating [[Attention (machine learning)|attention]]** [^bondarenko2023].

#### Details
This is also true of visual transformers and image data.

(Miller 2023) proposes using Quiet Attention AKA Softmax1 to avoid this:
$$
softmax_{1}(x_{i}) = \frac{\exp{x_{i}}}{1+\sum_{j}{\exp{x_{j}}}}
$$

This was used by [^billera2024] to modify the [[Invariant point attention]].

[^bondarenko2023]: Bondarenko et al. (2023) "Quantizable Transformers: Removing Outliers by Helping Attention Heads Do Nothing." NeurIPS. http://papers.nips.cc/paper_files/paper/2023/hash/edbcb7583fd8921dad78adecfe06a99b-Abstract-Conference.html
[^billera2024]: Billera et al. (2024) "The Continuous Language of Protein Structure." https://doi.org/10.1101/2024.05.11.593685
