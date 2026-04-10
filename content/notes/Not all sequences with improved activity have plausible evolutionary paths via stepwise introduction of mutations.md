---
tags: protein-design/misc
created: "2026-03-29T11:17:38"
modified: "2026-04-10T14:30:55"
---

#### Summary

**Not all sequences with improved activity have plausible evolutionary paths via stepwise introduction of mutations** [^kheronsky2018][^johnston2024][^muir2024]. This suggests that engineered libraries can access mutation combinations that are inaccessible to stepwise methods. Experimental evidence contradicting this claim was found by [^papkou2023] ([[Fitness landscapes are locally smooth but globally rugged]]). [^kirby2025] found [[Mutations obtained by antibodies during affinity maturation show epistasis in biophysical properties but not binding|evidence against this in antibodies]].

#### Details

In [^kheronsky2018], the phosphotriesterase design PTE_5 differs from dPTE2 by four mutations that were inserted simultaneously, but does not have a plausible evolutionary path to high fitness.

In [^johnston2024], where a library of 160,000 sequences saturating four positions of TrpB (tryptophan synthase) was generated, 20% of starting points had no plausible path to the optimal sequence.

[^muir2024] found that adenylate kinase variants using either zinc of hydrogen-bond networks could not be traverse by individual point mutations.

#### Figures

\![[Pasted-Graphic-26.png]]

*Figure from [^johnston2024]*

\![[Pasted-Graphic-6-1.png]]

*Figure from [^muir2024]*

#### See also

* [[Directed evolution]]
* [[Mutation memory half life]]

#### Publication history

29 March 2026: https://biomlzk.ghost.io/not-all-high-fitness-sequences-have-plausible-evolutionary-paths-from-lower-fitness-starting-points-via-sequential-introduction-of-mutations/

[^kheronsky2018]: Khersonsky et al. (2018) "Automated Design of Efficient and Functionally Diverse Enzyme Repertoires." *Molecular Cell*. https://doi.org/10.1016/j.molcel.2018.08.033
[^johnston2024]: Johnston et al. (2024) "A combinatorially complete epistatic fitness landscape in an enzyme active site." *Proceedings of the National Academy of Sciences*. https://doi.org/10.1073/pnas.2400439121
[^muir2024]: Muir et al. (2024) "Evolutionary-Scale Enzymology Enables Biochemical Constant Prediction Across a Multi-Peaked Catalytic Landscape." https://doi.org/10.1101/2024.10.23.619915
[^papkou2023]: Papkou et al. (2023) "A rugged yet easily navigable fitness landscape." *Science*. https://doi.org/10.1126/science.adh3860
[^kirby2025]: Kirby et al. (2025) "Retrospective SARS-CoV-2 human antibody development trajectories are largely sparse and permissive." *Proceedings of the National Academy of Sciences*. https://doi.org/10.1073/pnas.2412787122
