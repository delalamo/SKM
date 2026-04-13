---
tags:
  - alphafold3
  - protein-language-models/training
  - structure-prediction/sampling
  - conformational-dynamics/modeling
created: "2025-12-19T12:44:03"
modified: "2026-04-11T07:41:30"
---

#### Summary

**Alternate conformations can be sampled with MSA-based methods [[AlphaFold|AlphaFold2]] and [[Boltz]] by using either custom templates** [^del2022] **or custom sequences databases** (Monteiro da [^monteiro2024]) **or [[Multiple sequence alignments|MSAs]]** [^waymentsteele2023][^del2022]. For the last case, MSAs are modified either by [[Clustering|clustering]] using HDBSCAN or randomly subsampling, respectively. However, [[Protein structure prediction methods are unable to predict the energetics of a conformational landscape unless explicitly trained for that purpose|these ensembles do not correspond to the energetics of those proteins]]. MSA-based tricks were recently shown to work with Boltz ([[U87XyMPrZp|Richman et al 2025]]). These hacks circumvent the broader tendency of structure prediction methods to [[Structure prediction methods undersample the conformational space they find to be high-confidence|undersample conformations they find to be high-confidence]].

#### Details

Alternate conformations sampled via

- **Subsampled MSAs**: Fewer sequences are passed in the MSA [^del2022]. Required for addition of other restraints (e.g., via AlphaLink, [^stahl2023]). Also works for [[Complementarity-determining regions|CDRs]] of [[Nanobodies]] [^riccabona2024].
- **Masked MSA columns**: Entire columns of residues are mutated to either alanine or masked [^stein2022][^kalakoti2024]
- **Clustered MSAs**: [^waymentsteele2023]
- **Template curation**: Can more reliably influence which conformation is sampled, but requires an experimental structure (though Faezov and [^faezov2023] used models for some of their [[Kinases|kinases]]).
- **Dropout**: Shown by [^kalakoti2024] to not be very effective, unlike for docking ([[Dropout improves AF2 multimer prediction, including for antibody-antigen complexes|link]])

[^vani2023] summarized the challenge of MSA subsampling as follows:

> "The structures obtained, including those that are metastable, are not in any physically reasonable probability distribution. Nor is there an obvious way to directly obtain a distribution or free energy surface from them that could account for both enthalpy and entropy."

#### Figures

![[Pasted-image-20240423091334.png]]

*Figure from [^riccabona2024]*

![[Pasted-image-20241016074333.png]]

*Figure from [^schafer2024]*

[^del2022]: del Alamo et al. (2022) "Sampling alternative conformational states of transporters and receptors with AlphaFold2." *eLife*. https://doi.org/10.7554/eLife.75751
[^monteiro2024]: Monteiro da Silva et al. (2024) "High-throughput prediction of protein conformational distributions with subsampled AlphaFold2." *Nature Communications*. https://doi.org/10.1038/s41467-024-46715-9
[^waymentsteele2023]: Wayment-Steele et al. (2023) "Predicting multiple conformations via sequence clustering and AlphaFold2." *Nature*. https://doi.org/10.1038/s41586-023-06832-9
[^stahl2023]: Stahl et al. (2023) "Protein structure prediction with in-cell photo-crosslinking mass spectrometry and deep learning." *Nature Biotechnology*. https://doi.org/10.1038/s41587-023-01704-z
[^riccabona2024]: Riccabona et al. (2024) "Assessing AF2’s ability to predict structural ensembles of proteins." https://doi.org/10.1101/2024.04.16.589792
[^stein2022]: Stein & Mchaourab (2022) "SPEACH_AF: Sampling protein ensembles and conformational heterogeneity with Alphafold2." *PLOS Computational Biology*. https://doi.org/10.1371/journal.pcbi.1010483
[^kalakoti2024]: Kalakoti & Wallner (2024) "AFsample2: Predicting multiple conformations and ensembles with AlphaFold2." https://doi.org/10.1101/2024.05.28.596195
[^faezov2023]: Faezov & Dunbrack (2023) "AlphaFold2 models of the active form of all 437 catalytically competent human protein kinase domains." https://doi.org/10.1101/2023.07.21.550125
[^vani2023]: Vani et al. (2023) "Exploring Kinase Asp-Phe-Gly (DFG) Loop Conformational Stability with AlphaFold2-RAVE." *Journal of Chemical Information and Modeling*. https://doi.org/10.1021/acs.jcim.3c01436
[^schafer2024]: Schafer & Porter (2024) "AlphaFold2’s training set powers its predictions of fold-switched conformations." https://doi.org/10.1101/2024.10.11.617857
