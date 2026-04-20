---
title: Evolution and natural selection
aliases:
  - Evolution and natural selection
created: "2026-04-10T14:02:57"
modified: "2026-04-20T10:13:23"
---

Protein **evolution** is the process and result of gradual sequence changes resulting in functional and/or structural changes. See [[Epistasis]] for examples on why evolutionary trajectories are difficult to predict. This note excludes any discussion of [[Somatic hypermutation|somatic hypermutation]].

## Notes

#### Paradigms and preliminaries

- **Neutral theory:** most observed amino acid changes are neutral (i.e., silent in fitness effects). This leads to **genetic drift**. Developed by [[Kimura 1985]].
- **Nearly neutral theory:** deleterious mutations are retained and subsequently compensated for by advantageous mutations (which is consistent with the observation that [[The majority of missense mutations are destabilizing|most missense mutations are destabilizing]]). Developed by [[10.1038__246096a0|Ohta 1973]] to explain why the rate of protein evolution was independent of generation time, which is in turn inversely proportional to population size.
  ![[Equilibrium.png]]
  _Figure from [^ohta1973]_
- The theory of **punctuated equilibrium** suggests that phenotypes change very little for long stretches of time, followed by abrupt rapid changes ([[10.1016__j.tree.2024.05.003|Duran et al 2024]]).
- **Statistical physics approach:** population size is equated with inverse temperature (such that infinite population is analogous to zero degrees Kelvin), and log-[[Fitness prediction|fitness]] with energy ([[10.1073__pnas.0501865102|Sella & Hirsh 2005]]). Advantageous and deleterious mutations are predicted to occur with equal frequency. This framing ignores the imbalance in sequence data ([[10.1101__2024.03.07.584001|Ding & Steinhardt 2024]], [[10.1101__2022.01.29.478324|Weinstein et al 2022]]).
- **Fisher's geometric model:** The overall fitness of a phenotype can be quantified along $N$ dimensions; Fisher postulated that phenotypes in a population were distributed as a hypersphere centered on a local maximum.
- **Protein evolvability** refers to the ability of a protein to 1) [[Evolution and natural selection|evolve]] new functions in relatively few mutations and 2) be robust to mutations that lead to loss-of-function ([[10.1098__rspb.2007.1137|Wagner 2007]]). These are described as contradictory statements by [[10.1126__science.1169375|Tokuriki & Tawfik 2009]] but are described as complementary at the structural level.
- "The **principle of minimal frustration** suggests that naturally evolved proteins with the same structure should have similar folding rates and that modulation of thermodynamic stability should occur via unfolding rates" (quoted from [[10.1073__pnas.1613892114|Tzul et al 2017]]). This has been supported by the observation that [[Differences in thermostability of structurally similar proteins are due to differences in unfolding rates|thioredoxins fold at similar rates but unfold at rates that correlate with their thermostability values]].

#### Observations

- **Protein folds with high sequence diversity also have high functional diversity** ([[10.1098__rspb.2007.1137|Wagner 2007]]).
- **The sequence capacity of a protein exceeds $10^{23}$ for even small proteins (35-40 AAs), but the fraction of [[Stability and thermostability|stable]] states is extremely small and inversely correlated with protein size.** These values were estimated using [[Potts models]] ([[10.1016__j.bpj.2017.08.039|Tian & Best 2017]]).
  ![[TABLE-1-Estimates-of-SC.png]]
  _Figure from [^tian2017]_
