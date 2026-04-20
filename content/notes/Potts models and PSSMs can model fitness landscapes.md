---
title: Potts models and PSSMs can model fitness landscapes
tags:
  - conformational-dynamics/evolution
created: "2024-04-29T14:38:30"
modified: "2026-04-20T07:16:03"
---
#### Summary
 **[[Potts models]] derived from [[Multiple sequence alignments|MSAs]] can be used as the basis to model fitness landscapes** [^sesta2023]. This is proposed to take epistatic effects into account. Fannjiang and [^fannjiang2023] give several citations for these correlating with actual fitness landscapes. However, [[MSA Transformer]] seemed to outperform Potts in this regard [^lupo2022][^sgarbossa2023]. While PSSMs can also be used, they do not account for any higher-order interactions.

[^sesta2023]: Sesta et al. (2024) "Inference of annealed protein fitness landscapes with AnnealDCA." PLOS Computational Biology. https://doi.org/10.1371/journal.pcbi.1011812
[^fannjiang2023]: Fannjiang & Listgarten (2023) "Is novelty predictable?." *arXiv*. https://doi.org/10.48550/arXiv.2306.00872
[^lupo2022]: Lupo et al. (2022) "Protein language models trained on multiple sequence alignments learn phylogenetic relationships." *Nature Communications*. https://doi.org/10.1038/s41467-022-34032-y
[^sgarbossa2023]: Sgarbossa et al. (2023) "Generative power of a protein language model trained on multiple sequence alignments." *eLife*. https://doi.org/10.7554/eLife.79854
