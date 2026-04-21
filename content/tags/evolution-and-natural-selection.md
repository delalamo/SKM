---
title: Evolution and natural selection
aliases:
  - Evolution and natural selection
created: "2026-04-10T14:02:57"
modified: "2026-04-20T08:16:13"
---

Protein **evolution** is the process and result of gradual sequence changes resulting in functional and/or structural changes. See [[Epistasis]] for examples on why evolutionary trajectories are difficult to predict. This note excludes any discussion of [[Somatic hypermutation|somatic hypermutation]].

## Notes

#### Paradigms and preliminaries

- **Neutral theory:** most observed amino acid changes are neutral (i.e., silent in fitness effects). This leads to **genetic drift**. Developed by Kimura [@kimura1985].
- **Nearly neutral theory:** deleterious mutations are retained and subsequently compensated for by advantageous mutations (which is consistent with the observation that [[The majority of missense mutations are destabilizing|most missense mutations are destabilizing]]). Developed by Ohta [@ohta1973] to explain why the rate of protein evolution was independent of generation time, which is in turn inversely proportional to population size.
 ![[Equilibrium.png]]
 _Figure from [@ohta1973]_
- The theory of **punctuated equilibrium** suggests that phenotypes change very little for long stretches of time, followed by abrupt rapid changes [@durannebreda2024].
- **Statistical physics approach:** population size is equated with inverse temperature (such that infinite population is analogous to zero degrees Kelvin), and log-[[Fitness prediction|fitness]] with energy [@sella2005]. Advantageous and deleterious mutations are predicted to occur with equal frequency. This framing ignores the imbalance in sequence data [@ding2024protein; @weinstein2022].
- **Fisher's geometric model:** The overall fitness of a phenotype can be quantified along $N$ dimensions; Fisher postulated that phenotypes in a population were distributed as a hypersphere centered on a local maximum.
- **Protein evolvability** refers to the ability of a protein to 1) [[Evolution and natural selection|evolve]] new functions in relatively few mutations and 2) be robust to mutations that lead to loss-of-function [@wagner2007]. These are described as contradictory statements by Tokuriki & Tawfik [@tokuriki2009] but are described as complementary at the structural level.
- "The **principle of minimal frustration** suggests that naturally evolved proteins with the same structure should have similar folding rates and that modulation of thermodynamic stability should occur via unfolding rates" (quoted from [@tzul2017]). This has been supported by the observation that [[Differences in thermostability of structurally similar proteins are due to differences in unfolding rates|thioredoxins fold at similar rates but unfold at rates that correlate with their thermostability values]].

#### Observations

- **Protein folds with high sequence diversity also have high functional diversity** [@wagner2007].
- **The sequence capacity of a protein exceeds $10^{23}$ for even small proteins (35-40 AAs), but the fraction of [[Stability and thermostability|stable]] states is extremely small and inversely correlated with protein size.** These values were estimated using [[Potts models]] [@tian2017].
 ![[TABLE-1-Estimates-of-SC.png]]
 _Figure from [@tian2017]_
