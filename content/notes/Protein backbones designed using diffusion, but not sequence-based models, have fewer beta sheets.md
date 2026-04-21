---
tags:
  - diffusion-models/protein-design
  - protein-design/design
  - tm-score
created: "2024-11-04T23:45:40"
modified: "2026-04-21T07:03:26"
---

#### Summary

**Protein [[tags/protein-backbone-design#Diffusion|structure diffusion]] produces fewer β-sheets than helices** [@lin2023generating], **and design success rates are generally lower** [@ingraham2023]. [@lee2023] nonetheless confirmed by circular dichroism that sheet designs express and fold correctly. This tendency against sheets can be ameliorated by fine-tuning [@huguet2024]. In contrast, [[tags/protein-language-models|language-model]]-designed proteins do not have this bias [@alamdari2023].

#### Details

[@watson2023] do not mention this explicitly but their experimentally characterized designs are all exclusively alpha helical. In general designs that aren't fully α-helical these tend to have lower predicted TM-score when refolding (middle panel below).

#### Figures

![[Pasted-image-20240204122717.png]]

*Figure 3 from [@lin2023generating]*

![[Pasted-image-20231203100221.png]]

*Figure 5h from [@ingraham2023]*

![[Pasted-image-20240204121659.png]]

*Figure S14 from [@ingraham2023]*

![[Pasted-image-20240605181721.png]]

*Figure 3 from [@huguet2024]*

![[Pasted-image-20241105054451.png]]

*Ref [@alamdari2023]*

#### See also

* [[Protein backbones designed by diffusion, but not by language models, have more secondary structure]]
* [[De novo designed proteins with alpha helices are easier to predict than those with other secondary structures]]
