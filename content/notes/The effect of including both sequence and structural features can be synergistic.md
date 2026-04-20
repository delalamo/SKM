---
tags:
  - inverse-folding/evaluation
  - inverse-folding/observations
  - protein-language-models/applications
created: "2026-04-05T17:58:34"
modified: "2026-04-20T09:16:21"
summary: The effect of including both sequence and structural features can be synergistic
---
#### Summary
**The benefit of including both sequence- and structure-based features during [[Inverse folding]] is greater than the sum of each feature's benefit in isolation** [^wang2023].

#### Figures
| | SPDesign¹ | SPDesign² | SPDesign³ | SPDesign |
|---|---|---|---|---|
| Backbone atoms distance | ✓ | ✓ | ✓ | ✓ |
| Pre-trained knowledge of structure | ✗ | ✓ | ✗ | ✓ |
| Structural sequence profile | ✗ | ✗ | ✓ | ✓ |
| Perplexity | 5.36 | 4.96 | 3.51 | 2.43 |
| Recovery (%) | 44.60 | 48.81 | 58.76 | 67.05 |
*Table 3 from [^wang2023]*

[^wang2023]: Wang et al. (2024) "SPDesign: protein sequence designer based on structural sequence profile using ultrafast shape recognition." Briefings in Bioinformatics. https://doi.org/10.1093/bib/bbae146
