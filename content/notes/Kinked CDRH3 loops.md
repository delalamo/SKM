---
title: Kinked CDRH3 loops
created: 2026-04-10T14:02:57
modified: "2026-04-20T08:32:20"
---

**Kinked [[Complementarity-determining regions#CDRH3|CDRH3]]** are a conformational feature found in 80-90% of human [[Antibodies|antibodies]] and nearly 60% of camelid [[Nanobodies|nanobodies]] ([[10.1016__j.str.2014.11.010|Weitzner et al 2015]], [[10.1038__s42003-023-05241-y|Bahrami Dizicheh et al 2023]]). This occurs at the C-terminus of the loop and is [[Germline usage determines whether nanobody CDR3 is kinked of extended|dictated by germline use]]. Similar bends are found in other proteins, such as PDZ domains and peptidase C1 domains, that are involved in [[Protein-protein interactions|protein-protein interactions]] ([[10.1016__j.str.2014.11.010|Weitzner et al 2015]]).

![[Pasted-Graphic-5-1.png]]
*Ref [^weitzner2015]*
![[42003_2023_5241_Fig1_HTML.png]]
*Ref [^bahrami2023]*

#### Details

The precise definition by Weitzner et al uses the following two parameters:
* $\mathbf{\tau_{101}}$: $C_{\alpha}$-$C_{\alpha}$-$C_{\alpha}$ pseudo-bond angle over the three C-terminal loop residues (Chothia 100X–101–102, IMGT 115-116-117).
* $\mathbf{\alpha_{101}}$: $C_{\alpha}$-$C_{\alpha}$-$C_{\alpha}$-$C_{\alpha}$ pseudo-dihedral angle over the same three residues plus the next one (Chothia 103, IMGT 118).

Then, a two-parameter model is fit over these that includes a Gaussian component centered at $\mathbf{\tau_{101}}~101°$ (80% of structures) and a von Mises component centered at $\mathbf{\alpha_{101}}~39°$. This includes about 80% of structures in the PDB at the time of the Weitzner paper. Loops that fall into this component are considered kinked, while those that don't are considered extended or straight.

#### Notes

* [[Axe-like CDRH3 loops]]


[^bahrami2023]: Bahrami Dizicheh et al. (2023) "VHH CDR-H3 conformation is determined by VH germline usage." *Communications Biology*. https://doi.org/10.1038/s42003-023-05241-y
[^weitzner2015]: Weitzner et al. (2015) "The Origin of CDR H3 Structural Diversity." *Structure*. https://doi.org/10.1016/j.str.2014.11.010
