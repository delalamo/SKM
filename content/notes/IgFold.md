---
title: IgFold
created: 2026-04-10T14:30:55
modified: "2026-04-21T07:28:09"
---

**IgFold** is an [[antibodies|antibody]] [[antibody-structure-prediction|structure prediction]] method that uses embeddings from the AntiBERTy [@ruffolo2021] and extensively uses [[Invariant point attention|invariant point attention]] [@ruffolo2023].

#### Details

* Nodes initialized from hidden layer embeddings
* Edges initialized from all interresidue attention matrices from each layer
* Interchain embeddings across H and L chain set to zero
* Uses the two invariant point attention sets, the second of which consists of three layers with unique weights
* Includes some distilled training data from [[alphafold2|AlphaFold2]]
* Error estimation also uses [[Invariant point attention]]
* A study found it to generate [[DL structure tools introduce chiral errors such as swapped chiral centers, D-amino acids, and cis-amide bonds|unrealistic bond lengths and angles]], particularly in [[Complementarity-determining regions#CDRH3|CDRH3]]
* Results are competitive with AlphaFold Multimer
