---
tags: [protein-design/misc]
created: "2026-04-05T17:54:18"
modified: "2026-04-10T14:02:57"
---

---
summary: Smaller PLMs models are more effective at variant effect prediction
tags: 
 - protein-language-models/applications
 - mutations/prediction
 - esm/observations
---
#### Summary
**Protein property prediction using [[Protein language models|PLMs]] does not benefit from [[Scaling hypothesis|scale]] beyond ~650M parameters, except when predicting A) structural features or B) features of sparsely populated protein families such as those from viruses.** This is particularly the case with zero-shot prediction [^tan2023][^nijkamp2023][^notin2023]. Some authors have reported it is also true of fine-tuning [^detlefsen2022][^li2024][^vieira2024], although aligning PLMs using [[Reinforcement learning|reinforcement learning]] using data does seem to restore the trend in some cases [^bhatnagar2025]. The exception of structure when transfer learning was shown by [^li2024], and corroborated by attempts to use (ESM) embeddings as starting points for [[Structure prediction|structure prediction]] ([^lin2023] and [^lee2023]). Related to this, larger PLMs are better at [[Larger PLMs are better at homolog detection|homolog detection]] and [[Larger PLMs are better at thermostability prediction|thermostability prediction]], and do not improve as much as smaller models at fitness prediction when [[Language models can be infused with structure via low-rank adapter layers|infused with structural information via low-rank adaptors]] [^ruffolo2024]. Likewise, the exception for viral proteins was observed by [^gurev2025]. [^zhang2024] surmise that both exceptions are due to large PLMs having a greater capacity to [[PLMs learn family-specific protein contacts from sequence context windows of about 20-40 amino acids|memorize domain-specific contacts]].

#### Details
Larger (ProGen) models were better able to predict fitness of distant sequences ("wide mutational scale"; [^nijkamp2023]). Likewise, engineered [[CRISPR-Cas9|CRISPR]] variants were said to be better predicted with larger models ([^ruffolo2025]; mentioned at PEGS Boston 2024). Augmenting ProGen models with structural information only led to improvements in fitness prediction in smaller models, suggesting that the larger models had already learned most of that information.

This is also true of post-translational modification prediction ([^peng2024]; ESM2-650M vs ESM2-3B).

#### Figures
| Model type | Model name | Spearman | AUC | MCC | NDCG | Recall |
|---|---|---|---|---|---|---|
| Alignment-based | Site-Independent | 0.361 | 0.697 | 0.288 | 0.746 | 0.201 |
| | WaveNet | 0.216 | 0.623 | 0.174 | 0.684 | 0.154 |
| | EVmutation | 0.397 | 0.717 | 0.306 | 0.775 | 0.220 |
| | DeepSequence (ens.) | 0.422 | 0.731 | 0.330 | 0.775 | 0.227 |
| | EVE (ens.) | 0.441 | 0.741 | 0.343 | 0.781 | **0.231** |
| | GEMME | **0.457** | 0.750 | 0.353 | 0.775 | 0.209 |
| Protein language | UniRep | 0.193 | 0.607 | 0.149 | 0.647 | 0.14 |
| | CARP (640M) | 0.373 | 0.704 | 0.289 | 0.749 | 0.210 |
| | RITA XL | 0.373 | 0.708 | 0.294 | 0.750 | 0.194 |
| | ProGen2 XL | 0.392 | 0.718 | 0.307 | 0.766 | 0.200 |
| | ESM-1b ★ | 0.399 | 0.722 | 0.315 | 0.748 | 0.205 |
| | ESM2 (15B) ★ | 0.405 | 0.723 | 0.318 | 0.759 | 0.210 |
| | ESM-1v (ens.) | 0.416 | 0.730 | 0.329 | 0.753 | 0.216 |
| | VESPA | 0.437 | 0.743 | 0.348 | 0.774 | 0.201 |
| Hybrid | UniRep evotuned | 0.347 | 0.693 | 0.274 | 0.737 | 0.181 |
| | MSA Transformer (ens.) | 0.434 | 0.738 | 0.341 | 0.777 | 0.224 |
| | Tranception L | 0.436 | 0.740 | 0.342 | 0.778 | 0.221 |
| | TranceptEVE L | **0.457** | **0.752** | **0.357** | **0.785** | **0.231** |
| Inverse Folding | ProteinMPNN | 0.258 | 0.640 | 0.196 | 0.712 | 0.186 |
| | MIF-ST | 0.401 | 0.718 | 0.310 | 0.766 | 0.227 |
| | ESM-IF1 | 0.422 | 0.730 | 0.331 | 0.748 | 0.223 |
*Figure from [^notin2023]*

