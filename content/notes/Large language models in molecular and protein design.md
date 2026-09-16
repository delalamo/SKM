---
title: Large language models in molecular and protein design
aliases:
  - LLM-guided molecular design
  - LLM design MOC
tags:
  - design/sequence-generation
  - inference/sampling-and-search
  - evidence/design-validation
created: "2026-09-16"
modified: "2026-09-16T12:00:34"
---

## Overview

**General-purpose language models can contribute to molecular design by ranking variants, proposing sequences, interpreting computational feedback, and coordinating specialist tools.** These roles make different demands on the model and have different kinds of experimental support.

This map currently emphasizes proteins and antibodies, including proteins that bind small molecules. General-purpose text LLMs are distinct from [[Protein language models|protein language models]] such as [[ESM]] and [[ProGen]], which learn directly from protein sequences. Text-conditioned specialist generators form another related approach: [[Text-to-structure protein design models outperform text-to-sequence models]].

## Evidence by role

| LLM role | Main note | Evidence |
| --- | --- | --- |
| Rank existing variants | [[General-purpose language models can rank protein variants without specialist tools|PG-LLM]] | Retrospective ranking against measured variant effects |
| Propose complete sequences | [[General-purpose language models can propose ligand binders but do not reliably satisfy design constraints|Ligand-binding protein design with LLMs]] | Binding hits after structure prediction, human filtering, and experimental testing |
| Propose mutations and interpret feedback | [[LLM-proposed antibody mutations can yield binders when guided by structural feedback|OpenDDE-Harness]] | Iterative computational search followed by prospective binding assays |
| Direct a design campaign | [[LLM agents can autonomously coordinate protein design campaigns that yield experimental binders|Autonomous binder design with Claude]] | Target research, tool coordination, and candidate selection followed by external wet-lab validation |

## Variant evaluation

[[General-purpose language models can rank protein variants without specialist tools|PG-LLM]] demonstrates useful [[Variant effect prediction|variant-ranking]] ability from sequences and assay descriptions alone. The strongest tested LLMs outperform many sequence-only predictors, while the leading specialist remains better on the main benchmark [@arora2026pgllm].

This supports a role in prioritization and interpretation. It does not establish prospective design hit rates or accurate ranking among only the highest-fitness candidates. See [[Aggregate benchmark correlations can mask weak within-category performance]] and [[Language models cannot extrapolate to functional novelty or ultra-high-fitness variants]]; the latter concerns protein language models and should not automatically be generalized to text LLMs.

## Sequence proposals and structural feedback

[[General-purpose language models can propose ligand binders but do not reliably satisfy design constraints|The ligand-design study]] shows that direct sequence proposals can produce active proteins, while also exposing failures to satisfy requested topology, binding-site, and oligomerization constraints [@kim2026llmdesign].

[[LLM-proposed antibody mutations can yield binders when guided by structural feedback|OpenDDE-Harness]] places an external evaluator, or *oracle*, in the loop: the LLM proposes edits, OpenDDE predicts the complex, and the resulting evidence informs selection and subsequent proposals. The complete pipeline yielded experimentally detected binders [@openddeharness2026]. Here, “oracle” means a computational scoring tool; its confidence scores are not binding measurements.

Related: [[Search algorithms are more important than language model choice for model-guided protein engineering and design]]; [[Protein structure prediction and design confidence metrics do not correlate with binding affinity]].

## Autonomous campaign management

[[LLM agents can autonomously coordinate protein design campaigns that yield experimental binders|The Anthropic report]] extends the role of the LLM to researching targets, selecting regions to model, choosing and combining tools, managing compute, and ranking designs. An expert-written protocol supplied the operating framework; the computational campaigns then proceeded autonomously and produced experimentally validated binders [@claudescience2026].

The report's separate filtering result is already covered in [[Ensembling structure prediction methods for filtering improves recovery]]. Keeping these findings linked distinguishes the agent's coordination capability from the predictive value of its scoring tools.

## Interpreting success

- **Ranking measured variants** tests prioritization; **prospective binding assays** test whether new designs work.
- Computational feedback can guide a search without being an accurate measurement of affinity: [[Accurate fitness landscapes are unnecessary for productively engineering enzymes or proteins]].
- Autonomous computational design and an autonomous laboratory are different levels of automation. Human target selection, protocol design, synthesis orders, and experimental interpretation remain part of the Anthropic study.
- These studies evaluate different tasks and selection procedures. Their hit rates do not constitute a controlled comparison of direct LLM design, oracle-guided mutation, and agent-managed campaigns.
