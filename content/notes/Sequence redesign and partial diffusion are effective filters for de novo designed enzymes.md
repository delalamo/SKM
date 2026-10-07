---
title: Sequence redesign and partial diffusion are effective filters for de novo designed enzymes
tags:
  - design/enzymes
  - evidence/design-validation
created: "2026-10-07"
modified: "2026-10-07T08:57:11"
---

#### Summary

**Multiple [[Inverse folding|sequence redesigns]] and partial [[Diffusion models|diffusion]] are effective filters for de novo designed enzymes** [@wu2026_B]. Briefly, this involves redesigning the sequence with a fixed backbone, or running partial diffusion and co-designing sequence and backbone, and running the same validation metrics on the resulting designs. The filtering method's effectiveness was recorded in a range of enzymes, including Kemp eliminases and serine esterases, using AlphaProtein Novo. Recall was noted to drop using this approach, meaning some true positives (enzymatically active molecules) were filtered out.

#### Details

The approach may help identify broad sequence/structure basins, implying that such basins are more likely to contain true positives than narrow areas of the function space that score well. This is similar to an observation in [[Structure prediction|structural modeling]] that found that ground-truth structures were more likely to be found in broad well-scoring basins than narrow ones [@shortle1998].

#### Figures

![[alphaprotein-novo-enzyme-filters.png]]

_Ref [@wu2026_B]_

#### See also

- [[Partial structure diffusion can make de novo backbones more designable]]
- [[Most ML quality metrics cannot effectively predict enzyme activity after controlling for similarity to native]]
- [[Multiple-seed forward folding marginally improves precision on de novo designed enzymes]]

#### Sources

- [Source issue #982](https://github.com/delalamo/SKM/issues/982).
