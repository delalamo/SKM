---
title: DockQ
tags:
created: 2026-04-10T14:02:57
modified: "2026-04-20T08:00:05"
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
*Figure from [@hitawala2024]*

#### Details

A pDockQ of 0.50 was found to filter out nearly all false positives in a study on predicting protein-protein interactions ([[10.1038__s41594-022-00910-8|Burke et al 2023]]).

![[Pasted-image-20241002094412.png]]
*Figure from [@burke2023]*

<!-- generated -->
