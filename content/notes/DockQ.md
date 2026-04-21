---
title: DockQ
created: 2026-04-10T14:02:57
modified: "2026-04-21T07:28:09"
---

*(pDockQ redirects here)*
**DockQ** is a metric ranging from zero to one that is used to evaluate [[structure-prediction|predicted structures]] of [[protein-protein-interactions|protein complexes]] [@basu2016]:

$$
DockQ=\frac{1}{3}\left( f_{nat} +\frac{1}{1+\left( \frac{iRMSD}{1.5}\right)^{2}} +\frac{1}{1+\left( \frac{LRMSD}{8.5}\right)^{2}} \right)
$$

$f_{Nat}$: Fraction of native contacts
$iRMSD$: Interface RMSD
$LRMSD$: Ligand RMSD
A DockQ value of 0.23 or better is usually treated as a correctly docked pose.

#### Details

![[Pasted-image-20241001064019.png]]
*Ref [@hitawala2024]*

#### Details

A pDockQ of 0.50 was found to filter out nearly all false positives in a study on predicting protein-protein interactions [@burke2023].

![[Pasted-image-20241002094412.png]]
*Ref [@burke2023]*
