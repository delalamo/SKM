---
tags:
  - structure-prediction
created: "2026-04-05T17:37:18"
modified: "2026-04-11T06:06:39"
---

#### Summary

**Iterative [[Structure prediction|protein structure prediction]] outperforms all-at-once structure prediction** [^hayes2025]. This was pronounced for difficult targets (e.g., [[CASP14]] and [[CASP15]] proteins), whereas easy targets (CAMEO) could be predicted using either approach.

#### Figures

| | Iterative / O(L³) | | | Argmax / O(L²) | | |
|---|---|---|---|---|---|---|
| **Model** | **CAMEO** | **CASP14** | **CASP15** | **CAMEO** | **CASP14** | **CASP15** |
|---|---|---|---|---|---|---|
| 1.4B Open | 0.830 | 0.705 | 0.733 | 0.805 | 0.640 | 0.677 |
| 1.4B Overtrained | 0.846 | 0.714 | 0.750 | 0.825 | 0.651 | 0.700 |
| 1.4B | 0.807 | 0.693 | 0.697 | 0.775 | 0.608 | 0.636 |
| 7B | 0.870 | 0.742 | 0.764 | 0.852 | 0.607 | 0.726 |
| 98B | 0.895 | 0.763 | 0.801 | 0.884 | 0.719 | 0.770 |
| ESMFold | 0.865 | 0.728 | 0.735 | | | |
| AlphaFold2 | 0.904 | 0.846 | 0.826 | | | |

*Figure from [^hayes2025]*

[^hayes2025]: Hayes et al. (2025) "Simulating 500 million years of evolution with a language model." *Science*. https://doi.org/10.1126/science.ads0018
