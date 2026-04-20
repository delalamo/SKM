---
tags:
  - protein-language-models/representations
created: "2026-01-22T11:03:49"
modified: "2026-04-20T08:32:20"
---

#### Summary

**Sequences with lower [[Sequence perplexity|log-likelihood]] values yield poor zero-shot [[Variant effect prediction|variant effect prediction values]] using [[Protein language models|protein language models]]** [^gordon2024][^wells2025]. This can be mitigated by fine-tuning [^gordon2024]. In contrast, sequences with high log-likelihoods yield poorer predictions when using a fine-tuned model (i.e., the opposite result). However, [[Correlation between sequence log-likelihood and variant effect prediction performance breaks down as PLMs get larger|this correlation breaks down as PLMs get larger]].

#### Figures

![[Pasted-Graphic-4-3.png]]
![[Pasted-image-20241004101202.png]]
*Figures from [^gordon2024]*

![[(D).png]]
*Ref [^wells2025]*

#### See also

* [[PLMs are biased by uneven distribution of sequence data in datasets such as UniRef and UniProt]]
* [[PLMs downweigh probability of sequences with multiple mutations]]

[^gordon2024]: Gordon et al. (2024) "Protein Language Model Fitness Is a Matter of Preference." https://doi.org/10.1101/2024.10.03.616542
[^wells2025]: Wells et al. (2025) "ProFam: Open-Source Protein Family Language Modelling for Fitness Prediction and Design." https://doi.org/10.64898/2025.12.19.695431
