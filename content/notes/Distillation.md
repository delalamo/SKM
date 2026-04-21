---
title: Distillation
tags:
  - citation-fix
created: 2026-04-10T14:30:55
modified: "2026-04-21T05:01:15"
---

**Distillation** of machine learning models refers to the generation of additional training data using either another neural network (cross-distillation, or student-teacher training) or an earlier version of a neural network (self distillation). This can be to expose more training data ([[AlphaFold2]], [[AlphaMissense]], [[ESM]]3) or to shrink the model (DistillProtBERT; [@geffen2022]) for better generalization. It has also been used to turn [[Protein language models|PLMs]] into [[Variant effect prediction]] models [@marquet2024], by adding a top-off layer that is trained using predictions from larger specialized models. Finally, cross-distillation was used when training AlphaFold3 for prediction of disordered regions (see [[AlphaFold3 uses cross-distillation from AlphaFold2 to avoid hallucinating secondary structure in low-pLDDT regions]]; [@abramson2024]).
