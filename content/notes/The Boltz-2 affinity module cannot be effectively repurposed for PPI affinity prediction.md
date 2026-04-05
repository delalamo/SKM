---
tags:
  - protein-folding/misc
---

#### Summary

**The [[Boltz|Boltz-2]] affinity module for small molecule-protein affinity prediction cannot be effectively repurposed for [[Protein-protein interactions|protein-protein interaction]] affinity prediction** (King et al 2025[^king2025]). They found that it underperformed fine-tuning from [[ESM]] embeddings. However, appending Boltz features to ESM features improves affinity prediction.

[^king2025]: King et al. (2025) "On fine-tuning Boltz-2 for protein-protein affinity prediction." https://doi.org/10.48550/ARXIV.2512.06592
