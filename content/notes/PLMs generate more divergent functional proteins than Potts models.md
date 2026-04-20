---
tags: 
  - protein-design/enzyme-design
created: "2024-10-27T04:47:55"
modified: "2026-04-20T07:16:03"
---

#### Summary
**Proteins designed using PLMs more unique than those designed using Potts models** [^madani2023]. For example, $\beta$-lactamase sequences designed using [[Potts models]] by [^fram2023] were found to be active up to 50% sequence identity, but not more. This also includes [[MSA-transformer]][^sgarbossa2023]. In contrast, lysozyme sequences designed using (ProGen) model after fine-tuning achieve activity with identities as low as 31% [^madani2023]. In the same experiment, bmDCA-generated sequences were inactive. Other studies have found that they are more likely to fold with high [[TM-score]][^alamdari2023].

#### Figures
![[Pasted-image-20231107232400.png|400]]
*Figure from [^fram2023]*

![[PF00072.jpg]]
*Figure from [^sgarbossa2023]*

![[Pasted-image-20241105054851.png]]
*Figure from [^alamdari2023]*

[^madani2023]: Madani et al. (2023) "Large language models generate functional protein sequences across diverse families." *Nature Biotechnology*. https://doi.org/10.1038/s41587-022-01618-2
[^fram2023]: Fram et al. (2024) "Simultaneous enhancement of multiple functional properties using evolution-informed protein design." Nature Communications. https://doi.org/10.1038/s41467-024-49119-x
[^sgarbossa2023]: Sgarbossa et al. (2023) "Generative power of a protein language model trained on multiple sequence alignments." *eLife*. https://doi.org/10.7554/eLife.79854
[^alamdari2023]: Alamdari et al. (2023) "Protein generation with evolutionary diffusion: sequence is all you need." https://doi.org/10.1101/2023.09.11.556673
