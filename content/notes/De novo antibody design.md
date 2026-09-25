---
title: De novo antibody design
tags:
  - design/antibodies
created: 2026-04-10T14:30:55
modified: "2026-08-25T10:16:02"
review:
  - "citation-fix"
---

***De novo* [[tags/antibodies|antibody]] design** aims to create antibodies purely *in silico* that are capable of binding antigens at predefined epitopes in user-specified ways.

#### Summary of methods

* [[Inversion of protein folding neural networks|Backpropagation]]-based
	* Germinal [@millefragoso2025]
	* BoltzDesign [@cho2025b]
* [[notes/Diffusion models|Diffusion]]/flow matching-based
	* RF-antibody [@bennett2024]
	* DiffAb
	* IgGM
	* TiDE-Ab [@kim2026tideab]
	* BoltzGen
	* Boltz (but requires [[notes/Inverse folding|structure-based sequence design]]; [@wohlwend2024])
* Unknown due to proprietary methods
	* Chai-2
	* JAM-2 (Nabla)
    * Latent-X 
