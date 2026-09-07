---
tags:
  - prediction/confidence
  - prediction/complexes
created: "2026-06-23"
modified: "2026-07-17T10:38:09"
---

#### Summary

**Different [[notes/AlphaFold3|AlphaFold3]] clones have differently calibrated confidence heads.** AF3-family and open-source clone confidence heads differ in calibration and binder-filtering behavior, affecting their suitability for antibody-antigen docking and design workflows [@jing2026; @smorodina2026].

#### Figures

![[af3-clones-confidence-head-calibration-promera.jpg]]

*Figure from [@jing2026]*

![[af3-clones-confidence-head-calibration-smorodina.png]]

*Figure from [@smorodina2026]*

#### See also

* [[The confidence metrics of AlphaFold2 are better calibrated than those of AlphaFold3]]
* [[AlphaFold3 ipTM can distinguish between antibody binders and nonbinders]]
* [[Structure prediction uncertainty metrics as energy functions]]
