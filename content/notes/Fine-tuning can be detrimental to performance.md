---
tags:
  - protein-language-models/training
created: "2024-07-02T05:11:12"
modified: "2026-04-21T07:03:26"
---
#### Summary
**Fine-tuning PLMs can be detrimental to downstream tasks.** [@detlefsen2022] say that it "should therefore take place only under rigorous cross validation." [@heinzinger2023] found evidence of [[Catastrophic forgetting]] during fine-tuning of their [[tags/protein-language-models|PLM]] on [[Foldseek]] structural descriptors. [@kenlay2024large] avoided this by maintaining the pretraining objective and data when fine-tuning; in their case keeping unpaired antibody sequences while fine-tuning on paired sequences.

#### Details
Beyond protein ML models, RLHF was also found to worsen performance of the large language model [[GPT]]-4 [@chen2024how].

#### Figures
![[Fine-tuning-benchmark.png]]
*Ref [@detlefsen2022]*
