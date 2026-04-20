---
tags:
  - structure-prediction/limitations
  - thermostability/prediction
  - plddt
created: "2026-03-06T09:43:56"
modified: "2026-04-20T07:46:00"
---

## Summary

**Protein folding neural networks cannot predict [[Stability and thermostability|stability]].** Pak et al 2023a [@pak2023alphafold] found that ddG values did not correlate with [[pLDDT]]. Aina et al 2023 [@aina2023] found by running Hamiltonian [[Replica-exchange molecular dynamics]] on high-[[pLDDT]] designs that subsequently fell apart. Papers cited by Diaz et al 2023 [@diaz2023] showed that RMSD also does not correlate with stability, although McBride et al 2023 [@mcbride2023] showed that a custom strain score was able to predict this with some success.

## Figures

![[Pasted-image-20240624104718.png]]
*Figure from Pak et al 2023a [@pak2023alphafold]*

## See also

* [[High-pLDDT designs can be insoluble]]
* [[Protein structure prediction and design confidence metrics do not correlate with binding affinity]]
