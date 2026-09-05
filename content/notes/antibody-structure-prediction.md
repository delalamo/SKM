---
title: Antibody structure prediction
aliases:
  - "Antibody structure prediction"
  - "tags/antibody-structure-prediction"
created: 2026-04-10T14:30:55
modified: "2026-04-20T10:13:23"
tags:
  - prediction/antibody-structure
  - prediction/complexes
---

The **[[tags/antibodies|antibody]] [[notes/structure-prediction|structure prediction]]** problem is a subclass of the protein structure prediction problem that is mostly focused on predicting the [[Complementarity-determining regions|CDRs]], specifically the [[Complementarity-determining regions#CDRH3|CDRH3]] loop that mediates antigen binding. It also sometimes includes the antibody-antigen docking problem.

#### Models

- **AbFold**: a method that concatenates information from [[IgFold]] and [[notes/alphafold2|AlphaFold2]] Multimer when modeling antibodies, which usually predict different conformations, leading to [[Antibody structure prediction improved with AlphaFold2 features|improved prediction quality]] [@peng2023]
- **[[IgFold]]**: a method that uses embeddings from the antibody-specific [[notes/protein-language-models|PLM]] AntiBERTy
- **[[ImmuneBuilder]]**: Consists of ABodyBuilder2 (for [[tags/antibodies|Antibodies]]), NanoBodyBuilder2 (for [[Nanobodies]]), and TCRBuilder2 (for [[T-cell receptors]]).
