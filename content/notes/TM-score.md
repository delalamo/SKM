---
tags:
  - protein-folding/misc
---
#### Summary
**TM-score** is an alignment-dependent protein structure similarity term introduced by Zhang & Skolnick 2004[^zhang2004] that is widely used for assessing [[Structure prediction|protein structure prediction]] methods. It is defined as:

$$TM\text{-}score = max \left[\frac{1}{L_{target}} \sum_{i}^{L_{common}} \left(\frac{1}{1+ \left( \frac{d_{i}}{d_{0} \left( L_{target} \right)} \right)^{2}} \right) \right]$$

$L_{target}$: length of the amino acid sequence of the target protein
$L_{common}$: number of residues in both the target and query proteins
$d$: Distance between pairs of residues
$d_{0}(L_{target}) = 1.24*\sqrt[3]{L_{target}-15}-1.8$: Distance scaling factor

[^zhang2004]: Zhang & Skolnick (2004) "Scoring function for automated assessment of protein structure template quality." *Proteins: Structure, Function, and Bioinformatics*. https://doi.org/10.1002/prot.20264
