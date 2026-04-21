---
tags:
  - protein-language-models/training
created: "2026-03-26T21:47:41"
modified: "2026-04-21T05:01:15"
---

#### Summary

**Sequence-only [[Protein language models|protein language models]] implicitly cluster protein sequences at fineness granularities that increase with size** [@zhang2025]. For example, [[ESM]]-15B implicitly learns about sequence constraints from very similar proteins, whereas the 650M model learns from a broader pool of sequences. This was determined by observing the extent to which these models learn homo-oligomeric contacts and comparing their performance to that of [[MSA-Pairformer]].

#### Figures

![[Pasted-image-20251211092215.png]]
*Ref [@zhang2025]*

#### See also

* [[Protein property prediction using PLMs does not benefit from scale except when predicting inferring features of either structural or sparsely populated sequence families]]
* [[Larger PLMs generate more novel sequences from more sparsely populated protein families]]
