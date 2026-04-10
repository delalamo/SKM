---
tags:
  - protein-design/misc
created: "2024-05-08T18:02:06"
modified: "2026-04-10T14:30:55"
---
#### Summary
 **Including [[pLDDT]] and [[TM-score|pTM]] values from [[Structure prediction|structure prediction]] as losses during [[Inverse folding|inverse folding]] improves sequence diversity but not sequence recovery** [^melnyk2023]. By contrast, (Corso et al 2023b) found that including confidence in small molecule docking using [[DiffDock]] improved docking recovery. [^gao2023] found that predicting confidence of each residue and using that as information can improve sequence recovery ("teacher models"), leading their model to outperform other methods such as [[ProteinMPNN]].

#### Details
[^melnyk2023] used a distilled version of [[AlphaFold|AlphaFold2]] to calculate pLDDT and pTM.

#### Figures
\![[AFDistill-pipeline.png]]
*Figure from [^melnyk2023]*

[^melnyk2023]: Melnyk et al. (2022) "AlphaFold Distillation for Protein Design." https://doi.org/10.48550/arXiv.2210.03488
[^gao2023]: Gao et al. (2023) "Knowledge-Design: Pushing the Limit of Protein Design via Knowledge Refinement." https://doi.org/10.48550/arXiv.2305.15151
