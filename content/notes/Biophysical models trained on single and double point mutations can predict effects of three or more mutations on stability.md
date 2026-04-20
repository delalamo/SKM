---
title: Biophysical models trained on single and double point mutations can predict effects of three or more mutations on stability
tags:
  - thermostability/prediction
created: "2024-12-31T08:08:44"
modified: "2026-04-20T07:46:00"
---
#### Summary
 **Biophysical models trained on single and double point mutations can predict effects of three or more mutations on [[Stability and thermostability|stability]]** [@faure2024]. Authors trained biophysical models on single and double [[Variant effect prediction#Missense mutations|missense mutations]], which then generalized to a median of 13 mutations with high correlation. They conclude that "when global nonlinearities due to cooperative protein folding are properly accounted for and measurements are averaged across genetic backgrounds, first-order and pairwise energetic couplings provide sufficient information for many prediction tasks". In contrast, [@boyer2023], who trained an [[Graph neural networks|EGNN]] on the data from [@tsuboyama2023], found that models trained on single/double point mutations don't generalize to more mutations.

#### Figures
![[ddG-models-can't-extrapolate.png]]
Purple: p < 0.05, orange: p > 0.05.
*Figure from [@boyer2023]*

#### See also
* [[Insufficient ddG data on Abs for training]]
* [[Focused protein sequence libraries are poor training sets]]
