---
title: ImmuneBuilder
tags:
  - immunebuilder
---

**ImmuneBuilder** is an [[Antibody structure prediction]] method consisting of ABodyBuilder2 for [[Antibodies|antibodies]], NanoBodyBuilder2 for [[Nanobodies|nanobodies]], and TCRBuilder2 for [[T-cell receptors|TCRs]] ([[10.1038__s42003-023-04927-7|Abandades et al 2023]]).

#### Details

* ABodyBuilder2 is trained on [[Observable Antibody Space]] and outperforms [[AlphaFold|AlphaFold2]] on antibody [[Complementarity-determining regions#CDRH3|CDRH3]] loops. However EquiFold outperforms it on side chain recovery. Provides uncertainty estimation that correlates for CDRH3 RMSD.
* Data elision studies on ABodyBuilder2 showed that [[DL structure prediction methods cannot predict CDR conformations unseen during training]].
* Models generated with ABodyBuilder2 have [[Structural modeling introduces bias toward larger hydrophobic patches in antibodies|larger hydrophobic patches]].

#### See also

* [[Deep learning methods produce different CDRH3 conformers]]

<!-- generated -->
