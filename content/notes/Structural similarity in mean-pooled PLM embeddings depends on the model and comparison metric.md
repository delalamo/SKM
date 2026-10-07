---
aliases:
  - "Distance between averaged PLM embeddings does not correlate with structural difference"
  - "notes/Distance between averaged PLM embeddings does not correlate with structural difference"
tags:
  - model-analysis/representation-geometry
  - prediction/structure
created: "2024-11-14T03:05:00"
modified: "2026-10-07T09:14:27"
---

#### Summary

**Mean-pooled [[notes/Protein language models|PLM]] embeddings can capture structural similarity, but the relationship depends on the representation, comparison metric, and benchmark** [@pantolini2022; @danwada2026]. This does not mean that distance between embeddings correlates with magnitude of structural differences [@kilinc2023; @rives2021; @pantolini2022].

#### Details
A comparison of metrics shows that cosine distance is more informative for these kinds of detection tasks (see below).

#### Figures
| Model | Cosine | Euclidean similarity | RBF similarity | Manhattan similarity | Dot product |
| --- | ---: | ---: | ---: | ---: | ---: |
| ESM-1b | **0.483** | 0.475 | 0.475 | 0.470 | 0.333 |
| ESM-2 | **0.623** | 0.166 | 0.617 | 0.616 | 0.044 |
| ProstT5 | **0.676** | 0.653 | 0.653 | 0.648 | 0.491 |
| ProtT5 | **0.557** | 0.491 | 0.491 | 0.492 | 0.457 |

![[Pasted-Graphic-6.png]]

*Figure 3 from [@pantolini2022]; AD=average distance*

#### See also
* [[Distance between PLM representations of two proteins correlates with functional dissimilarity]]
* [[PLM embeddings contain enough information to align proteins without fine-tuning]]
* [[Protein language model embeddings are more predictive of homology than catalytic efficiency]]
