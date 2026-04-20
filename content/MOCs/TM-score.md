---
title: TM-score
tags:
  - tm-score
  - structure-prediction/metrics
created: "2024-06-26T13:44:46"
modified: "2026-04-20T10:13:23"
---
#### Summary
**TM-score** is an alignment-dependent protein structure similarity term introduced by [^zhang2004] that is widely used for assessing [[Structure prediction|protein structure prediction]] methods. It is defined as:

$$TM\text{-}score = max \left[\frac{1}{L_{target}} \sum_{i}^{L_{common}} \left(\frac{1}{1+ \left( \frac{d_{i}}{d_{0} \left( L_{target} \right)} \right)^{2}} \right) \right]$$

$L_{target}$: length of the amino acid sequence of the target protein
$L_{common}$: number of residues in both the target and query proteins
$d$: Distance between pairs of residues
$d_{0}(L_{target}) = 1.24*\sqrt[3]{L_{target}-15}-1.8$: Distance scaling factor

[^zhang2004]: Zhang & Skolnick (2004) "Scoring function for automated assessment of protein structure template quality." *Proteins: Structure, Function, and Bioinformatics*. https://doi.org/10.1002/prot.20264

<!-- generated -->

## General

- [[AlphaFold3 ipTM can distinguish between antibody binders and nonbinders]]
- [[Confidence metrics for diffusion-based structure prediction methods can be improved with minimal changes to conditioning representations]]
- [[Confidence metrics from structure prediction correlate with accuracy even in the absence of coevolutionary data]]
- [[Diffusion-based structure prediction can sometimes model conformational ensembles]]
- [[Heavy and light chains of de novo designed antibodies with the same framework and binding mode can be exchanged]]
- [[Including structure prediction confidence while training inverse folding improves sequence diversity but not sequence recovery]]
- [[Inverse folding sequence perplexities correlate with Rosetta energies, forward folding TM-scores, and sequence recovery]]
- [[Natural sequences have higher pTM but lower pLDDT than de novo sequences]]
- [[PLM-based sequence searches outperform sequence- and matches structure-based search methods]]
- [[Protein backbones designed using diffusion, but not sequence-based models, have fewer beta sheets]]
- [[Protein property prediction using PLMs does not benefit from scale except when predicting inferring features of either structural or sparsely populated sequence families]]
- [[Protein structure prediction and design confidence metrics do not correlate with binding affinity]]
- [[Reinforcement learning outperforms fine-tuning in property-guided inverse folding]]
- [[Sequence perplexity and TM-score are negatively correlated when predicting structure using protein language models]]
- [[Structure prediction from conformational samplers tends to be worse than those from vanilla structure prediction methods]]
- [[Structure prediction metrics can be used to predict oligomer stoichiometry]]
- [[Structure prediction uncertainty metrics as energy functions]]
- [[Template CDR retrieval using embeddings]]
- [[Unfreezing PLM during structure training improves prediction quality]]
- [[pTM is less lenient than pLDDT toward structural novelty when predicting alternate conformations]]
