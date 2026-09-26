---
tags:
  - design/sequence-generation
  - evidence/generalization
created: "2026-09-25"
modified: "2026-09-25"
---

#### Overview

General-purpose text language models have been tested on molecular and protein tasks ranging from interpretation to sequence proposals. Their capabilities should be assessed by task and endpoint. They differ from [[Protein language models|protein language models]] trained directly on biological sequences.

#### Evidence by task

| Task | Finding | What was evaluated |
| --- | --- | --- |
| Epitope identification | [[General-purpose language models underperform specialist models on tested epitope identification tasks|Specialist methods outperformed general-purpose LLMs on the matched benchmark tasks]] [@wang2026_G] | Prediction on existing labeled examples; the comparison does not establish prospective binder-design performance. |
| Ligand-binder design | [[General-purpose language models can propose ligand binders but do not reliably satisfy design constraints|LLMs proposed some experimentally active ligand binders, with uneven constraint satisfaction]] [@kim2026llmdesign] | Computational assessment and a small set of prospective experiments; the study does not isolate a general experimental advantage from adding specialist tools. |

These findings address different roles. Weak epitope-identification results need not rule out useful sequence proposals, while a few experimental hits do not establish reliable performance across molecular design tasks.
