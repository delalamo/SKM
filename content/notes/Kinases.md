---
title: Kinases
created: 2026-04-10T14:02:57
modified: "2026-04-20T10:13:23"
---

**Kinases** are proteins that catalyze ATP-consuming Mg-dependent phosphorylation of proteins. These regulate most cellular processes in eukaryotic organisms. Consists of N-terminal sheet domain with C-helix, and a C-terminal helical domain

#### Details

As of July 2023 (last release of [@faezov2023]), there are 481 genes in the human proteome with a full-length kinase domain, and 13 with two. An estimated 437 are catalytically competent, while 57 are pseudokinases (lacking Asp in HRD motif). In the PDB there are 292, 268 of which are catalytically competent and 24 are pseudokinases.

#### Structural features

Kinases in an active state were found to consist of several structural features:
* DFG position for DFG motif, specifically the placement of the Phe side chain
* "BLAminus" backbone dihedral angles for residue preceding DFG motif (meaning that X, D, and F residue occupy B, L, and A Ramachandran angles); all of these structures are DFGin
* N-terminal salt bridge between conserved Glu of C-helix and Lys of N-terminal beta sheet. Presence of this salt bridge is strongly correlated with the "BLAminus" conformation
* H-bond between residue three after DFG (DFGxxX) and residue preceding HRD motif, found in 97% of BLAminus conformations
* Contact between alpha carbon of residue nine AAs before activation loop C-terminus
These were modeled with [[AlphaFold2]] [@faezov2023].
* *Regulatory spine:** Consists of histidine from HRD motif, phenylalanine from DFG motif, the AA four positions after conserved glutanmate salt bridge, and a final unspecified hydrophobic amino acid (usually leucine) seven positions after HPN motif.
* **DFG-in:** A conformation where the Asp side chain of the DFG-motif is in the ATP binding site, while the Phe is either in a pocket or adjacent to C-helix or N-terminal domain. Majority of ATP-bound structures in PDB are DFGin
* **DFG-out:** A conformation where the Asp side chan of the DFG-motif is not in the active site and the Phe is released from C-terminal pocket.
![[Kinase-geometry.png]]
