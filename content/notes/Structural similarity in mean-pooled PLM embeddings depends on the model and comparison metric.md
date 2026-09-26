---
aliases:
  - "Distance between averaged PLM embeddings does not correlate with structural difference"
  - "notes/Distance between averaged PLM embeddings does not correlate with structural difference"
tags:
  - model-analysis/representation-geometry
  - prediction/structure
created: "2024-11-14T03:05:00"
modified: "2026-09-25"
---

#### Summary

**Mean-pooled [[notes/Protein language models|PLM]] embeddings can capture structural similarity, but the relationship depends on the representation, comparison metric, and benchmark** [@pantolini2022; @danwada2026]. The earlier negative distance-correlation result does not establish that all pooled PLM representations lack structural information; structural homology can be detectable even when sequence similarity is low [@kilinc2023; @rives2021].

#### Dependence on representation and benchmark

Pantolini and colleagues reported that distances between averaged embeddings did not track structural differences in their evaluated setting [@pantolini2022]. The original figure below records that result. It should be interpreted within that study rather than generalized to every representation or similarity measure.

RemoteProtBench evaluated 20,445 low-identity PISCES protein pairs (no more than 30% sequence identity), comparing five similarity measures applied to four mean-pooled PLM representations against TM-align structural similarity [@danwada2026]. **Cosine similarity had the highest Spearman correlation for every tested model in this specific study.**

The table reports Spearman correlation with TM-min, reproduced numerically from the [authors’ results table](https://github.com/sutanubh1/RemoteProtBench/blob/main/results/spearman/table3_plms_x_metrics_x_tmmin_rho.csv), rounded to three decimal places. Bold identifies the highest value in each row.

| Model | Cosine | Euclidean similarity | RBF similarity | Manhattan similarity | Dot product |
| --- | ---: | ---: | ---: | ---: | ---: |
| ESM-1b | **0.483** | 0.475 | 0.475 | 0.470 | 0.333 |
| ESM-2 | **0.623** | 0.166 | 0.617 | 0.616 | 0.044 |
| ProstT5 | **0.676** | 0.653 | 0.653 | 0.648 | 0.491 |
| ProtT5 | **0.557** | 0.491 | 0.491 | 0.492 | 0.457 |

These positive correlations qualify the older broad negative claim without showing that its original experiment was wrong. They also do not establish cosine as the best method for every homology-detection task: metric selection within fixed embeddings, pairwise structural correlation, and retrieval performance are different evaluations. See [[PLM searches can improve remote-homology detection beyond profile HMMs]] and [[PLM-based sequence searches outperform sequence- and matches structure-based search methods]] for related retrieval evidence.

#### Figures
![[Pasted-Graphic-6.png]]

*Figure 3 from [@pantolini2022]; AD=average distance*

#### See also
* [[Distance between PLM representations of two proteins correlates with functional dissimilarity]]
* [[PLM embeddings contain enough information to align proteins without fine-tuning]]
* [[Protein language model embeddings are more predictive of homology than catalytic efficiency]]
