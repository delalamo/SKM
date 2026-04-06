---
title: Biophysical models trained on single and double point mutations can predict effects of three or more mutations on stability
tags:
  - protein-design/misc
created: "2024-12-31T08:08:44"
modified: "2026-04-05T23:36:09"
---
#### Summary
 **Biophysical models trained on single and double point mutations can predict effects of three or more mutations on [[Stability and thermostability|stability]]** [^faure2024]. Authors trained biophysical models on single and double [[Variant effect prediction#Missense mutations|missense mutations]], which then generalized to a median of 13 mutations with high correlation. They conclude that "when global nonlinearities due to cooperative protein folding are properly accounted for and measurements are averaged across genetic backgrounds, first-order and pairwise energetic couplings provide sufficient information for many prediction tasks". In contrast, [^boyer2023], who trained an [[Graph neural networks|EGNN]] on the data from [^tsuboyama2023], found that models trained on single/double point mutations don't generalize to more mutations.

#### Figures
![](/assets/ddG-models-can't-extrapolate.png)
Purple: p < 0.05, orange: p > 0.05.
*Figure from [^boyer2023]*

#### See also
* [[Insufficient ddG data on Abs for training]]
* [[Focused protein sequence libraries are poor training sets]]

[^faure2024]: Faure et al. (2024) "The genetic architecture of protein stability." *Nature*. https://doi.org/10.1038/s41586-024-07966-0
[^boyer2023]: Boyer et al. (2023) "Predicting protein stability changes under multiple amino acid substitutions using equivariant graph neural networks." https://doi.org/10.48550/arXiv.2305.19801
[^tsuboyama2023]: Tsuboyama et al. (2023) "Mega-scale experimental analysis of protein folding stability in biology and design." *Nature*. https://doi.org/10.1038/s41586-023-06328-6
