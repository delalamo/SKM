---
tags: protein-design/misc
---

#### Summary

**[[Protein language models|PLMs]] and PLM-based [[Structure prediction|structure predictors]] generalize to some *de novo* designed proteins** (Verkuil et al 2022[^verkuil2022]). Synthetic proteins designed using [[ESM]] were successfully expressed in the wet lab and adopted a structure consisted with predicted contacts. Likewise, [[ESMFold]] correctly predicted the structures of other de novo designed proteins (such as those designed by Praetorius et al 2023[^praetorius2023]; see del Alamo et al 2023[^del2023]).

#### Details

They use Gibbs sampling to generate new protein backbones by jointly considering $p(structure|sequence)$ and $p(sequence)$ (see below).

#### Figures

![](/assets/Pasted-image-20231102144615.png)

*Figure from Verkuil et al 2022[^verkuil2022]*

#### See also

* [[Inverse folding from MD simulations]]

[^verkuil2022]: Verkuil et al. (2022) "Language models generalize beyond natural proteins." https://doi.org/10.1101/2022.12.21.521521
[^praetorius2023]: Praetorius et al. (2023) "Design of stimulus-responsive two-state hinge proteins." *Science*. https://doi.org/10.1126/science.adg7731
[^del2023]: del Alamo et al. (2023) "Conformational sampling and interpolation using language-based protein folding neural networks." https://doi.org/10.1101/2023.12.16.571997
