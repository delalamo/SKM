---
title: BLOSUM62
tags:
created: 2026-04-10T14:02:57
modified: "2026-04-17T06:40:29"
---

The **BLOSUM62** matrix quantifies the similarity of amino acids to one another when computing evolutionary distance sequences ([[10.1073__pnas.89.22.10915|Henikoff and Henikoff 1992]]).

![[Pasted-image-20231102143552.png]]
*Figure needs to be cited*

#### Observations

* **The BLOSUM62 matrix has math errors, but is more effective than the mathematically correct matrix** ([[10.1038__nbt0308-274|Styczynski et al 2008]]). There are some attempts to fix this but I am unaware of whether they improve or worsen performance.
* **The BLOSUM62 matrix has been used to restrict mutagenesis of [[Antibodies|antibodies]]** ([[10.1038_s41467-022-31457-3|Makowski et al 2022]]). BLOSUM-guided mutagenesis has been shown to lead to greater binding likelihood than [[Protein language models|protein language models]] and [[Inverse folding|inverse folding models]] ([[10.1101__2024.03.26.586756|Chinery et al 2024]]) in [[Trastuzumab]].
![[Pasted-image-20260323084753.png]]
* **The BLOSUM62 matrix is unsuitable for [[T-cell receptors|TCR]] analysis due to overstating the effect of non-cysteine mutations** ([[10.1093__bib__bbae602|Postovskaya et al 2024]]).
![[Pasted-image-20241127061303.png]]
	*Figure from [^postovskaya2024]*

<!-- generated -->

[^postovskaya2024]: Postovskaya et al. (2024) "tcrBLOSUM: an amino acid substitution matrix for sensitive alignment of distant epitope-specific TCRs." *Briefings in Bioinformatics*. https://doi.org/10.1093/bib/bbae602