\![[Pasted-image-20231112063046.png]]
*Figure from [^nijkamp2023]*

\![[Pasted-image-20240209164702.png]]
\![[Pasted-image-20240209164730.png]]
*Figures 3-5 from [^li2024]*

\![[Pasted-image-20241125084321.png]]
*Figure from [^vieira2024]*

\![[0.40.png]]
*Figure from [^bhatnagar2025]*

\![[Mean-p-(All-Taxa).png]]
\![[ProteinGym-(All-Taxa).png]]
*Figures from [^gurev2025]*

[^tan2023]: Tan et al. (2023) "Multi-level Protein Representation Learning for Blind Mutational Effect Prediction." https://doi.org/10.48550/arXiv.2306.04899
[^nijkamp2023]: Nijkamp et al. (2023) "ProGen2: Exploring the boundaries of protein language models." *Cell Systems*. https://doi.org/10.1016/j.cels.2023.10.002
[^notin2023]: Notin et al. (2023) "ProteinGym: Large-Scale Benchmarks for Protein Design and Fitness Prediction." https://doi.org/10.1101/2023.12.07.570727
[^detlefsen2022]: Detlefsen et al. (2022) "Learning meaningful representations of protein sequences." *Nature Communications*. https://doi.org/10.1038/s41467-022-29443-w
[^li2024]: Li et al. (2024) "Feature Reuse and Scaling: Understanding Transfer Learning with Protein Language Models." https://doi.org/10.1101/2024.02.05.578959
[^vieira2024]: Vieira et al. (2024) "Medium-sized protein language models perform well at transfer learning on realistic datasets." https://doi.org/10.1101/2024.11.22.624936
[^bhatnagar2025]: Bhatnagar et al. (2025) "Scaling Unlocks Broader Generation and Deeper Functional Understanding of Proteins." https://doi.org/10.1101/2025.04.15.649055
[^lin2023]: Lin et al. (2023) "Evolutionary-scale prediction of atomic-level protein structure with a language model." *Science*. https://doi.org/10.1126/science.ade2574
[^lee2023]: Lee et al. (2023) "Solvent: A Framework for Protein Folding." https://doi.org/10.48550/arXiv.2307.04603
[^ruffolo2024]: Ruffolo et al. (2024) "Adapting protein language models for structure-conditioned design." https://doi.org/10.1101/2024.08.03.606485
[^gurev2025]: Gurev et al. (2025) "Evaluating variant effect prediction across viruses." https://doi.org/10.1101/2025.08.04.668549
[^zhang2024]: Zhang et al. (2024) "Protein language models learn evolutionary statistics of interacting sequence motifs." *Proceedings of the National Academy of Sciences*. https://doi.org/10.1073/pnas.2406285121
[^ruffolo2025]: Ruffolo et al. (2025) "Design of highly functional genome editors by modelling CRISPR–Cas sequences." *Nature*. https://doi.org/10.1038/s41586-025-09298-z
[^peng2024]: Peng et al. (2024) "PTM-Mamba: A PTM-Aware Protein Language Model with Bidirectional Gated Mamba Blocks." https://doi.org/10.1101/2024.02.28.581983
