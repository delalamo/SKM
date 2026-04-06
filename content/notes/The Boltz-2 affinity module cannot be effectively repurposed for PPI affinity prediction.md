---
tags:
  - protein-folding/misc
created: "2025-12-11T09:01:07"
modified: "2026-04-05T23:36:09"
---

#### Summary

**The [[Boltz|Boltz-2]] affinity module for small molecule-protein affinity prediction cannot be effectively repurposed for [[Protein-protein interactions|protein-protein interaction]] affinity prediction** [^king2025]. They found that it underperformed fine-tuning from [[ESM]] embeddings. However, appending Boltz features to ESM features improves affinity prediction.

[^king2025]: King et al. (2025) "On fine-tuning Boltz-2 for protein-protein affinity prediction." https://doi.org/10.48550/ARXIV.2512.06592
