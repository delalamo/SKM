---
title: CUMAb
tags:
  - cumab
---

**CUMAb** is a method for [[Antibody humanization|antibody humanization]] using [[Rosetta]] and human [[Germline#V-genes|V-genes]] and [[Germline#J-genes|J-genes]].
![](/assets/Pasted-image-20231016154327.png)
*Figure from [[10.1038__s41551-023-01079-1|Tennenhouse et al 2023]]*

#### Details

* Workflow:
	1. Starts from structure ([[Antibodies can be humanized using AlphaFold2 models|or model]]) of animal Fv
	2. All FW regions replaced with human sequence
	3. FW encoded by [[Germline#V-genes|V-gene]] and [[Germline#J-genes|J-gene]] ([[Somatic hypermutation]]); [[Germline#D-genes|D-gene]] in [[Complementarity-determining regions#CDRH3|CDRH3]] only, and can therefore be ignored
	4. This leads to 63,180 combinations with [[Light chains#Kappa subtype|kappa subtype]] and 48,600 with [[Light chains#Lambda subtype|lambda subtype]] light chains
	5. Ignores sequences with [[Antibody glycosylation|glycosylation]] sites and three or more cysteines
	6. In total, over 20,000 human [[Framework region]] sequences
	7. Relax w/ grafted CDRs; w/ antigen remaining fixed
	8. Eliminate designs that cause CDRs to deviate by more than 0.5 A RMSD, unless a computational model is used
	9. [[Clustering|Cluster]] by V-gene subgroup
*  Able to find non-obvious V/J-gene combinations for grafting of [[Complementarity-determining regions|CDRs]]; four of five test cases did not use human equivalent of starting genes

#### See also

* [[Humanization can destabilize antibodies]]

<!-- generated -->
