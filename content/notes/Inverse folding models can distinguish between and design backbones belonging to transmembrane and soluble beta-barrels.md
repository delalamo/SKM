---
tags:
  - protein-design/misc
---
#### Summary
 **[[Inverse folding]] methods can successfully distinguish between membrane and soluble beta barrels, and can design them with hydrophobic and hydrophilic residues in the right places** (Dolorfino & Vorobieva 2024[^dolorfino2024]). They demonstrated this with [[ProteinMPNN]].

#### Details
Before this preprint was released, ProteinMPNN was said to fail at designing transmembrane beta barrels (from Hermosilla et al's talk at [[NeurIPS_2023]]), despite designing sequences that pass all tests; the presenter suspected it was because successful designs don't occupy the ground state, which is an aggregated state.

#### Figures
![](/assets/Pasted-image-20240122095943.png)
*Figure 2 from Dolorfino & Vorobieva 2024[^dolorfino2024]*

#### See also
* [[Membrane proteins are predicted by PLMs via solvent-exposed hydrophobic residues]]

[^dolorfino2024]: Dolorfino et al. (2024) "ProteinMPNN Recovers Complex Sequence Properties of Transmembrane β-barrels." https://doi.org/10.1101/2024.01.16.575764
