---
tags:
  - protein-folding/misc
created: "2024-06-27T01:45:36"
modified: "2026-04-05T23:14:54"
---
#### Summary
**During [[Inverse folding]], the identity of about 50% of amino acids can be determined from context alone, i.e., the identities of the surrounding residues are not necessary** (Mahajan et al 2023[^mahajan2023], Ding et al 2024[^ding2024]). This could be what allows methods such as [[ProteinMPNN|MiniMPNN]] and Frame2Seq, which predict the entire sequence in a single shot, to match the performance of autoregressive methods such as [[ESM-IF]] and [[Geometric Vector Perceptrons|GVP]].

#### See also
- [[Iterative structure prediction outperforms all-at-once structure prediction]]

[^mahajan2023]: Mahajan et al. (2023) "Contextual protein and antibody encodings from equivariant graph transformers." https://doi.org/10.1101/2023.07.15.549154
[^ding2024]: Ding et al. (2024) "Protein design using structure-based residue preferences." *Nature Communications*. https://doi.org/10.1038/s41467-024-45621-4
