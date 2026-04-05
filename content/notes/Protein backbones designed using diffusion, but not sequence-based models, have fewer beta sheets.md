---
tags: protein-design/misc
---

#### Summary

**Protein [[Protein backbone design#Diffusion|structure diffusion]] produces fewer β-sheets than helices** (Lin et al 2023a[^lin2023]), **and design success rates are generally lower** (Ingraham et al 2023[^ingraham2023]). Lee et al 2023c[^lee2023] nonetheless confirmed by circular dichroism that sheet designs express and fold correctly. This tendency against sheets can be ameliorated by fine-tuning (Huguet et al 2024[^huguet2024]). In contrast, [[Protein language models|language-model]]-designed proteins do not have this bias (Alamdari et al 2023[^alamdari2023]).

#### Details

Watson et al 2023[^watson2023] do not mention this explicitly but their experimentally characterized designs are all exclusively alpha helical. In general designs that aren't fully α-helical these tend to have lower predicted TM-score when refolding (middle panel below).

#### Figures

![](/assets/Pasted-image-20240204122717.png)

*Figure 3 from Lin et al 2023a[^lin2023]*

![](/assets/Pasted-image-20231203100221.png)

*Figure 5h from Ingraham et al 2023[^ingraham2023]*

![](/assets/Pasted-image-20240204121659.png)

*Figure S14 from Ingraham et al 2023[^ingraham2023]*

![](/assets/Pasted-image-20240605181721.png)

*Figure 3 from Huguet et al 2024[^huguet2024]*

![](/assets/Pasted-image-20241105054451.png)

*Figure from Alamdari et al 2023[^alamdari2023]*

#### See also

* [[Protein backbones designed by diffusion, but not by language models, have more secondary structure]]
* [[De novo designed proteins with alpha helices are easier to predict than those with other secondary structures]]

[^lin2023]: Lin & AlQuraishi (2023) "Generating Novel, Designable, and Diverse Protein Structures by Equivariantly Diffusing Oriented Residue Clouds." https://doi.org/10.48550/arXiv.2301.12485
[^ingraham2023]: Ingraham et al. (2023) "Illuminating protein space with a programmable generative model." *Nature*. https://doi.org/10.1038/s41586-023-06728-8
[^lee2023]: Lee et al. (2023) "Score-based generative modeling for de novo protein design." *Nature Computational Science*. https://doi.org/10.1038/s43588-023-00440-3
[^huguet2024]: Huguet et al. (2024) "Sequence-Augmented SE(3)-Flow Matching For Conditional Protein Backbone Generation." https://doi.org/10.48550/ARXIV.2405.20313
[^alamdari2023]: Alamdari et al. (2023) "Protein generation with evolutionary diffusion: sequence is all you need." https://doi.org/10.1101/2023.09.11.556673
[^watson2023]: Watson et al. (2023) "De novo design of protein structure and function with RFdiffusion." *Nature*. https://doi.org/10.1038/s41586-023-06415-8
