---
tags:
  - protein-language-models/representations
created: "2026-01-22T11:03:49"
modified: "2026-04-21T05:01:15"
---

#### Summary

**Sequences with lower [[Sequence perplexity|log-likelihood]] values yield poor zero-shot [[Variant effect prediction|variant effect prediction values]] using [[Protein language models|protein language models]]** [@gordon2024; @wells2025profam]. This can be mitigated by fine-tuning [@gordon2024]. In contrast, sequences with high log-likelihoods yield poorer predictions when using a fine-tuned model (i.e., the opposite result). However, [[Correlation between sequence log-likelihood and variant effect prediction performance breaks down as PLMs get larger|this correlation breaks down as PLMs get larger]].

#### Figures

![[Pasted-Graphic-4-3.png]]
![[Pasted-image-20241004101202.png]]
*Figures from [@gordon2024]*

![[(D).png]]
*Ref [@wells2025profam]*

#### See also

* [[PLMs are biased by uneven distribution of sequence data in datasets such as UniRef and UniProt]]
* [[PLMs downweigh probability of sequences with multiple mutations]]
