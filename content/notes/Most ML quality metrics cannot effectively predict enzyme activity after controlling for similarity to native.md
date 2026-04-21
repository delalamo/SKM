---
tags:
  - plddt
  - variant-effect-prediction
created: 2025-02-27T04:21:03
modified: "2026-04-21T07:28:09"
---

#### Summary

**The activity of synthetic sequences that were experimentally generated and tested by [@johnson2024] could not be distinguished using common ML/statistical quality metrics.** These include [[plddt|pLDDT]], [[ESM]]-1v or MSA-transformer probabilities, [[blosum62|BLOSUM62]] distance or sequence identity from template, [[Rosetta]] scores, [[ESM-IF]] or [[ProteinMPNN]] probabilities, or [[Convolutional neural networks|CNN]]-based probabilities. These were designed using either [[MSA Transformer]], [[ancestral-sequence-reconstruction|Ancestral sequence reconstruction]], a generative adversarial network, or simply randomly chosen natural sequences ("test" in figure below). Slightly less than half were active.

#### Figures

![[Average-of-CuSOD-and-MDH-ROC-AUC-for-round-2.png]]

*Figure 2A from [@johnson2024]*

#### See also

* [[Protein folding neural networks cannot predict protein stability]]
* [[Sequence- and structure-derived ML quality metrics from ML do not correlate with each other]]
