---
tags:
  - structure-prediction/limitations
  - thermostability/prediction
  - plddt
created: "2026-03-06T09:43:56"
modified: "2026-04-11T07:41:30"
---

## Summary

**Protein folding neural networks cannot predict [[Stability and thermostability|stability]].** [Pak et al 2023a][^pak2023] found that ddG values did not correlate with [[pLDDT]]. [Aina et al 2023][^aina2023] found by running Hamiltonian [[Replica-exchange molecular dynamics]] on high-[[pLDDT]] designs that subsequently fell apart. Papers cited by [Diaz et al 2023][^diaz2023] showed that RMSD also does not correlate with stability, although [McBride et al 2023][^mcbride2023] showed that a custom strain score was able to predict this with some success.

## Figures

![[Pasted-image-20240624104718.png]]
*Figure from [Pak et al 2023a][^pak2023]*

## See also

* [[High-pLDDT designs can be insoluble]]
* [[Protein structure prediction and design confidence metrics do not correlate with binding affinity]]

[^pak2023]: Pak et al. (2023) "Using AlphaFold to predict the impact of single mutations on protein stability and function." *PLOS ONE*. https://doi.org/10.1371/journal.pone.0282689
[^aina2023]: Aina et al. (2023) "De Novo Design of a β-Helix Tau Protein Scaffold: An Oligomer-Selective Vaccine Immunogen Candidate for Alzheimer’s Disease." *ACS Chemical Neuroscience*. https://doi.org/10.1021/acschemneuro.3c00007
[^diaz2023]: Diaz et al. (2023) "Stability Oracle: A Structure-Based Graph-Transformer for Identifying Stabilizing Mutations." https://doi.org/10.1101/2023.05.15.540857
[^mcbride2023]: McBride et al. (2023) "AlphaFold2 Can Predict Single-Mutation Effects." *Physical Review Letters*. https://doi.org/10.1103/PhysRevLett.131.218401
