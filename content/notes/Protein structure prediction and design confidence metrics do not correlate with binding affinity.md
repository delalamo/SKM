---
tags:
  - protein-design/misc
created: "2026-03-06T11:07:36"
modified: "2026-04-10T14:02:57"
---

#### Summary

**Confidence metrics from structural modeling and design neural networks, namely [[pLDDT]], [[TM-score|ipTM]], [[Rosetta]] scores, [[ProteinMPNN]] likelihoods, and [[ESM]]-2 log-likelihoods, do not correlate with binding for *de novo* binders** [^li2024][^kosonocky2026]. For pLDDT is also broadly true of [[Protein folding neural networks cannot predict protein stability|protein stability]]. [^maddipatla2026] showed that metrics like ipTM can quickly [[Confidence metrics for diffusion-based structure prediction methods can be improved with minimal changes to conditioning representations|respond to even small changes in the conditioning representations used to drive diffusion-based structure prediction, showing how brittle such metrics are with respect to input sequences and MSAs]].

#### Figures

\![[Pasted-image-20240624103326.png]]
*Figure from [^li2024]*

#### See also

* [[Protein folding neural networks cannot predict protein stability]]
* [[Protein structure prediction and design metrics don't correlate with expression probability]]
* [[Sequence- and structure-derived ML quality metrics from ML do not correlate with each other]]

#### Publication history

* 6 March 2026: https://delalamo.xyz/post/2026-03-06-conf-affinity

[^li2024]: Li et al. (2024) "Design of linear and cyclic peptide binders of different lengths from protein sequence information." https://doi.org/10.1101/2024.06.20.599739
[^kosonocky2026]: Kosonocky et al. (2026) "Validation and analysis of 12,000 AI-driven CAR-T designs in the
                  Bits to Binders
                  competition." https://doi.org/10.64898/2026.03.03.709355
[^maddipatla2026]: Maddipatla et al. (2026) "Inference-time optimization for experiment-grounded protein ensemble generation." https://doi.org/10.48550/ARXIV.2602.24007
