---
tags:
  - thermostability/prediction
  - low-rank-adaptation
created: 2026-01-22T11:23:24
modified: "2026-04-21T05:01:15"
---

#### Summary

**Adding structural adaptor layers to [[Protein language models|protein language models]] leads to improvements in [[Stability and thermostability#Prediction|thermostability prediction]] compared to using [[Inverse folding|structure-based neural networks]] alone** [@li2025]. This was achieved by adding a [[Attention (machine learning)|cross-attention]] layer with [[ProteinMPNN]] embeddings to each layer of [[ESM|ESM2-650M]] and fine-tuning on the mega-scale thermostability dataset [@tsuboyama2023].

#### Figures

![[Pasted-image-20250220082437.png]]

![[Pasted-image-20250220082509.png]]

*Ref [@li2025]*

#### See also

- [[Language models can be infused with structure via low-rank adapter layers]]
