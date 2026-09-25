---
tags:
  - antibodies/recognition
  - evidence/generalization
created: "2026-09-25"
modified: "2026-09-25"
---

#### Summary

**General-purpose text language models underperform matched specialist models on the tested epitope-identification tasks in EpiBench** [@wang2026_G]. This concerns sequence-based localization and comparison of epitopes, rather than prospective [[notes/De novo antibody design|antibody design]].

#### Details

EpiBench evaluates nine LLMs on 1,609 examples across five tasks. Matched specialist baselines outperform the tested LLMs on targetable-region discovery, antibody-conditioned epitope identification, and epitope binning (tasks 1–3). Functional epitope assessment and escape assessment (tasks 4–5) have no directly matched specialist baseline; the comparison does not establish specialist superiority on all five tasks.

The closed-book setting tests what the models infer from supplied sequences. It does not evaluate a workflow that retrieves evidence or invokes specialist prediction tools. Partial epitope-related signal therefore coexists with limitations in antibody-specific grounding and residue localization.

#### See also

- [[notes/Antibody structure prediction|Antibody structure prediction]]
- [[Correct antibody-antigen prediction in AF3 and related models is partially determined by training set similarity]]
