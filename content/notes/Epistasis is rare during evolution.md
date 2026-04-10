---
title: Epistasis is rare during evolution
tags:
  - protein-design/misc
created: "2026-03-16T11:36:47"
modified: "2026-04-10T15:26:33"
---
#### Summary
 **[[Epistasis]], in which protein fitness changes in a non-additive way, is rare in natural evolution and laboratory evolution.** Simple statistical models with only additive effects can explain most (80-95%) of changes in activity between variants [^ding2024][^faure2024][^beltran2024][^alcantar2025]. This has been suggested by multiple studies, which found that the effect of mutations that improve [[Stability and thermostability]] was basically entirely additive (see figure below).[^peleg2021][^escobedo2024][^alcantar2025] Park et al. were able to model 92-96% of variance in genome fitness by accounting exclusively for single-point and pairwise interactions plus a sigmoid nonlinearity; e.g., less than <5% of genomes in their test set showed third-order interactions.[^park2023] That said, there are examples where linear models are unable to accurately model fitness ([^faure2024], [^ding2024], [^tonner2022] with [[Spike protein]]/[[ACE2]]), so the type of statistical model still matters. 

#### Details
Sarkisyan et al. found that some mutations killed fluorescence in some GFP backbones but not others, and that pre-existing evolutionary propensity (e.g., from a PSSM) could not predict this.[^sarkisyan2016] They conclude that this is the result of destabilization. this made an additive model of fluorescence inappropriate; from that perspective epistasis occurred in 30% of multi-substitution variants. They conclude that this is largely due to threshold robustness, and that these mutations are destabilizing. See [[Mutation memory half life]]. Anecdotally [^tonner2022] came to a similar conclusion.

Beltran et al. measured >500k pathogenic variants in human diseases across 500 domains and found that additive models were sufficient to model almost all fitness changes.[^beltran2024]

Escobedo et al. found that the effects of substitutions in the hydrophobic core of proteins could be explained by linear models.[^escobedo2024]

Alcantar et al. carried out a "combinatorially complete" analysis of mutations introduced during [[Affinity maturation|affinity maturation]] of *de novo* designed minibinders and found that the binding improvements were basically entirely additive, which is similar to [[Antibodies|antibodies]] ([[Mutations obtained by antibodies during affinity maturation show epistasis in biophysical properties but not binding]]).[^alcantar2025]

#### Figures
\![[Pasted-image-20231015161415.png]]
*Figure from [^peleg2021]*

\![[Epistasis_frequency.png]]
*Figure from [^sarkisyan2016]*

\![[Pasted-image-20240223071500.png]]
*Figure 2 from [^ding2024]*

#### See also
* [[Stability-activity trade-off during enzyme design and evolution is highly local and not global]]
* [[Mutations obtained by antibodies during affinity maturation show epistasis in biophysical properties but not binding]]

[^ding2024]: Ding et al. (2024) "Protein design using structure-based residue preferences." *Nature Communications*. https://doi.org/10.1038/s41467-024-45621-4
[^faure2024]: Faure et al. (2024) "The genetic architecture of protein stability." *Nature*. https://doi.org/10.1038/s41586-024-07966-0
[^beltran2024]: Beltran et al. (2024) "Site saturation mutagenesis of 500 human protein domains reveals the contribution of protein destabilization to genetic disease." https://doi.org/10.1101/2024.04.26.591310
[^alcantar2025]: Alcantar et al. (2025) "Mapping the evolution of computationally designed protein binders." https://doi.org/10.1101/2025.10.04.680454
[^peleg2021]: Peleg et al. (2021) "Community-Wide Experimental Evaluation of the PROSS Stability-Design Method." *Journal of Molecular Biology*. https://doi.org/10.1016/j.jmb.2021.166964
[^escobedo2024]: Escobedo et al. (2024) "Genetics, energetics and allostery during a billion years of hydrophobic protein core evolution." https://doi.org/10.1101/2024.05.11.593672
[^park2023]: Park et al. (2023) "The simplicity of protein sequence-function relationships." https://doi.org/10.1101/2023.09.02.556057
[^tonner2022]: Tonner et al. (2022) "Interpretable modeling of genotype–phenotype landscapes with state-of-the-art predictive power." *Proceedings of the National Academy of Sciences*. https://doi.org/10.1073/pnas.2114021119
[^sarkisyan2016]: Sarkisyan et al. (2016) "Local fitness landscape of the green fluorescent protein." *Nature*. https://doi.org/10.1038/nature17995
