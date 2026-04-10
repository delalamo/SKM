---
title: Antibody structure prediction
tags:
  - antibody-structure-prediction
---

The **[[Antibodies|antibody]] [[Structure prediction|structure prediction]]** problem is a subclass of the protein structure prediction problem that is mostly focused on predicting the [[Complementarity-determining regions|CDRs]], specifically the [[Complementarity-determining regions#CDRH3|CDRH3]] loop that mediates antigen binding. It also sometimes includes the antibody-antigen docking problem.

#### Models

* **AbFold**: a method that concatenates information from [[IgFold]] and [[AlphaFold|AlphaFold2]] Multimer when modeling antibodies, which usually predict different conformations, leading to [[Antibody structure prediction improved with AlphaFold2 features|improved prediction quality]] ([[10.1101__2023.04.20.537598|Peng et al 2023]])
* **[[IgFold]]**: a method that uses embeddings from the [[Antibody language models|antibody LM]] AntiBERTy
* **[[ImmuneBuilder]]**: Consists of ABodyBuilder2 (for [[Antibodies]]), NanoBodyBuilder2 (for [[Nanobodies]]), and TCRBuilder2 (for [[T-cell receptors]]).

#### Structure prediction observations

*See also [[Antibody-antigen interactions]]*

<!-- generated -->
