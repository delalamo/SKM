---
title: GRAB motifs
created: 2026-04-05T23:36:09
modified: "2026-10-09T05:36:09"
tags:
  - antibodies/recognition
  - antibodies/repertoires
---

**[[Germline]]-encoded amino acid-binding motifs** (shortened **GRAB motifs**, coined by [@shrock2023]) are regions in [[tags/antibodies|antibodies]], mostly in the [[notes/Light chains|light chain]] [[Complementarity-determining regions|CDRs]], that target specific amino acids on the surface of potential epitopes. For example, a common lysine-binding GRAB motif is D57 in CDR2 of many lambda light chains.

Residue indices below use [[Antibody numbering|IMGT numbering]] with structural gap placement, converted from the Chothia labels in the source using the [VH](https://www.imgt.org/IMGTScientificChart/Numbering/IMGTnumberingCDR_VH.html), [Vκ](https://www.imgt.org/IMGTScientificChart/Numbering/IMGTnumberingCDR_VK.html), and [Vλ](https://www.imgt.org/IMGTScientificChart/Numbering/IMGTnumberingCDR_VL.html) correspondence tables.

#### Details
- Lysine-binding GRAB motifs:
 - In IgLV3-1, Y38 from CDR1 and N80 from framework 3; IgLV3-10, IgLV3-25, IgLV6-57, and IgLV3-21 have similar motifs (four additional lambda V-gene segments had Y/S38, D57, S/T80 predicted by AlphaFold to fold into similar structures; there are no PDB structures of these)
 - In IgLV5-37, instead the residues are Y57, D64, and N38
 - 75% of PDB Ab-Ag structures (24 out of 32) involving these six light chain V-genes maintain this interaction, and lysine was found at edge of epitope
- Asp/Glu-binding GRAB motifs:
 - IgHV3-21 CDR2 (S57, S58, S59, S63, Y64) binds D or E
 - Four of eight PDB structures with this heavy chain V-gene have this binding mode
 - IgHV3-11 also has this motif, but has no representatives in the PDB
- A second lysine-binding GRAB motif:
 - IgHV5-51 CDR1/CDR2/framework-3 residues W38, Y57, D62, D64, sometimes R66 bind lysine in 8 of 10 PDB structures
- Hydrophobic-binding GRAB motif:
 - IgKV4-1 Y31, Y38, Y108 (CDR1 and CDR3) forms nonpolar interactions with antigens, primarily recognizing proline (four examples) but also binding histidine, valine, arginine, alanine (one example each); eight out of 22 PDB IgKV4-1 structures

#### Figures
![[IgLV3-10.png]]
*Ref [@shrock2023]; the source figure retains Chothia residue labels.*
