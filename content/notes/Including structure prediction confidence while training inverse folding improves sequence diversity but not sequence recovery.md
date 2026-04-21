---
tags:
  - inverse-folding/training
  - tm-score
  - plddt
created: "2024-05-08T18:02:06"
modified: "2026-04-21T07:03:26"
---
#### Summary
 **Including [[tags/plddt|pLDDT]] and [[tags/tm-score|pTM]] values from [[tags/structure-prediction|structure prediction]] as losses during [[tags/inverse-folding|inverse folding]] improves sequence diversity but not sequence recovery** [@melnyk2023]. By contrast, Corso et al. [@corso2024deep] found that including confidence in small molecule docking using [[DiffDock]] improved docking recovery. [@gao2023] found that predicting confidence of each residue and using that as information can improve sequence recovery ("teacher models"), leading their model to outperform other methods such as [[ProteinMPNN]].

#### Details
[@melnyk2023] used a distilled version of [[tags/alphafold2|AlphaFold2]] to calculate pLDDT and pTM.

#### Figures
![[AFDistill-pipeline.png]]
*Ref [@melnyk2023]*
