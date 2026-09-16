---
aliases:
  - Autonomous de novo protein binder design with Claude
tags:
  - design/binders
  - inference/sampling-and-search
  - evidence/design-validation
created: "2026-09-16"
modified: "2026-09-16T12:00:34"
---

#### Summary

**LLM agents can autonomously coordinate target research, specialist design tools, computational optimization, and candidate selection to produce experimentally validated protein binders.** Anthropic's Claude campaigns demonstrate this role across multiple targets under an expert-written protocol [@claudescience2026].

#### Campaign management

Claude Opus 4.8 and Mythos Preview researched targets, selected modeling regions and epitopes, installed tools, allocated compute, and ranked candidates during 24–48-hour campaigns. Humans supplied targets, an approximately 16,000-word protocol, resources, and subsequent experimental ordering and interpretation.

The protocol required exploration of seven designated structure-generation methods. Within those constraints, Claude assembled different pipelines across targets and campaigns, combining backbone generators with sequence-design methods such as [[ProteinMPNN|SolubleMPNN]] and iterative optimization. This is autonomy within a supplied research framework.

#### Experimental support

The report records **354 binders among 1,320 designs with interpretable target data (26.8%), covering 14 of 15 targets**. One additional target was excluded because aggregation prevented interpretation. Validation was performed by Adaptyv Bio and Twist Bioscience.

Among top-ranked designs in the three broad campaigns, 49% bound. The overall totals include 30 supplementary TNFα designs selected by a human from Claude's scored pool; those are excluded from ranking analyses.

The computational campaigns preceded wet-lab testing. Binding was validated, but biological activity and experimental structures were not. There was no matched human-expert campaign using the same tools and budget.

#### Figures

![[claude-protein-design-tool-orchestration.png]]

*Figure 3 from [@claudescience2026]: combinations of structure generation, sequence design, and optimization, with experimental outcomes. The figure uses 1,315 tested designs. Method-specific hit rates describe the selected campaigns; target and method choices were not randomized.*

#### See also

- [[Large language models in molecular and protein design]]
- [[Ensembling structure prediction methods for filtering improves recovery]] — the separate result about the campaign's scoring tools.
- [[LLM-proposed antibody mutations can yield binders when guided by structural feedback]]
- [[General-purpose language models can propose ligand binders but do not reliably satisfy design constraints]]
- [[Effectiveness of filtering metrics for de novo minibinder design vary by target]]

#### Sources

- [Autonomous de novo protein binder design with Claude](https://www-cdn.anthropic.com/30bf50e22a01388bb29bf077ee3f244531594b7a.pdf), August 18, 2026 technical report.
- [Anthropic overview](https://www.anthropic.com/research/Claude-accelerates-protein-design).
- [Released prompts, design provenance, and experimental data](https://huggingface.co/datasets/Anthropic/claude-protein-binder-design).
