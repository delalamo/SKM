---
title: Generic PLMs outperform antibody-specific PLMs on zero-shot predictions of affinity changes
tags:
  - antibodies/misc
---
#### Summary
 **Generic [[Protein language models|PLMs]] outperform [[Antibodies]] [[Antibody language models|LMs]] on zero-shot prediction of affinity changes.** This was observed using [[ESM]] (Hie et al 2023[^hie2023]) and other [[BERT]]-based models (Li et al 2023[^li2023]), as well as the autoregressive model like [[ProGen]] (Nijkamp et al 2023[^nijkamp2023]). However, they are worse at predicting [[Antibody LMs outperform generic PLMs on intrafamily thermostability prediction|intra-family thermostability]] (Chungyoun et al 2024[^chungyoun2024]).

#### Details
Hie et al 2023[^hie2023] concluded this by comparing experimental binding affinity data collected on clones picked using ESM to zero-shot predictions by AbLang and SAPIENS.

The failure of antibody LMs to predict residues with high affinity may be due to their [[PLMs are biased toward germline antibodies|bias toward germline residues]].

[^hie2023]: Hie et al. (2023) "Efficient evolution of human antibodies from general protein language models." *Nature Biotechnology*. https://doi.org/10.1038/s41587-023-01763-2
[^li2023]: Li et al. (2023) "Machine learning optimization of candidate antibody yields highly diverse sub-nanomolar affinity antibody libraries." *Nature Communications*. https://doi.org/10.1038/s41467-023-39022-2
[^nijkamp2023]: Nijkamp et al. (2023) "ProGen2: Exploring the boundaries of protein language models." *Cell Systems*. https://doi.org/10.1016/j.cels.2023.10.002
[^chungyoun2024]: Chungyoun et al. (2024) "FLAb: Benchmarking deep learning methods for antibody fitness prediction." https://doi.org/10.1101/2024.01.13.575504
