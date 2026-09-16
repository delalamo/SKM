---
title: Protein interface space remains far from complete despite recurring local geometries
aliases:
  - Protein-protein interaction interfaces are highly degenerate
  - notes/Protein-protein interaction interfaces are highly degenerate
tags:
  - biophysics/interactions
created: 2024-10-02T16:11:39
modified: "2026-09-16T12:02:38"
---
#### Summary

**The experimentally characterized space of [[Protein-protein interactions|protein–protein interfaces]] remains substantially incomplete.** Foldseek-Interface shows that new interface types continue to be discovered even as discovery of new protein structural families slows. Recurring local packing geometries therefore do not establish that the repertoire of complete interfaces is nearly exhausted [@strom2026].

#### Details

Foldseek-Interface grouped approximately 3.1 million PDB dimers into 77,167 interface clusters. Continued discovery of new clusters and the underrepresentation of disorder-mediated interactions support substantial remaining structural diversity. The cluster count depends on the similarity definition and threshold; it is not an estimate of the total number of interfaces in nature [@strom2026].

#### Reconciling earlier evidence

Earlier studies demonstrated redundancy among interacting nine-residue fragments and geometric similarities between domain interfaces [@su2024; @verma2019]. These results support reuse of structural motifs. They do not establish completeness of the interface repertoire.

Foldseek-Interface also identifies shared geometries across different protein folds, but only 721 of 13,725 eligible CATH-annotated clusters contained multiple domain pairs. This restricted comparison supports some cross-fold reuse without establishing that such reuse dominates interface space [@strom2026].

The resulting interpretation is that local interface geometry is reusable, while complete binding arrangements remain diverse and incompletely sampled. Claims of near-completeness should be reconsidered in light of the broader Foldseek-Interface analysis.

#### Related

* [[AlphaFold2 recapitulates interaction biases from PDB when modeling antibodies]]
* [[Protein interface clusters rarely span experimental structure determination methods]]
* [[Protein structure more conserved than sequence]]
