---
tags:
  - inverse-folding/misc
created: 2024-06-27T01:45:36
modified: "2026-04-20T07:16:03"
---
#### Summary
**During [[Inverse folding]], the identity of about 50% of amino acids can be determined from context alone, i.e., the identities of the surrounding residues are not necessary** [^mahajan2023][^ding2024]. This could be what allows methods such as [[ProteinMPNN|MiniMPNN]] and Frame2Seq, which predict the entire sequence in a single shot, to match the performance of autoregressive methods such as [[ESM-IF]] and [[Geometric Vector Perceptrons|GVP]].

#### See also
- [[Iterative structure prediction outperforms all-at-once structure prediction]]

[^mahajan2023]: Mahajan et al. (2025) "How well do contextual protein encodings learn structure, function, and evolutionary context?." Cell Systems. https://doi.org/10.1016/j.cels.2025.101201
[^ding2024]: Ding et al. (2024) "Protein design using structure-based residue preferences." *Nature Communications*. https://doi.org/10.1038/s41467-024-45621-4
