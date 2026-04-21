---
tags:
  - affinity-maturation
  - conformational-dynamics/evolution
  - citation-fix
aliases:
  - Conformational entropy in antibodies decreases during affinity maturation
created: "2026-04-21T05:01:15"
modified: "2026-04-21T07:03:26"
---

#### Summary
[[Conformational entropy in antibodies decreases during affinity maturation|🔗]] **[[Protein dynamics|Conformational entropy]] in [[tags/antibodies|antibodies]] decreases during [[tags/affinity-maturation|affinity maturation]]** [@guloglu2023; @fernandezquintero2020local]. The claim is corroborated by anecdotal [[MD simulations]] [@zimmermann2006; @fernandezquintero2020; @chong1999] and various spectroscopy measurements ([[_Articles that need citations|citation needed]]). Some studies found that only [[Complementarity-determining regions#CDRH3|CDRH3]] rigidified to a statistically significant degree [@haidar2014], while other regions like the light chain CDRs either did not or became more flexible [@li2015].

#### Details

Several examples of antibody rigidification:

* Adhikary et al. [@adhikary2012] showed that five somatic mutations were sufficient to drastically reduce conformational entropy

* Chong et al. [@chong1999] showed using MD that the affinity-matured hapten-binding antibody 48G7 is less conformationally flexible than the naive [[Germline|germline]] antibody.

* Blackler et al. [@blackler2022] crystallized several closely related germline antibodies with and without antigen and found substantial variation in the conformation adopted by [[Complementarity-determining regions|CDRs]]. Nowak et al. [@nowak2016] also found that CDRs, and especially CDRH3, can adopt multiple conformations that are difficult to [[Clustering|cluster]] by sequence.

Rigidification of antibodies during affinity maturation was corroborated by three pulse photon echo peak shift spectroscopy studies showing that mature antibodies had fewer loop and sidechain motions (refs in intro to [@jeliazkov2018]). Jeliazkov et al found that the data from the PDB and from [[Rosetta]] models were not conclusive on the matter.



[@fernandezquintero2020local] propose that rigidification is due to the introduction of h-bonds, electrostatic interactions, VDW contacts, and shape complementarity. In contrast Zimmermann et al. [@zimmermann2006] found that mutations introduced "far from the active site" and closer to beta strands were responsible.



To add to the confusion, [[HDX-MS]] data suggest that [[Complementarity-determining regions#CDRH2|CDRH2]] and [[Complementarity-determining regions#CDRL2|CDRL2]], but not [[Complementarity-determining regions#CDRH3|CDRH3]], have decreased dynamics following affinity maturation [@jeliazkov2018].



[@ovchinnikov2018] suggest that rigidification is mediated by mutations in [[Framework region|framework residues]], and present a quantitative model for how [[Broadly neutralizing antibodies|broadly neutralizing antibodies]] balance broad specificity via flexibility with high affinity and selectivity with rigidification.



#### Figures

![[PCA-affinity-maturation-dynamics.png|600]]

*Ref [@fernandezquintero2018]*



#### See also

* [[Antibody thermostability decreases during affinity maturation]]

* [[Conformational entropy in antibodies is inversely proportional to antigen affinity]]

* [[Affinity-specificity tradeoff in antibodies is partially mediated by varying the magnitude of rigidification]]
