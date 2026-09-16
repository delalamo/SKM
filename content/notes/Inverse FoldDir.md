---
title: Inverse FoldDir
tags:
  - design/inverse-folding
  - model-design/generative-models
  - evidence/generalization
created: "2026-09-15"
modified: "2026-09-16T12:00:34"
---

**Inverse FoldDir** combines a [[Geometric Vector Perceptrons|GVP]] structural encoder with Dirichlet [[Flow matching]] to design sequences on fixed protein backbones. It supports full-sequence design, fixed-residue inpainting, and soft amino-acid preferences [@tartici2026].

#### Details

The released model uses CATH 4.2 training chains plus 2,824,736 filtered AlphaFold Database structures. [[ESM-IF]] instead used approximately 12 million predicted structures [@hsu2022]. Thus the methods use different training corpora; Inverse FoldDir does not simply use a larger number of predicted structures. Baselines were evaluated as released, without retraining on a common dataset.

On 1,120 CATH test proteins, [[ESMFold]] refolding gave the following results (Tables 1 and 3; TM-scores converted from the paper's 0-100 scale):

| Model | TM-score ↑ | Cα RMSD, Å ↓ |
| --- | ---: | ---: |
| Inverse FoldDir | 0.845 ± 0.002 | 1.76 ± 0.01 |
| ESM-IF1 | 0.833 ± 0.002 | 1.86 ± 0.01 |
| Inverse FoldDir without predicted training structures | 0.810 ± 0.002 | 2.02 ± 0.01 |

Uncertainties are standard deviations of three generation-replicate means. These results support refolding consistency, not an isolated architectural advantage or guaranteed experimental function. The [released model's data audit](https://huggingface.co/AlpTartici/inversefolddir#training-data) also acknowledges residual structural overlap for five test chains after filtering at cluster-representative level.

#### See also

- [[Inverse folding by flow matching resolves residue identities at different times]]
- [[Protein models designed using inverse folding can be used to supplement training DBs for PLMs and structure prediction models]]
- [[Sequence recovery in inverse folding models is not correlated with self-consistency of generated designs]]
