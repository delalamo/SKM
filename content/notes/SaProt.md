---
title: SaProt
created: 2026-04-10T14:30:55
modified: "2026-08-19T16:32:04"
---

**SaProt** is a [[protein-language-models|protein language model]] trained on paired amino acid identities and [[Foldseek]] tokens derived largely from [[alphafold2|AlphaFold2]] structures [@su2023]. It outperformed sequence-only baselines across ten downstream tasks, including zero-shot [[variant-effect-prediction|variant effect prediction]].

#### Details

* Structural tokens for residues with [[plddt|pLDDT]] values less than 70 are masked.

#### See also

* [[Structural tokens improve zero-shot variant effect prediction in ESM3, but only when structures are not computationally derived]]
