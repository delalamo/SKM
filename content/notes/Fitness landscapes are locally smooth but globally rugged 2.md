---
title: Fitness landscapes are locally smooth but globally rugged
tags:
  - protein-design/misc
created: "2024-05-05T09:49:33"
modified: "2026-04-10T14:30:55"
---
#### Summary
 **Fitness landscapes are locally smooth but globally rugged** [^papkou2023]. In other words, effects of mutations on fitness are locally additive but become defined by non-additive interactions as mutations accumulate [^beltran2024]. However some contradictory evidence exists (see [[Not all sequences with improved activity have plausible evolutionary paths via stepwise introduction of mutations]]).

#### Details
 Mutants of dihydrofolate reductase were found to be distributed across many fitness peaks. However, for variants similar (<6 mutations from local maxima), the number of steps required to reach the local fitness maxima while maintaining a monotonically improving evolutionary trajectory generally matched the total number of substitutions anyway; in other words, there was a way to reach the local maxima without extra steps. 

[^beltran2024] say the following (figure numbers and statistics edited out for clarity):

> The excellent performance of these additive energy models is both useful and important: it demonstrates that epistasis makes only a small contribution to protein stability across these levels of sequence divergence. Combinatorial mutagenesis of individual proteins suggests a similar conclusion. The decay of predictive performance with sequence divergence does, however, suggest a role for epistasis in the evolution of protein stability. Indeed, we identify 25,410 mutations with evidence of epistasis as vriants with large residuals to the Boltzmann model fits. These epistatic variants are enriched in the buried cores of protein domains and depleted from protein surfaces, across the full range of measured stabilities and protein families.

#### Figures
\![[Pasted-image-20231128234239.png]]
*Figure from [^papkou2023]*

[^papkou2023]: Papkou et al. (2023) "A rugged yet easily navigable fitness landscape." *Science*. https://doi.org/10.1126/science.adh3860
[^beltran2024]: Beltran et al. (2024) "Site saturation mutagenesis of 500 human protein domains reveals the contribution of protein destabilization to genetic disease." https://doi.org/10.1101/2024.04.26.591310
