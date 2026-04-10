---
tags:
  - antibodies/misc
created: "2026-04-05T17:48:59"
modified: "2026-04-10T14:30:55"
---
#### Summary
 **[[Inverse folding]] of [[Complementarity-determining regions|CDRs]] benefits from masking contiguous stretches of residues during training** ([[bxZMKHtlL6|Høie et al 2023]]). This is in contrast to inverse folding of [[Framework region|framework residues]], which like generic proteins benefit from random masking (AKA "shotgun masking"; [^hsu2022]).

#### Figures
| Exp/Pred | Layer Decay | OAS Gaussian Noise | Test Masking | FR Avg. | CDR1H | CDR2H | CDR3H | CDR1L | CDR2L | CDR3L |
|---|---|---|---|---|---|---|---|---|---|---|
| Exp | - | - | None | **0.898** | 0.731 | **0.712** | 0.569 | **0.723** | *0.736* | 0.718 |
| Exp | - | ✓ | None | **0.898** | *0.735* | 0.698 | 0.566 | 0.716 | 0.702 | 0.713 |
| Exp | ✓ | - | None | *0.895* | **0.741** | 0.700 | **0.584** | 0.716 | **0.741** | *0.725* |
| Exp | ✓ | ✓ | None | 0.894 | 0.727 | *0.702* | 0.573 | 0.720 | 0.728 | **0.727** |
| Exp | - | - | CDRs | **0.894** | 0.680 | 0.637 | *0.432* | 0.677 | *0.689* | **0.661** |
| Exp | - | ✓ | CDRs | **0.894** | **0.696** | 0.651 | **0.434** | **0.692** | 0.680 | *0.659* |
| Exp | ✓ | - | CDRs | 0.890 | 0.675 | **0.657** | 0.431 | 0.666 | *0.689* | 0.658 |
| Exp | ✓ | ✓ | CDRs | *0.891* | *0.681* | 0.653 | 0.430 | 0.666 | **0.698** | 0.655 |
| Pred | - | - | None | **0.909** | **0.753** | *0.716* | 0.561 | 0.738 | 0.731 | *0.722* |
| Pred | - | ✓ | None | 0.905 | 0.749 | 0.704 | 0.558 | 0.729 | 0.725 | *0.722* |
| Pred | ✓ | - | None | *0.907* | *0.750* | **0.730** | **0.572** | **0.746** | **0.737** | **0.730** |
| Pred | ✓ | ✓ | None | 0.903 | 0.744 | 0.713 | 0.554 | *0.744* | *0.733* | 0.718 |
| Pred | - | - | CDRs | **0.904** | *0.706* | 0.650 | **0.445** | *0.691* | *0.687* | **0.665** |
| Pred | - | ✓ | CDRs | 0.901 | **0.709** | 0.657 | *0.435* | **0.701** | **0.690** | 0.658 |
| Pred | ✓ | - | CDRs | 0.903 | 0.695 | 0.654 | *0.435* | 0.675 | 0.675 | 0.654 |
| Pred | ✓ | ✓ | CDRs | 0.898 | 0.699 | 0.647 | 0.433 | 0.682 | 0.682 | *0.658* |
*Table from [[bxZMKHtlL6|Høie et al 2023]]*

[^hsu2022]: Hsu et al. (2022) "Learning inverse folding from millions of predicted structures." https://doi.org/10.1101/2022.04.10.487779
