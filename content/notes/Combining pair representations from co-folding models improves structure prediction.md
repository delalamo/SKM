---
tags:
  - prediction/complexes
  - prediction/ligand-docking
  - inference/ensembling
created: "2026-09-25"
modified: "2026-09-25"
---

#### Summary

**Combining complementary pair representations from independently trained co-folding models can improve structure prediction** [@jang2026]. SoupFold improves protein–protein and protein–ligand predictions on its evaluated FoldBench tasks, including examples where the individual models fail.

#### Details

Learned mappings transfer teacher pair representations into a base model's representation space. The mapped features and base features are averaged before the base diffusion module generates coordinates. The co-folding models remain frozen, but the transfer networks are fitted; this is not parameter-free averaging.

This exploits complementarity before generation, unlike [[Ensembling structure prediction methods for filtering improves recovery|combining output scores to filter completed predictions]]. It also differs from [[notes/Model merging|weight merging]] and from [[Conformational sampling by AlphaFold3-generation methods can be achieved by scaling the pair representation|scaling one model's pair representation to change sampling]]. Improvement on these benchmarks does not establish universal benefit from every teacher or transfer map.

#### See also

- [[AF3-generation methods incorporate MSA information exclusively into the pair representation]]
- [[Different AlphaFold3 clones have differently calibrated confidence heads]]
