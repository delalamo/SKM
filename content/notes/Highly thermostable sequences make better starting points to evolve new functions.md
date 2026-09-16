---
tags:
  - evolution/selection
  - biophysics/stability
  - design/directed-evolution
created: "2024-05-05T09:50:14"
modified: "2026-09-16T12:00:34"
---
#### Summary
 **Proteins with higher [[notes/Stability and thermostability|thermostability]] are more capable of [[Directed evolution|laboratory evolution]] new functions; e.g., they are more [[notes/Evolution and natural selection|evolvable]]** [@bloom2006]. This was determined using cytochrome P450, where stabilizing mutations acted as a buffer against destabilizing mutations.

#### Details
Additionally, [@zheng2020] found that evolving YFP to GFP had greater overall success and greater fitness if starting from YFP that was under greater selective pressure in prior rounds:

> populations under strong selection for the ancestral yellow fluorescent phenotype during phase I subsequently evolved the new green fluorescent phenotype most rapidly during phase II. Compared to populations under weak or no selection, they reached higher green fluorescence during each generation of phase II and evolved a green emission peak more rapidly

#### Mutational buffering by compensatory substitutions

Related evidence comes from super-compensatory substitutions in yeast His3p [@jiang2026supercompensators]. Among 372,867 variant genotypes, 31,701 had zero relative fitness; 3,750 (11.8%) met the study's rescuability threshold of 0.1 after additional substitutions. Rescuability sums significant fitness gains from rescuing genotypes and divides by the number of measured supersets of the original genotype; it is not the probability that an arbitrary new mutation rescues it.

Most super-compensators were more than 8 Å from the catalytic site, with none within 4 Å of the substrate. [[Rosetta]] calculations and structural analysis support stabilization as a contributing mechanism, rather than demonstrating higher melting temperatures. A new local mutagenesis experiment found that S189A improved fitness for 77% of the tested variants (Figure 5).

Super-compensators buffered both beneficial and deleterious substitution effects, producing locally flatter [[Fitness landscapes are locally smooth but globally rugged|fitness landscapes]]. This supports using robust starting backgrounds, but the study did not directly test the acquisition of a new enzymatic function.

#### Figures

![[his3-compensatory-rescuability.png]]
*Figure 1E from [@jiang2026supercompensators]. Rescuability distributions for missense genotypes and nonsense controls; N ≥ 10 denotes at least ten synonymous nucleotide variants used to estimate fitness for an amino-acid genotype.*

#### See also
* [[Ancestrally reconstructed sequences are more thermostable than extant sequences]]
* [[notes/Ancestral sequence reconstruction|Ancestral sequence reconstruction]]
* [[The majority of missense mutations are destabilizing]]
* [[Natural selection favors the highest average local fitness]]
