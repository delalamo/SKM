---
tags:
  - protein-backbone-design/designability
created: "2025-02-17T05:10:10"
modified: "2026-04-21T05:01:15"
---

#### Summary

**[[Protein language models|PLMs]] and PLM-based [[Structure prediction|structure predictors]] generalize to some *de novo* designed proteins** [@verkuil2022]. Synthetic proteins designed using [[ESM]] were successfully expressed in the wet lab and adopted a structure consisted with predicted contacts. Likewise, [[ESMFold]] correctly predicted the structures of other de novo designed proteins (such as those designed by [@praetorius2023]; see [@del2023]).

#### Details

They use Gibbs sampling to generate new protein backbones by jointly considering $p(structure|sequence)$ and $p(sequence)$ (see below).

#### Figures

![[Pasted-image-20231102144615.png]]

*Ref [@verkuil2022]*

#### See also

* [[Inverse folding from MD simulations]]
