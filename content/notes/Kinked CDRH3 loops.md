---
title: Kinked CDRH3 loops
created: 2026-04-10T14:02:57
modified: "2026-04-21T07:28:09"
---

**Kinked [[Complementarity-determining regions#CDRH3|CDRH3]]** are a conformational feature found in 80-90% of human [[antibodies|antibodies]] and nearly 60% of camelid [[Nanobodies|nanobodies]] [@weitzner2015; @bahrami2023]. This occurs at the C-terminus of the loop and is [[Germline usage determines whether nanobody CDR3 is kinked of extended|dictated by germline use]]. Similar bends are found in other proteins, such as PDZ domains and peptidase C1 domains, that are involved in [[protein-protein-interactions|protein-protein interactions]] [@weitzner2015].

![[Pasted-Graphic-5-1.png]]
*Ref [@weitzner2015]*
![[42003_2023_5241_Fig1_HTML.png]]
*Ref [@bahrami2023]*

#### Details

The precise definition by Weitzner et al uses the following two parameters:
* $\mathbf{\tau_{101}}$: $C_{\alpha}$-$C_{\alpha}$-$C_{\alpha}$ pseudo-bond angle over the three C-terminal loop residues (Chothia 100X–101–102, IMGT 115-116-117).
* $\mathbf{\alpha_{101}}$: $C_{\alpha}$-$C_{\alpha}$-$C_{\alpha}$-$C_{\alpha}$ pseudo-dihedral angle over the same three residues plus the next one (Chothia 103, IMGT 118).

Then, a two-parameter model is fit over these that includes a Gaussian component centered at $\mathbf{\tau_{101}}~101°$ (80% of structures) and a von Mises component centered at $\mathbf{\alpha_{101}}~39°$. This includes about 80% of structures in the PDB at the time of the Weitzner paper. Loops that fall into this component are considered kinked, while those that don't are considered extended or straight.

#### Notes

* [[Axe-like CDRH3 loops]]
