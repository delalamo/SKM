---
tags:
  - prediction/binding
  - evidence/generalization
created: 2025-12-11T09:01:07
modified: "2026-08-25T10:16:02"
---

#### Summary

**The [[notes/AlphaFold3|Boltz-2]] affinity module for small molecule-protein affinity prediction cannot be effectively repurposed for [[notes/Protein-protein interactions|protein-protein interaction]] affinity prediction** [@king2025]. They found that it underperformed fine-tuning from [[ESM]] embeddings. However, appending Boltz features to ESM features improves affinity prediction. This limitation is specific to repurposing the native affinity module: [[Boltz-2 intermediate representations can predict protein-protein binding affinity|PreFold-dG]] uses distance-weighted intermediate representations in a separate predictor and reports strong $\Delta G$ and $\Delta\Delta G$ performance [@park2026prefold].

#### See also

- [[All-atom structure and affinity predictors partially generalize to point mutants]]
