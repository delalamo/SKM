---
title: ESMFold
created: 2026-04-10T14:02:57
modified: "2026-04-21T07:28:09"
---

**ESMFold** is a [[structure-prediction|structure prediction]] method that relies on the [[ESM]]2-3B [[protein-language-models|protein language model]]. Its design includes the structure module as well as a stripped-down [[Evoformer]]. It was trained on several million [[alphafold2|AlphaFold2]] models in addition to the PDB.

![[Pasted-image-20231016155454.png]]
*Figure 2 from Lin et al. [@lin2023]*

#### Notes

* **ESMFold [[Inversion of protein folding neural networks|hallucinates]] more realistic sequences than [[alphafold2|AlphaFold2]]** [@jeliazkov2023]. No fine-tuning is required for family- or fold-specific design, unlike [[ProGen]] ([[Base PLMs must usually be fine-tuned to generate functionally active sequences]]).
* **[[AlphaFold2 outperforms ESMFold at distinguishing designable and undesignable protein backbones|ESMFold has a tendency to fold everything]]** [@hermosilla2023]. This can be more closely checked by comparing the folded structure to the contacts predicted by the language model.
* **Inversion of [[ESMFold]] has allowed high-[[plddt|pLDDT]] paths to be identified for conformational interconversion** [@del2023].
* **[[ESMFold]] can validate diffusion designs with pdbTM < 0.6 and generate structures with [[plddt|pLDDT]] > 0.7** (again sequences are designed with [[ProteinMPNN]] at temperature = 0.1; Yim et al. [@yim2023]).
* **[[ESMFold]] has been used to rank clinical pathogenicity of CFTR mutations** [@drysdale2023].
