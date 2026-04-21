---
title: TM-score
aliases:
  - TM-score
created: "2024-06-26T13:44:46"
modified: "2026-04-20T10:13:23"
---

#### Summary

**TM-score** is an alignment-dependent protein structure similarity term introduced by [@zhang2004] that is widely used for assessing [[tags/structure-prediction|protein structure prediction]] methods. It is defined as:

$$
TM\text{-}score = max \left[\frac{1}{L_{target}} \sum_{i}^{L_{common}} \left(\frac{1}{1+ \left( \frac{d_{i}}{d_{0} \left( L_{target} \right)} \right)^{2}} \right) \right]
$$

$L_{target}$: length of the amino acid sequence of the target protein
$L_{common}$: number of residues in both the target and query proteins
$d$: Distance between pairs of residues
$d_{0}(L_{target}) = 1.24*\sqrt[3]{L_{target}-15}-1.8$: Distance scaling factor
