---
tags:
  - protein-language-models/training
  - plddt
title: Unconditional EvoDiff design metrics do not consistently improve with model scale
created: "2026-01-22T12:38:44"
modified: "2026-08-19T16:32:04"
---

#### Summary

**For unconditional EvoDiff sequence generation, scaling from 38M to 650M parameters did not consistently improve [[plddt|pLDDT]] or [[Sequence perplexity|self-consistency perplexity]] of designs** [@alamdari2023]. This is metric- and task-specific: larger [[protein-language-models|protein language models]] can be more steerable under activation steering even when raw generation metrics plateau [@huang2025].

#### Figures

![[scPerplexity.png]]

*Ref [@alamdari2023]*

#### See also

* [[Protein property prediction using PLMs does not benefit from scale except when predicting inferring features of either structural or sparsely populated sequence families]]
