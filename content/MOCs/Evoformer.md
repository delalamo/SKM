---
title: Evoformer
tags:
  - evoformer
---

The **Evoformer** is a deep learning module introduced and used by [[AlphaFold|AlphaFold2]] that processes [[Multiple sequence alignments]] for protein [[Structure prediction|structure prediction]]. It contains the majority of trainable parameters and is similar to [[MSA Transformer]] (probably independently developed) in that it uses axial attention.

#### Mentions

* **The evoformer partially learns protein dynamics** ([[10.48550__arXiv.2306.05445|Zheng et al 2023]]). Its embeddings can be used without fine-tuning as inputs to a [[Graph neural networks|GNN]]-[[Transformer]] hybrid that modeled protein dynamics (albeit imperfectly).
	![](/assets/Pasted-image-20231201132939.png)
	*Figure from [[10.48550__arXiv.2306.05445|Zheng et al 2023]]*

<!-- generated -->
