---
tags:
  - evolution/homology
  - inference/feature-extraction
title: PLM searches can improve remote-homology detection beyond profile HMMs
created: "2024-07-02T05:12:03"
modified: "2026-08-25T13:38:32"
---
#### Summary
**[[notes/protein-language-models|PLM]]-based searches can recover remote homologs missed by conventional profile-HMM pipelines, particularly in the 20-25% sequence-identity regime** [@kilinc2023; @liu2024plmsearch]. This does not mean that HMMs cannot identify remote homologs: HMM-HMM comparison in HHsearch was developed specifically for this task and detects relationships below 20% identity [@soding2005]. [@wu2024proteinclip] found that PLMs were better than HMM baselines at homolog detection at all scales ([[Larger PLMs are better at homolog detection|link]]).
