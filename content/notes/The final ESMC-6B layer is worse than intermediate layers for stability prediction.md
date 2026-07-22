---
tags:
  - protein-language-models/representations
  - thermostability/prediction
created: "2026-07-19"
modified: "2026-07-22T09:15:30"
---

#### Summary

**Intermediate ESMC-6B representations are more predictive of folding stability than the model's final layer.** This was measured by fitting linear probes to [[Sparse autoencoder|sparse-autoencoder]] features extracted across layers. Performance rises through much of the network and then drops at the output layer, consistent with final representations becoming specialized for the language-modeling objective [@candido2026].

#### See also

- [[Protein language models learn structure-level features, including disorder, in later layers]]
- [[Sparse autoencoders recover protein-family and gene-ontology features from PLM representations]]
- [[PLM pseudoperplexity stratifies stability-prediction accuracy]]
