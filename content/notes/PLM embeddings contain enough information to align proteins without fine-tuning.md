---
tags:
  - protein-folding/misc
created: "2025-02-10T07:37:30"
modified: "2026-04-10T14:02:57"
---

## Summary

**[[Protein language models|PLM]] embeddings contain enough information to be aligned without fine-tuning** ([Kaminski et al 2023](https://doi.org/10.1093/bioinformatics/btad579)), **and these alignments outperform purely sequence-based but not structure-based methods** ([Llinares-López et al 2022](https://doi.org/10.1038/s41592-022-01700-2), [Hamamsmy et al 2023](https://doi.org/10.1038/s41587-023-01917-2)). This could be since the embeddings of aligned positions in related sequences tend to co-[[Clustering|cluster]] ([McWhite et al 2023](https://doi.org/10.1101/gr.277675.123)). Alignment quality can be further improved by normalization ([Pantolini et al 2022](https://doi.org/10.1101/2022.12.13.520313)), which does not require PLM fine-tuning. [Ashrafzadeh et al 2023](https://doi.org/10.1101/2023.08.30.555602) surmise that the distance matrices implied by these embeddings are more effective than the [[BLOSUM62]] matrix used by many sequence alignments by default.

## Details

TM-vec, a fine-tuned model, was found to be worse than non-fine-tuned models ([Hamamsmy et al 2023](https://doi.org/10.1038/s41587-023-01917-2)).

To improve alignment quality using "normalization" (per [Pantolini et al 2022](https://doi.org/10.1101/2022.12.13.520313)), all distances (for their paper, Euclidean distances are used) are computed and converted to Z-scores to normalize relative to other entries in the same column and row. This was shown to improve performance relative to using non-normalized/enhanced values for alignment calculation.

## Figures

\![[MSA-and-embeddings-with-glycines-in-rec.png]]
*Figure from [McWhite et al 2023](https://doi.org/10.1101/gr.277675.123)*

\![[Malidup.png]]
*Figure from [Hamamsmy et al 2023](https://doi.org/10.1038/s41587-023-01917-2)*

\![[ProtTuker.png]]
*Figure from [Pantolini et al 2022](https://doi.org/10.1101/2022.12.13.520313); EBA and EBA-plain refer to PLM-based alignment with and without normalization*

## See also

* [[Multiple sequence alignments]]
* [[PLMs learn family-specific protein contacts from sequence context windows of about 20-40 amino acids]]
