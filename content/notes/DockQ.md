---
title: DockQ
created: 2026-04-10T14:02:57
modified: "2026-04-20T08:32:20"
---

*(pDockQ redirects here)*
**DockQ** is a metric ranging from zero to one that is used to evaluate [[Structure prediction|predicted structures]] of [[Protein-protein interactions|protein complexes]] ([[10.1371__journal.pone.0161879|Basu & Wallner 2016]]):

$$
DockQ=\frac{1}{3}\left( f_{nat} +\frac{1}{1+\left( \frac{iRMSD}{1.5}\right)^{2}} +\frac{1}{1+\left( \frac{LRMSD}{8.5}\right)^{2}} \right)
$$

$f_{Nat}$: Fraction of native contacts
$iRMSD$: Interface RMSD
$LRMSD$: Ligand RMSD
A DockQ value of 0.23 or better is usually treated as a correctly docked pose.

#### Details

![[Pasted-image-20241001064019.png]]
*Ref [^hitawala2024]*

#### Details

A pDockQ of 0.50 was found to filter out nearly all false positives in a study on predicting protein-protein interactions ([[10.1038__s41594-022-00910-8|Burke et al 2023]]).

![[Pasted-image-20241002094412.png]]
*Ref [^burke2023]*


[^burke2023]: Burke et al. (2023) "Towards a structurally resolved human protein interaction network." *Nature Structural & Molecular Biology*. https://doi.org/10.1038/s41594-022-00910-8
[^hitawala2024]: Hitawala & Gray (2024) "What does AlphaFold3 learn about antigen and nanobody docking, and what remains unsolved?." https://doi.org/10.1101/2024.09.21.614257
