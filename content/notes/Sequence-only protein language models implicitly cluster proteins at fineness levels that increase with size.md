---
tags:
  - protein-folding/misc
created: "2026-03-26T21:47:41"
modified: "2026-04-05T23:14:54"
---

#### Summary

**Sequence-only [[Protein language models|protein language models]] implicitly cluster protein sequences at fineness granularities that increase with size** (Zhang et al 2025[^zhang2025]). For example, [[ESM]]-15B implicitly learns about sequence constraints from very similar proteins, whereas the 650M model learns from a broader pool of sequences. This was determined by observing the extent to which these models learn homo-oligomeric contacts and comparing their performance to that of [[MSA-Pairformer]].

#### Figures

![](/assets/Pasted-image-20251211092215.png)
*Figure from Zhang et al 2025[^zhang2025]*

#### See also

* [[Protein property prediction using PLMs does not benefit from scale except when predicting inferring features of either structural or sparsely populated sequence families]]
* [[Larger PLMs generate more novel sequences from more sparsely populated protein families]]

[^zhang2025]: Zhang et al. (2025) "Hit or Miss: Understanding Emergence and Absence of Homo-oligomeric Contacts in Protein Language Models." https://doi.org/10.1101/2025.11.16.688745
