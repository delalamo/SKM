---
tags:
  - protein-folding/misc
created: "2024-07-02T05:11:12"
modified: "2026-04-05T23:36:09"
---
#### Summary
**Fine-tuning PLMs can be detrimental to downstream tasks.** [^detlefsen2022] say that it "should therefore take place only under rigorous cross validation." [^heinzinger2023] found evidence of [[Catastrophic forgetting]] during fine-tuning of their [[Protein language models|PLM]] on [[Foldseek]] structural descriptors. [^kenlay2024] avoided this by maintaining the pretraining objective and data when fine-tuning; in their case keeping unpaired antibody sequences while fine-tuning on paired sequences.

#### Details
Beyond protein ML models, RLHF was also found to worsen performance of the large language model [[GPT]]-4 [^chen2023].

#### Figures
![](/assets/Fine-tuning-benchmark.png)
*Figure from [^detlefsen2022]*

[^detlefsen2022]: Detlefsen et al. (2022) "Learning meaningful representations of protein sequences." *Nature Communications*. https://doi.org/10.1038/s41467-022-29443-w
[^heinzinger2023]: Heinzinger et al. (2023) "Bilingual Language Model for Protein Sequence and Structure." https://doi.org/10.1101/2023.07.23.550085
[^kenlay2024]: Kenlay et al. (2024) "Large scale paired antibody language models." https://doi.org/10.48550/ARXIV.2403.17889
[^chen2023]: Chen et al. (2023) "How is ChatGPT's behavior changing over time?." https://doi.org/10.48550/arXiv.2307.09009
