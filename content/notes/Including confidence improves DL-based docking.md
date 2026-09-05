---
tags:
  - prediction/ligand-docking
  - training/objectives-and-optimization
created: "2024-05-02T18:09:03"
modified: "2026-04-21T07:28:09"
review:
  - "citation-fix"
---

#### Summary
Small molecule docking accuracy can by improved by including confidence during training of small molecule docking via DiffDock and propagating that information to the early frames. Corso et al. [@corso2024deep] showed this as a form of [[notes/Diffusion guidance|guidance]]-involved training.

#### See also

* [[DiffDock confidence is inversely correlated with RMSD]]
* [[Including structure prediction confidence while training inverse folding improves sequence diversity but not sequence recovery]]
