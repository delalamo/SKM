---
aliases:
  - OpenDDE-Harness
tags:
  - design/antibodies
  - inference/sampling-and-search
  - evidence/design-validation
created: "2026-09-16"
modified: "2026-09-16T12:00:34"
---

#### Summary

**LLM-proposed antibody sequence changes can yield experimentally detected binders when embedded in an iterative search guided by predicted complex structures.** OpenDDE-Harness couples sequence proposals to OpenDDE structural evaluation, candidate selection, and reflection on previous outcomes [@openddeharness2026].

#### Details

The LLM proposes local substitutions or broader redesigns of [[Complementarity-determining regions|CDRs]] within specified constraints. OpenDDE predicts antibody–antigen complexes and supplies structural confidence and interface evidence. The harness validates proposals, updates a candidate population, and makes successes and failures available to subsequent rounds. This feedback changes the search context without retraining the LLM.

OpenDDE serves as a computational *oracle*: it evaluates proposed sequences rather than generating the CDR edits. Its scores are surrogate evidence, not measured affinity.

#### Experimental support

The report describes **38 binders among 80 synthesized designs (47.5%)**:

| Target and format cohort | Synthesized | Binding hits | Hit rate |
| --- | ---: | ---: | ---: |
| RAGE | 20 | 17 | 85% |
| TfR1 | 20 | 11 | 55% |
| CXCR4 VHH | 20 | 6 | 30% |
| CXCR4 mAb | 20 | 4 | 20% |

Binding was measured by surface plasmon resonance or biolayer interferometry. Denominators include designs that failed to yield sufficient material. Internal developability filters also contributed to experimental selection.

The CXCR4 case connects iterative structural optimization to a binding, SolubleMPNN-refined descendant. Starting and intermediate variants were not measured, so this does not demonstrate improved affinity attributable to the LLM's individual mutations.

The computational comparison favors the complete harness, but direct LLM generation received fewer refolding opportunities and no SolubleMPNN optimization; OpenDDE also served as both search evaluator and final evaluator. Thus, the study validates a working feedback-guided pipeline without isolating the necessity or contribution of the oracle, reflection, or memory.

#### Figures

![[opendde-harness-experimental-binding.png]]

*Figure 3 from [@openddeharness2026]. Sensorgrams and binding counts provide experimental evidence; the displayed complexes are predictions. Sequence-diversity measures depend on CDR length and antibody format.*

#### See also

- [[Large language models in molecular and protein design]]
- [[General-purpose language models can propose ligand binders but do not reliably satisfy design constraints]]
- [[LLM agents can autonomously coordinate protein design campaigns that yield experimental binders]]
- [[Search algorithms are more important than language model choice for model-guided protein engineering and design]]
- [[Protein structure prediction and design confidence metrics do not correlate with binding affinity]]

#### Sources

- [Technical report, September 10, 2026 repository revision](https://github.com/aurekaresearch/OpenDDE-Harness/blob/a0a8d1a07d92ab54947ef4d90ade982a682598d1/docs/assets/OpenDDE_harness_tech_report.pdf), especially Sections 2.1 and 3.1–3.3 and Figure 3.
- [OpenDDE-Harness project](https://github.com/aurekaresearch/OpenDDE-Harness).
