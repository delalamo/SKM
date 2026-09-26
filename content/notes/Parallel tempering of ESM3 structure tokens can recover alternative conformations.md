---
tags:
  - prediction/ensembles
  - inference/sampling-and-search
  - model-design/multimodal
created: "2026-09-15"
modified: "2026-09-25"
---

#### Summary

**[[Replica-exchange molecular dynamics|Parallel tempering]] applied to [[ESM|ESM3]] [[Protein structure tokenization|structure tokens]] can recover alternative protein conformations without retraining the model** [@wang2026msfold]. MSFold couples exploratory high-temperature token sampling to refinement at lower temperatures.

#### Details

MSFold uses 40 replicas and 500 sampling steps, producing 20,000 decoded conformations. Each step masks and resamples local token blocks and attempts exchanges between neighboring replicas. The temperatures scale model token probabilities; they are not physical temperatures in an atomistic simulation.

Across 312 experimental conformation pairs, the sampled ensemble recovered both states in 161 cases (51.6%), compared with 38.1% for AF Cluster and 37.8% for [[AlphaFold3]] (Figure 1). Success required at least one candidate with [[TM-score]] ≥ 0.75 for each reference state. This measures coverage of known structures, not their equilibrium populations or transition rates; it also uses the best matches in the full ensemble rather than only the highest-ranked predictions.

Sequence log-likelihood conditioned on each sampled structure provides a reference-free ranking score. The paper reports better selection than pTM or pLDDT, but ranking remains separate from generating the alternative state.

#### See also

- [[Structure prediction methods undersample the conformational space they find to be high-confidence]]
- [[Protein structure prediction methods are unable to predict the energetics of a conformational landscape unless explicitly trained for that purpose]]
- [[Sequence perplexity and TM-score are negatively correlated when predicting structure using protein language models]]
