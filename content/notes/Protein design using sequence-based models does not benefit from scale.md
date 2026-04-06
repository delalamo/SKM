---
tags: protein-design/misc
created: "2026-01-22T12:38:44"
modified: "2026-04-05T23:14:54"
---

#### Summary

**Protein design using [[Protein language models|sequence-based models]] does not benefit from scale** (Alamdari et al 2023[^alamdari2023]). Increasing the size of the model used for design from 38M to 650M parameters did not lead to higher [[pLDDT]] or [[Sequence perplexity|self-consistency perplexity]] of designs.

#### Figures

![](/assets/scPerplexity.png)

*Figure from Alamdari et al 2023[^alamdari2023]*

#### See also

* [[Protein property prediction using PLMs does not benefit from scale except when predicting inferring features of either structural or sparsely populated sequence families]]

[^alamdari2023]: Alamdari et al. (2023) "Protein generation with evolutionary diffusion: sequence is all you need." https://doi.org/10.1101/2023.09.11.556673
