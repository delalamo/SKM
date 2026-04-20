---
tags:
  - thermostability/prediction
created: "2026-04-05T17:49:54"
modified: "2026-04-20T08:32:20"
---
#### Summary
 **Larger [[Protein language models|protein language models]] are better able to predict thermostability** [^hermann2024]. This is likely related to their ability to [[Protein property prediction using PLMs does not benefit from scale except when predicting inferring features of either structural or sparsely populated sequence families|better model structures]].

#### Figures
| Model | EPA | FLIP | Difference |
|---|---|---|---|
| ESM-1b (650M), frozen | 0.620* | 0.680* | +0.060 |
| ESM2 (35M), frozen | 0.497 | 0.610 | +0.113 |
| ESM2 (650M), frozen | 0.523 | 0.618 | +0.095 |
| ESM2 (3B), frozen | 0.674 | 0.699 | +0.025 |
| ESM2 (15B), frozen | 0.670 | 0.721 | +0.051 |
| ESM2 (35M), finetuned | 0.436 | 0.478 | +0.042 |
| ESMFold seq. rep. (650M), frozen | 0.416 | 0.546 | +0.130 |
| Mean over ESM variants | ~0.548 | ~0.603 | +0.055 |
*Ref [^hermann2024]*

#### See also
* [[Larger PLMs are better at homolog detection]]

[^hermann2024]: Hermann et al. (2024) "Beware of Data Leakage from Protein LLM Pretraining." https://doi.org/10.1101/2024.07.23.604678
