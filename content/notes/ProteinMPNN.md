---
title: ProteinMPNN
tags:
  - proteinmpnn
created: "2026-04-10T14:02:57"
modified: "2026-04-21T07:03:26"
---

**ProteinMPNN** is an [[tags/inverse-folding|inverse folding]] method that uses a message-passing neural network. It has extensive wet-lab validation.
![[Pasted-image-20231016154908.png]]
*Ref [@dauparas2022]*

#### Notes

* **ProteinMPNN scores have been shown to correlate poorly with enzyme activity** ([[Most ML quality metrics cannot effectively predict enzyme activity after controlling for similarity to native|link]]).
* **Sequence recovery using ProteinMPNN matched the success rate of [[Rosetta]] when tasked with designing small protein binders, while being much faster** [@bennett2023].
* **Alternating between ProteinMPNN and [[Rosetta]] FastRelax improves success when normalized to CPU time, even though it is more expensive per sequence** [@bennett2023].
* **Sequence recovery can be improved by replacing the message-passing component with [[Invariant point attention]]** (see ProteinIPMP below; [@randolph2024]).
* **Constrained inverse folding allows design of functional enzymes** [@sumida2024].
* **Dauparas et al. [@dauparas2022] found that ProteinMPNN was insensitive to global sequence context.** In other words, removing information about sequence adjacency had no effect on sequence recovery. This could be a symptom of [[Over-squashing]].

#### Variations

* **AbMPNN**: A retrained version specifically designed for [[tags/antibodies|Antibodies]] [@dreyer2023]. Outperforms default ProteinMPNN on several metrics. However it is itself outperformed by AntiFold, trained on [[ESM-IF]] [@hoie2023].
* **MiniMPNN**: A modified version of ProteinMPNN that has $O(1)$ performance; i.e., it predicts the whole sequence in a single pass. Used by ProtPardelle [@chu2023].
* **ProteinIPMP**: A version that uses [[Invariant point attention]], leading to accuracy improvements. Co-released with PIPPack.
![[ProteinIPMP-vs-ProteinMPNN.png]]
* **ThermoMPNN**: A topped-off version for predicting [[tags/thermostability|Stability and thermostability]]. Trained using a high-quality subset of the Tsuboyama et al. [@tsuboyama2023] data [@dieckhaus2024]. Was found by Beltran et al. [@beltran2024] to be the best at [[tags/variant-effect-prediction|variant effect prediction]].
* **LigandMPNN**: A version that can account for non-protein matter [@dauparas2023].
* **IgMPNN**: A version pretrained on the PDB and fine-tuned on antibody structures [@shanehsazzadeh2023].
* **SoftAlign**: A retrained encoder used for structure-based alignment [@trinquier2025].
