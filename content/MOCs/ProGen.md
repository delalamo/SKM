---
title: ProGen
tags:
  - progen
---

**ProGen** is a family of autoregressive [[Protein language models|protein language models]]. **ProGen2** has been extensively shown to be capable of designing new sequences from scratch if fine-tuned; see [[Proteins designed using PLMs more unique than those designed using Potts models]] ([[10.1016__j.cels.2023.10.002|Nijkamp et al 2023]], [[10.1101__2025.04.15.649055|Bhatnagar et al 2025]]). **ProGen3** adopts a [[Mixture-of-experts]] architecture, is also capable of infilling masked spans, and can design proteins that express *in vitro* even without fine-tuning.

#### Uses

[[10.1038__s41587-022-01618-2|Madani et al 2023]] used a fine-tuned version of ProGen to generate functional lysozymes with low sequence identify to natural proteins.

[[10.1038__s41586-025-09298-z|Ruffolo et al 2025]] generated four million [[CRISPR-Cas9|CRISPR]] proteins and one million [[CRISPR-Cas9|Cas9]] proteins using fine-tuned versions of ProGen. Half were prompted with the N- or C-terminal 50 residues of natural enzymes, while the other half were fully *de novo*. The generated sequences were well distributed across the various sub-families of these proteins, and the observed [[pLDDT]] values from [[AlphaFold|AlphaFold2]] were above 80 for >80% and >99.4%, respectively.

<!-- generated -->
