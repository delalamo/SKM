---
title: TM-score
aliases:
  - "TM-score"
  - "ipTM"
  - "ipSAE"
  - "tags/tm-score"
created: "2024-06-26T13:44:46"
modified: "2026-06-23T11:45:43"
tags:
  - evidence/measurements
  - prediction/confidence
---

#### Summary

**TM-score** is an alignment-dependent protein structure similarity term introduced by [@zhang2004] that is widely used for assessing [[notes/structure-prediction|protein structure prediction]] methods. It is defined as:

$$
TM\text{-}score = max \left[\frac{1}{L_{target}} \sum_{i}^{L_{common}} \left(\frac{1}{1+ \left( \frac{d_{i}}{d_{0} \left( L_{target} \right)} \right)^{2}} \right) \right]
$$

$L_{target}$: length of the amino acid sequence of the target protein
$L_{common}$: number of residues in both the target and query proteins
$d$: Distance between pairs of residues
$d_{0}(L_{target}) = 1.24*\sqrt[3]{L_{target}-15}-1.8$: Distance scaling factor

#### Predicted variants

[[notes/structure-prediction|Protein folding neural networks]] such as [[notes/alphafold2|AlphaFold2]] and [[notes/alphafold3|AlphaFold3]] predict a distribution over aligned errors for each ordered residue pair, then use that distribution to calculate pTM and ipTM confidence scores [@jumper2021; @evans2021]. For bin center $\Delta_b$ and probability $p_{ijb}$, the expected TM contribution for a residue pair is:

$$
E_{ij} = \sum_b p_{ijb}\frac{1}{1+\left(\frac{\Delta_b}{d_0(L)}\right)^2}
$$

**ipTM** (interface predicted TM-score) uses this same TM-score transform, but masks the average to residues in other chains:

$$
ipTM = \max_i \left[\frac{1}{|J_i|}\sum_{j \in J_i} E_{ij}\right], \quad J_i = \{j : chain(j) \ne chain(i)\}
$$

$L$ is the number of modeled residues used for $d_0$. In practice, ipTM is an inter-chain pTM score rather than a direct interface-contact score: all residues in other chains can contribute, not just residues close in 3D.

**ipSAE** (interaction prediction score from aligned errors) is a [[notes/pae|PAE]]-derived replacement for ipTM calculated after choosing a PAE cutoff $\tau$ [@dunbrack2025]. For a chain direction $A \to B$ and aligned residue $i \in A$, it keeps only residues in the other chain with $PAE_{ij}<\tau$ and computes:

$$
pSAE_i(A \to B)= \frac{1}{|S_i|} \sum_{j \in S_i}\frac{1}{1+\left(\frac{PAE_{ij}}{d_0(|S_i|)}\right)^2}, \quad S_i = \{j \in B: PAE_{ij}<\tau\}
$$

Then:

$$
ipSAE(A \to B)=\max_{i \in A} pSAE_i(A \to B)
$$

The reported pairwise "max" score is the maximum of the two chain directions. Compared with ipTM, ipSAE specifically improves robustness to construct length, disordered tails, and accessory domains because it scores only confident inter-chain residue pairs, uses a local $d_0$ based on those residues rather than full chain/complex length, and uses the output PAE matrix rather than requiring AlphaFold's internal aligned-error logits [@dunbrack2025].
