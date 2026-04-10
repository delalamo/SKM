---
tags:
  - protein-folding/misc
created: "2024-10-02T03:54:16"
modified: "2026-04-05T23:36:09"
---

#### Summary

**[[Structure prediction]] and [[Inverse folding|design]] tools trained on monomers generalize to oligomers.** [[ESMFold]] can predict the structures of some oligomers despite being trained exclusively on monomers [^lin2023], and the original released version of [[AlphaFold|AlphaFold2]] was trained for monomers but allowed oligomers to be predicted with enough spacing between the sequences for the two chains (ColabFold). On the design side, [^mahajan2023] showed that it is possible to successfully design residues at [[Protein-protein interactions|PPI]] interfaces using models trained only on monomers, and [^dauparas2022] and [^torres2023] show experimental evidence of successful binder design using [[ProteinMPNN]], which was also only trained on monomers. However, they do not generalize to [[Training protein structure prediction neural networks on both positive and negative protein-protein interactions improves PPI discrimination|distinguishing between binders and nonbinders]].

[^lin2023]: Lin et al. (2023) "Evolutionary-scale prediction of atomic-level protein structure with a language model." *Science*. https://doi.org/10.1126/science.ade2574
[^mahajan2023]: Mahajan et al. (2023) "Contextual protein and antibody encodings from equivariant graph transformers." https://doi.org/10.1101/2023.07.15.549154
[^dauparas2022]: Dauparas et al. (2022) "Robust deep learning–based protein sequence design using ProteinMPNN." *Science*. https://doi.org/10.1126/science.add2187
[^torres2023]: Vázquez Torres et al. (2023) "De novo design of high-affinity binders of bioactive helical peptides." *Nature*. https://doi.org/10.1038/s41586-023-06953-1
