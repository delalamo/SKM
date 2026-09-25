---
tags:
  - prediction/complexes
  - training/pretraining-and-scaling
  - evidence/datasets
created: "2026-06-23"
modified: "2026-09-25"
---

#### Summary

**[[tags/antibodies|Antibody]]-antigen complex prediction appears to scale with training data and compute.** Co-folding performance appears to follow a scaling law dependent on both training data and compute [@jing2026].

#### Expanded experimental and distilled training data

TorchFold's successive training stages reached 34.0%, 65.9%, and 70.1% ranked FoldBench antibody–antigen success (section 2.1) [@torchfold2026]. Confidence-filtered (ipTM ≥ 0.8) sequence-pair predictions added predicted epitope coverage and interface geometries, but these are predicted labels rather than experimentally validated new interactions.

**The comparison is confounded by expanded experimental training data alongside the distillation examples.** The from-scratch PDB cutoff was 30 September 2021, whereas antibody–antigen fine-tuning used SAbDab through 1 January 2025. Interface-loss weighting and the stage-2 noise schedule also changed. Without a matched-data, matched-training ablation, the improvement cannot be assigned to distillation alone (Appendix A.3 and Table 2) [@torchfold2026].

#### Figures

![[antibody-antigen-complex-prediction-scaling-law.jpg]]

*Ref [@jing2026]*

#### See also

* [[Antibody-antigen modeling by diffusion-based structure prediction is data-limited]]
* [[Scaling hypothesis]]
* [[Correct antibody-antigen prediction in AF3 and related models is partially determined by training set similarity]]
