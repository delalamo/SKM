---
tags:
  - inverse-folding/training
created: 2025-01-02T10:42:31
modified: "2026-04-20T07:16:03"
---
#### Summary
**Designs of the [[Complementarity-determining regions#CDRH3|CDRH3]] loops of [[Trastuzumab]] are more natural when designed by models fine-tuned from a general [[Inverse folding|inverse folding]] model on structures of [[Antibodies|antibodies]] versus no fine tuning** [^mahajan2023]. Naturalness was judged using a [[Convolutional neural networks|CNN]] trained by [^mason2021]. Similar performance can be achieved by ensembling logits from an antibody-specific [[Protein language models|protein language model]] with those of the inverse folding model without fine-tuning.

[^mahajan2023]: Mahajan et al. (2025) "How well do contextual protein encodings learn structure, function, and evolutionary context?." Cell Systems. https://doi.org/10.1016/j.cels.2025.101201
[^mason2021]: Mason et al. (2021) "Optimization of therapeutic antibodies by predicting antigen specificity from antibody sequence via deep learning." *Nature Biomedical Engineering*. https://doi.org/10.1038/s41551-021-00699-9