---
tags:
  - prediction/confidence
  - prediction/structure
  - prediction/complexes
created: "2026-09-28"
modified: "2026-09-28T18:27:42"
---

#### Summary

**Confidence modules from [[notes/Diffusion models|diffusion-based]] [[notes/Structure prediction|structure prediction]] methods can score supplied structures while bypassing diffusion generation.** AF3Score feeds input coordinates directly into the [[notes/AlphaFold3|AlphaFold3]] confidence head, allowing candidate structures to be evaluated without first refining them through the structure-generation module [@liu2025af3score]. This provides a concrete way to use [[Structure prediction uncertainty metrics as energy functions|structure prediction uncertainty metrics as energy-like scoring functions]].

AF3Score was evaluated on monomers, protein complexes, designed binders, fold-switching proteins, and protein–ligand complexes. In the authors' designed-binder screening benchmark, it outperformed comparator methods on eight of ten targets; combining it with AlphaFold2-derived methods increased the success rate from 15.2% to 31.6% [@liu2025af3score]. Its ability to score alternative folds also connects to the observation that [[Structure prediction methods undersample the conformational space they find to be high-confidence|predictors can assign high confidence to conformations they fail to generate]].

TorchScore similarly evaluates supplied coordinates through the TorchFold confidence pathway with the same model weights and no separately trained scoring network. With the antibody–antigen checkpoint, its [[notes/TM-score|ipTM]] correlated with [[DockQ]] at Pearson 0.869 on pooled PDB55 candidates [@torchfold2026, Appendix C].

These scores estimate structural quality. Their usefulness for ranking candidates or enriching binders does not establish [[Protein structure prediction and design confidence metrics do not correlate with binding affinity|general binding-affinity prediction]] or calibrated thermodynamic energies. [[Different AlphaFold3 clones have differently calibrated confidence heads|Calibration depends on the checkpoint]], and a pooled candidate-level correlation need not imply equally strong ranking within each target's ensemble.

#### Related notes

- [[Structure prediction uncertainty metrics as energy functions]]
- [[Diffusion-based protein structure prediction methods double as energy methods comparable to traditional force fields]]
- [[AlphaFold3 ipTM can distinguish between antibody binders and nonbinders]]
- [[Boltz-2 intermediate representations can predict protein-protein binding affinity]]
- [[Confidence metrics for diffusion-based structure prediction methods can be improved with minimal changes to conditioning representations]]
