---
tags:
  - protein-folding/misc
created: "2026-01-22T11:23:24"
modified: "2026-04-05T23:36:09"
---

#### Summary

**Adding structural adaptor layers to [[Protein language models|protein language models]] leads to improvements in [[Stability and thermostability#Prediction|thermostability prediction]] compared to using [[Inverse folding|structure-based neural networks]] alone** [^li2025]. This was achieved by adding a [[Attention (machine learning)|cross-attention]] layer with [[ProteinMPNN]] embeddings to each layer of [[ESM|ESM2-650M]] and fine-tuning on the mega-scale thermostability dataset[^megascale].

#### Figures

![](/assets/Pasted-image-20250220082437.png)

![](/assets/Pasted-image-20250220082509.png)

*Figure from [^li2025]*

#### See also

- [[Language models can be infused with structure via low-rank adapter layers]]

[^li2025]: Li & Luo (2025) "Generalizable and scalable protein stability prediction with rewired protein generative models." https://doi.org/10.1101/2025.02.13.638154
[^megascale]: Tsuboyama et al. (2023) "Mega-scale experimental analysis of protein folding stability in biology and design." *Nature*. https://doi.org/10.1038/s41586-023-06328-6
