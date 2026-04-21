---
tags:
  - structure-prediction/sampling
created: "2024-10-02T03:54:16"
modified: "2026-04-21T05:01:15"
---

#### Summary

**[[Structure prediction]] and [[Inverse folding|design]] tools trained on monomers generalize to oligomers.** [[ESMFold]] can predict the structures of some oligomers despite being trained exclusively on monomers [@lin2023], and the original released version of [[AlphaFold2]] was trained for monomers but allowed oligomers to be predicted with enough spacing between the sequences for the two chains (ColabFold). On the design side, [@mahajan2023] showed that it is possible to successfully design residues at [[Protein-protein interactions|PPI]] interfaces using models trained only on monomers, and [@dauparas2022; @torres2023] show experimental evidence of successful binder design using [[ProteinMPNN]], which was also only trained on monomers. However, they do not generalize to [[Training protein structure prediction neural networks on both positive and negative protein-protein interactions improves PPI discrimination|distinguishing between binders and nonbinders]].
