---
tags: [protein-folding/misc]
---

#### Summary
**Proteins designed *de novo* from language models interpolate the design space of their training data, mirroring how naturally occurring proteins also borrow heavily form each other.** Brian Naughton in a series of twitter posts noted that esmGFP (generated using (ESM)3) has 58% sequence identity to any naturally occurring GFP, but 74% when considering mixing and matching across protein sequences (https://gistpreview.github.io/?81c106aa6e8519bcc77acdbde939a2fa/ESM3_GFP_alignment.html). Likewise, the [[CRISPR-Cas9|CRISPR]] enzyme [[Design of de novo CRISPR-Cas9 systems|openCRISPR]] (generated using fine-tuned (ProGen2)) from Ruffolo et al 2025[^ruffolo2025] can be recreated to 98% completion using three Streptococcus sequences (https://gistpreview.github.io/?f6684bb2fefa838bfff5082465df2ff0).

#### Figures
![](/assets/Pasted-image-20250803095055.png)
*Figure from Ruffolo et al 2025[^ruffolo2025]*

![](/assets/Pasted-image-20240626064620.png)
*Figure from Brian Naughton's Twitter; red regions have two or more consecutive novel residues; the long loop in the top right is not conserved*

[^ruffolo2025]: Ruffolo et al. (2025) "Design of highly functional genome editors by modelling CRISPR–Cas sequences." *Nature*. https://doi.org/10.1038/s41586-025-09298-z
