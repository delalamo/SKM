---
tags:
  - structure-prediction/sampling
  - conformational-dynamics/modeling
created: 2025-12-19T12:44:03
modified: "2026-04-21T05:01:15"
---

#### Summary

**Alternate conformations can be sampled with MSA-based methods [[AlphaFold2]] and [[AlphaFold3|Boltz]] by using either custom templates** [@delalamo2022sampling] **or custom sequences databases** [@monteiro2024] **or [[Multiple sequence alignments|MSAs]]** [@waymentsteele2023; @delalamo2022sampling]. For the last case, MSAs are modified either by [[Clustering|clustering]] using HDBSCAN or randomly subsampling, respectively. However, [[Protein structure prediction methods are unable to predict the energetics of a conformational landscape unless explicitly trained for that purpose|these ensembles do not correspond to the energetics of those proteins]]. MSA-based tricks were recently shown to work with Boltz [@richman2025]. These hacks circumvent the broader tendency of structure prediction methods to [[Structure prediction methods undersample the conformational space they find to be high-confidence|undersample conformations they find to be high-confidence]].

#### Details

Alternate conformations sampled via

- **Subsampled MSAs**: Fewer sequences are passed in the MSA [@delalamo2022sampling]. Required for addition of other restraints (e.g., via AlphaLink, [@stahl2023]). Also works for [[Complementarity-determining regions|CDRs]] of [[Nanobodies|nanobodies]] [@riccabona2024].
- **Masked MSA columns**: Entire columns of residues are mutated to either alanine or masked [@stein2022; @kalakoti2024]
- **Clustered MSAs**: [@waymentsteele2023]
- **Template curation**: Can more reliably influence which conformation is sampled, but requires an experimental structure (though Faezov and [@faezov2023] used models for some of their [[Kinases|kinases]]).
- **Dropout**: Shown by [@kalakoti2024] to not be very effective, unlike for docking ([[Dropout improves AF2 multimer prediction, including for antibody-antigen complexes|link]])

[@vani2023exploring] Vani et al summarized the challenge of MSA subsampling as follows:

> "The structures obtained, including those that are metastable, are not in any physically reasonable probability distribution. Nor is there an obvious way to directly obtain a distribution or free energy surface from them that could account for both enthalpy and entropy."

#### Figures

![[Pasted-image-20240423091334.png]]

*Ref [@riccabona2024]*

![[Pasted-image-20241016074333.png]]

*Ref [@schafer2024]*
