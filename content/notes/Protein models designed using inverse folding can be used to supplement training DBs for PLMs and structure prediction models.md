---
tags:
  - protein-language-models/training
  - structure-prediction/training
created: "2025-02-07T00:45:40"
modified: "2026-04-13T11:11:20"
---

## Summary

**Protein models designed by [[Inverse folding|inverse folding]] can be used to augment datasets of natural sequences when training [[Protein language models|protein language models]] and [[Structure prediction|protein folding neural networks]]** [^hayes2025][^wells2025]. This was demonstrated using ProFam1 and [[AlphaFold|AlphaFold2]], with inference on synthetic MSAs outperforming single-sequence predictions. Similar results were also presented with [[ESM]]3, although no ablation data is available to show its impact.

## See also

* [[Distillation]]
* [[Training backbone diffusion models on synthetic data improves designability]]

[^hayes2025]: Hayes et al. (2025) "Simulating 500 million years of evolution with a language model." *Science*. https://doi.org/10.1126/science.ads0018
[^wells2025]: Wells et al. (2025) "ProFam: Open-Source Protein Family Language Modelling for Fitness Prediction and Design." https://doi.org/10.64898/2025.12.19.695431
