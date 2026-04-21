---
title: SaProt
created: 2026-04-10T14:30:55
modified: "2026-04-21T07:03:26"
---

**SaProt** is a [[tags/protein-language-models|protein language model]] that is trained on both amino acid identities and [[Foldseek]] tokens from [[tags/alphafold2|AlphaFold2]] structures. As of mid-May 2024 it outperforms all other methods on [[tags/variant-effect-prediction|Variant effect prediction]].

#### Details

* Structural tokens for residues with [[tags/plddt|pLDDT]] values less than 70 are masked.
