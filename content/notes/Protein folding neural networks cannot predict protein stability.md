---
tags:
  - structure-prediction/limitations
  - thermostability/prediction
  - plddt
created: "2026-03-06T09:43:56"
modified: "2026-04-21T07:28:09"
---

## Summary

**Protein folding neural networks cannot predict [[thermostability|stability]].** [@pak2023alphafold] found that ddG values did not correlate with [[plddt|pLDDT]]. [@aina2023] found by running Hamiltonian [[Replica-exchange molecular dynamics]] on high-[[plddt|pLDDT]] designs that subsequently fell apart. Papers cited by [@diaz2023] showed that RMSD also does not correlate with stability, although [@mcbride2023] showed that a custom strain score was able to predict this with some success.

## Figures

![[Pasted-image-20240624104718.png]]
*Ref [@pak2023alphafold]*

## See also

* [[High-pLDDT designs can be insoluble]]
* [[Protein structure prediction and design confidence metrics do not correlate with binding affinity]]
