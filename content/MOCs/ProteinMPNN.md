---
title: ProteinMPNN
tags:
  - proteinmpnn
created: "2026-04-10T14:02:57"
modified: "2026-04-20T08:32:20"
---

**ProteinMPNN** is an [[Inverse folding|inverse folding]] method that uses a message-passing neural network. It has extensive wet-lab validation.
![[Pasted-image-20231016154908.png]]
*Ref [^dauparas2022]*

#### Notes

* **ProteinMPNN scores have been shown to correlate poorly with enzyme activity** ([[Most ML quality metrics cannot effectively predict enzyme activity after controlling for similarity to native|link]]).
* **Sequence recovery using ProteinMPNN matched the success rate of [[Rosetta]] when tasked with designing small protein binders, while being much faster** ([[10.1038__s41467-023-38328-5|Bennett et al 2023]]).
* **Alternating between ProteinMPNN and [[Rosetta]] FastRelax improves success when normalized to CPU time, even though it is more expensive per sequence** ([[10.1038__s41467-023-38328-5|Bennett et al 2023]]).
* **Sequence recovery can be improved by replacing the message-passing component with [[Invariant point attention]]** (see ProteinIPMP below; [[10.1002__prot.26705|Randolph and Kuhlman 2024]]).
* **Constrained inverse folding allows design of functional enzymes** ([[10.1021__jacs.3c10941|Sumida et al 2024]]).
* **[[10.1126__science.add2187|Dauparas et al 2022]] found that ProteinMPNN was insensitive to global sequence context.** In other words, removing information about sequence adjacency had no effect on sequence recovery. This could be a symptom of [[Over-squashing]].

#### Variations

* **AbMPNN**: A retrained version specifically designed for [[Antibodies]] ([[10.48550__arXiv.2310.19513|Dreyer et al 2023]]). Outperforms default ProteinMPNN on several metrics. However it is itself outperformed by AntiFold, trained on [[ESM-IF]] ([[bxZMKHtlL6|Høie et al 2023]]).
* **MiniMPNN**: A modified version of ProteinMPNN that has $O(1)$ performance; i.e., it predicts the whole sequence in a single pass. Used by ProtPardelle ([[10.1073__pnas.2311500121|Chu et al 2024]]).
* **ProteinIPMP**: A version that uses [[Invariant point attention]], leading to accuracy improvements. Co-released with PIPPack.
![[ProteinIPMP-vs-ProteinMPNN.png]]
* **ThermoMPNN**: A topped-off version for predicting [[Stability and thermostability]]. Trained using a high-quality subset of the [[10.1038__s41586-023-06328-6|Tsuboyama et al 2023]] data ([[10.1073__pnas.2314853121|Dieckhaus et al 2024]]). Was found by [[10.1101__2024.04.26.591310|Beltran et al 2024]] to be the best at [[Variant effect prediction|variant effect prediction]].
* **LigandMPNN**: A version that can account for non-protein matter ([[10.1038__s41592-025-02626-1|Dauparas et al 2025]]).
* **IgMPNN**: A version pretrained on the PDB and fine-tuned on antibody structures ([[10.1101__2023.12.08.570889|Shanehsazzadeh et al 2023]]).
* **SoftAlign**: A retrained encoder used for structure-based alignment ([[10.1101__2025.05.09.653096|Trinquier et al 2025]]).

<!-- generated -->

[^dauparas2022]: Dauparas et al. (2022) "Robust deep learning–based protein sequence design using ProteinMPNN." *Science*. https://doi.org/10.1126/science.add2187
