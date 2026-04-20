---
tags:
  - protein-language-models/training
created: "2024-07-02T05:11:12"
modified: "2026-04-20T08:32:20"
---
#### Summary
**Fine-tuning PLMs can be detrimental to downstream tasks.** [^detlefsen2022] say that it "should therefore take place only under rigorous cross validation." [^heinzinger2023] found evidence of [[Catastrophic forgetting]] during fine-tuning of their [[Protein language models|PLM]] on [[Foldseek]] structural descriptors. [^kenlay2024] avoided this by maintaining the pretraining objective and data when fine-tuning; in their case keeping unpaired antibody sequences while fine-tuning on paired sequences.

#### Details
Beyond protein ML models, RLHF was also found to worsen performance of the large language model [[GPT]]-4 [^chen2023].

#### Figures
![[Fine-tuning-benchmark.png]]
*Ref [^detlefsen2022]*

[^detlefsen2022]: Detlefsen et al. (2022) "Learning meaningful representations of protein sequences." *Nature Communications*. https://doi.org/10.1038/s41467-022-29443-w
[^heinzinger2023]: Heinzinger et al. (2024) "Bilingual language model for protein sequence and structure." NAR Genomics and Bioinformatics. https://doi.org/10.1093/nargab/lqae150
[^kenlay2024]: Kenlay et al. (2024) "Large scale paired antibody language models." PLoS Comput. Biol.. https://doi.org/10.1371/JOURNAL.PCBI.1012646
[^chen2023]: Chen et al. (2024) "How Is ChatGPT’s Behavior Changing Over Time?." Harvard Data Science Review. https://doi.org/10.1162/99608f92.5317da47
