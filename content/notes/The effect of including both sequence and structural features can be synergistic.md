---
tags:
  - inverse-folding/evaluation
created: "2026-04-05T17:58:34"
modified: "2026-04-21T07:28:09"
summary: The effect of including both sequence and structural features can be synergistic
---
#### Summary
**The benefit of including both sequence- and structure-based features during [[inverse-folding|Inverse folding]] is greater than the sum of each feature's benefit in isolation** [@wang2024spdesign].

#### Figures
| | SPDesign¹ | SPDesign² | SPDesign³ | SPDesign |
|---|---|---|---|---|
| Backbone atoms distance | ✓ | ✓ | ✓ | ✓ |
| Pre-trained knowledge of structure | ✗ | ✓ | ✗ | ✓ |
| Structural sequence profile | ✗ | ✗ | ✓ | ✓ |
| Perplexity | 5.36 | 4.96 | 3.51 | 2.43 |
| Recovery (%) | 44.60 | 48.81 | 58.76 | 67.05 |
*Table 3 from [@wang2024spdesign]*
