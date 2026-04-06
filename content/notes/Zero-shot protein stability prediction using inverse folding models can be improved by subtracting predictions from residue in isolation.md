---
title: Zero-shot protein stability prediction using inverse folding models can be improved by subtracting predictions from residue in isolation
tags:
  - antibodies/misc
created: "2025-02-04T03:01:22"
modified: "2026-04-05T23:36:09"
---
#### Summary
 **Zero-shot protein [[Stability and thermostability#Prediction|stability prediction]] using [[Inverse folding|inverse folding]] models can be improved by subtracting predictions from residue in isolation** [^dutton2024]. This corrects for the contribution of unique backbone geometries (particularly for glycine, [[Substitution matrix for inverse folding closely matches BLOSUM62 matrix except proline|proline]], valine, and isoleucine) on predictions. It is equivalent to corrections made by [[Free energy perturbation|FEP]].

#### See also
* [[PLMs downweigh probability of sequences with multiple mutations]]
* [[Inverse folding models can predict antibody-antigen binding affinities with higher accuracy by correcting with predictions from unbound state]]

[^dutton2024]: Dutton et al. (2024) "Improving Inverse Folding models at Protein Stability Prediction without additional Training or Data." https://doi.org/10.1101/2024.06.15.599145
