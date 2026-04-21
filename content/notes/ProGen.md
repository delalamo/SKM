---
title: ProGen
created: 2026-04-10T14:30:55
modified: "2026-04-21T05:01:15"
---

**ProGen** is a family of autoregressive [[Protein language models|protein language models]]. **ProGen2** has been extensively shown to be capable of designing new sequences from scratch if fine-tuned; see [[PLMs generate more divergent functional proteins than Potts models]] [@nijkamp2023; @bhatnagar2025]. **ProGen3** adopts a [[Mixture-of-experts]] architecture, is also capable of infilling masked spans, and can design proteins that express *in vitro* even without fine-tuning.

#### Uses

[@madani2023] used a fine-tuned version of ProGen to generate functional lysozymes with low sequence identify to natural proteins.

[@ruffolo2025] generated four million [[CRISPR-Cas9|CRISPR]] proteins and one million [[CRISPR-Cas9|Cas9]] proteins using fine-tuned versions of ProGen. Half were prompted with the N- or C-terminal 50 residues of natural enzymes, while the other half were fully *de novo*. The generated sequences were well distributed across the various sub-families of these proteins, and the observed [[pLDDT]] values from [[AlphaFold2]] were above 80 for >80% and >99.4%, respectively.
