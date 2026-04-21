---
tags:
  - alphafold3
  - protein-protein-interactions
created: 2025-12-11T09:01:07
modified: "2026-04-21T07:03:26"
---

#### Summary

**The [[tags/alphafold3|Boltz-2]] affinity module for small molecule-protein affinity prediction cannot be effectively repurposed for [[tags/protein-protein-interactions|protein-protein interaction]] affinity prediction** [@king2025]. They found that it underperformed fine-tuning from [[ESM]] embeddings. However, appending Boltz features to ESM features improves affinity prediction.
