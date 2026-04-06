---
tags: [protein-folding/misc]
created: "2024-07-02T05:10:23"
modified: "2026-04-05T23:14:54"
---

---
summary: Epistasis more likely to occur in buried residues than surface residues
tags: thermostability/prediction, epistasis/observations, fitness-prediction
---
#### Summary
**(Epistasis) more likely to occur in buried residues than surface residues** (Beltran et al 2024[^beltran2024]). In general, the effects of combinations of mutations in buried or unstructured residues are more difficult to predict, compared to exposed residues or residues on helices/sheets (van der Flier et al 2023[^van2023]). The identity of the amino acids being mutated didn't seem to matter in such cases. The use of [[Protein language models]] did not appear to help in those cases. Escobedo et al 2024[^escobedo2024] found that the effect of mutating hydrophobic cores could still be explained quite well using single and pairwise effect predictors.

#### Details
Summarized by van der Flier et al 2023[^van2023]: 

	"The contrasting results between single and combinatorial variants suggest that mutations at sites that are buried, closely connected or close to the active site are not inherently more difficult to predict. Rather, it is their occurrence alongside other mutations with the same structural characteristic that makes effect prediction harder, possibly resulting from (Epistasis)"

[^beltran2024]: Beltran et al. (2024) "Site saturation mutagenesis of 500 human protein domains reveals the contribution of protein destabilization to genetic disease." https://doi.org/10.1101/2024.04.26.591310
[^van2023]: van der Flier et al. (2023) "Enzyme Structure Correlates With Variant Effect Predictability." https://doi.org/10.1101/2023.09.25.559319
[^escobedo2024]: Escobedo et al. (2024) "Genetics, energetics and allostery during a billion years of hydrophobic protein core evolution." https://doi.org/10.1101/2024.05.11.593672
