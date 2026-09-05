---
tags:
  - prediction/confidence
  - prediction/complexes
created: "2026-06-23"
modified: "2026-07-17T10:38:09"
---

#### Summary

**Interface contact score** (iCS) is Promera's antibody-antigen [[confidence-metrics|confidence metric]] that scores whether predicted interface contacts are likely to be true contacts [@jing2026].

#### Details

Promera trains an additional confidence module to classify each predicted interface contact as correct if it appears in the ground-truth complex and incorrect otherwise. iCS is defined as the average predicted correctness probability over the interface contacts present in the prediction.

In shuffled nanobody-antigen pairs, Promera iCS gives stronger enrichment of correct pairs than [[notes/tm-score|ipTM]] or ipSAE, reaching about 18x enrichment at 10% recall and about 20x enrichment around the high-stringency threshold discussed by the authors [@jing2026].

#### See also

* [[Different AlphaFold3 clones have differently calibrated confidence heads]]
* [[AlphaFold3 ipTM can distinguish between antibody binders and nonbinders]]
* [[iPAE is anticorrelated with number of interface H-bonds]]
* [[Correct CDRH3 prediction is necessary but insufficient for correct Ab-Ag docking]]
