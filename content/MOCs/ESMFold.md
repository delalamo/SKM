---
title: ESMFold
tags:
  - esmfold
created: "2026-04-10T14:02:57"
modified: "2026-04-11T07:41:30"
---

**ESMFold** is a [[Structure prediction|structure prediction]] method that relies on the [[ESM]]2-3B [[Protein language models|protein language model]]. Its design includes the structure module as well as a stripped-down [[Evoformer]]. It was trained on several million [[AlphaFold|AlphaFold2]] models in addition to the PDB.

![[Pasted-image-20231016155454.png]]
*Figure 2 from [[10.1126__science.ade2574|Lin et al 2023]]*

#### Notes

* **ESMFold [[Inversion of protein folding neural networks|hallucinates]] more realistic sequences than [[AlphaFold]]** ([[10.1101__2023.05.23.541774|Jeliazkov et al 2023]]). No fine-tuning is required for family- or fold-specific design, unlike [[ProGen]] ([[Base PLMs must usually be fine-tuned to generate functionally active sequences]]).
* **[[AlphaFold2 outperforms ESMFold at distinguishing designable and undesignable protein backbones|ESMFold has a tendency to fold everything]]** ([[10.1101__2023.06.06.543955|Hermosilla et al 2023]]). This can be more closely checked by comparing the folded structure to the contacts predicted by the language model.
* **Inversion of [[ESMFold]] has allowed high-[[pLDDT]] paths to be identified for conformational interconversion** ([[10.1101__2023.12.16.571997|del Alamo et al 2023]]).
* **[[ESMFold]] can validate diffusion designs with pdbTM < 0.6 and generate structures with [[pLDDT]] > 0.7** (again sequences are designed with [[ProteinMPNN]] at temperature = 0.1; [[10.48550__arXiv.2302.02277|Yim et al 2023]]).
* **[[ESMFold]] has been used to rank clinical pathogenicity of CFTR mutations** ([[10.1101__2023.10.26.564274v1|Drysdale 2023]]).

<!-- generated -->
