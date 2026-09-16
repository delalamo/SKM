---
aliases:
  - PG-LLM
tags:
  - prediction/variant-effects
  - evidence/generalization
  - evidence/datasets
created: "2026-09-16"
modified: "2026-09-16T12:00:34"
---

#### Summary

**General-purpose language models can make useful [[Variant effect prediction|protein-variant rankings]] from sequences and assay descriptions without specialist tools, although the strongest specialist predictors remain better on the main PG-LLM benchmark** [@arora2026pgllm].

#### Details

PG-LLM evaluates 217 [[ProteinGym]] substitution assays across 186 proteins. Each prompt contains the wild-type sequence, assay context, and 50 full-length variant sequences sampled across the measured fitness range. Models rank them without tools, [[Multiple sequence alignments|MSAs]], or structures. Ninety-five specialist predictors are rescored on the same candidates.

| Model or reference group | Spearman ρ |
| --- | ---: |
| Claude Opus 5 | 0.406 |
| GPT-5.6 Sol | 0.402 |
| [[ESM|ESM2-650M]] | 0.411 |
| Sequence-only predictor median | 0.374 |
| Alignment/structure predictor median | 0.435 |
| VenusREM | 0.523 |

Scores use nested averaging across assays, proteins, and functional categories, then average three candidate draws. Opus 5 exceeds 49 of 95 comparators, including 41 of 46 sequence-only methods. Provider refusals change coverage: Sol leads when evaluated on the assays shared with Opus 5. More reasoning generally helps, with diminishing returns; larger candidate lists impair ranking.

A separate panel contains 59 recent assays from 19 studies. Sol reaches ρ = 0.332, versus 0.202 for ESM2-650M and 0.323 for VespaG. This reduces concerns about training exposure, although only 57 of 59 assays postdate Sol's stated cutoff.

These are rankings of supplied substitution variants. The benchmark does not establish prospective wet-lab design success, clinical pathogenicity prediction, or performance across complete fitness landscapes.

#### Figures

![[pg-llm-variant-ranking.png]]

*Figure 1 from the August 19, 2026 version of [@arora2026pgllm]. Bars show the LLMs; marks below show specialist predictors on the same candidate sets. Scores should not be substituted for full-assay ProteinGym scores.*

#### See also

- [[Large language models in molecular and protein design]]
- [[General-purpose language models can propose ligand binders but do not reliably satisfy design constraints]]
- [[Aggregate benchmark correlations can mask weak within-category performance]]
- [[Protein language models are better zero-shot predictors for ranking closely related sequences than distantly related sequences]]

#### Sources

- [Paper](https://doi.org/10.64898/2026.07.27.741045), August 19, 2026 revision.
- [Authors' benchmark overview and results](https://www.proteingymllm.com/).
