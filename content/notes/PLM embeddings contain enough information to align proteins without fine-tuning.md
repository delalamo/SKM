---
tags:
  - protein-folding/misc
created: "2025-02-10T07:37:30"
modified: "2026-04-10T14:15:21"
---

## Summary

**[[Protein language models|PLM]] embeddings contain enough information to be aligned without fine-tuning** ([Kaminski et al 2023][^kaminski2023]), **and these alignments outperform purely sequence-based but not structure-based methods** ([Llinares-López et al 2022][^llinareslpez2022], [Hamamsmy et al 2023][^hamamsy2023]). This could be since the embeddings of aligned positions in related sequences tend to co-[[Clustering|cluster]] ([McWhite et al 2023][^mcwhite2023]). Alignment quality can be further improved by normalization ([Pantolini et al 2022][^pantolini2022]), which does not require PLM fine-tuning. [Ashrafzadeh et al 2023][^ashrafzadeh2023] surmise that the distance matrices implied by these embeddings are more effective than the [[BLOSUM62]] matrix used by many sequence alignments by default.

## Details

TM-vec, a fine-tuned model, was found to be worse than non-fine-tuned models ([Hamamsmy et al 2023][^hamamsy2023]).

To improve alignment quality using "normalization" (per [Pantolini et al 2022][^pantolini2022]), all distances (for their paper, Euclidean distances are used) are computed and converted to Z-scores to normalize relative to other entries in the same column and row. This was shown to improve performance relative to using non-normalized/enhanced values for alignment calculation.

## Figures

\![[MSA-and-embeddings-with-glycines-in-rec.png]]
*Figure from [McWhite et al 2023][^mcwhite2023]*

\![[Malidup.png]]
*Figure from [Hamamsmy et al 2023][^hamamsy2023]*

\![[ProtTuker.png]]
*Figure from [Pantolini et al 2022][^pantolini2022]; EBA and EBA-plain refer to PLM-based alignment with and without normalization*

## See also

* [[Multiple sequence alignments]]
* [[PLMs learn family-specific protein contacts from sequence context windows of about 20-40 amino acids]]

[^kaminski2023]: Kaminski et al. (2023) "pLM-BLAST: distant homology detection based on direct comparison of sequence representations from protein language models." *Bioinformatics*. https://doi.org/10.1093/bioinformatics/btad579
[^llinareslpez2022]: Llinares-López et al. (2022) "Deep embedding and alignment of protein sequences." *Nature Methods*. https://doi.org/10.1038/s41592-022-01700-2
[^hamamsy2023]: Hamamsy et al. (2023) "Protein remote homology detection and structural alignment using deep learning." *Nature Biotechnology*. https://doi.org/10.1038/s41587-023-01917-2
[^mcwhite2023]: McWhite et al. (2023) "Leveraging protein language models for accurate multiple sequence alignments." *Genome Research*. https://doi.org/10.1101/gr.277675.123
[^pantolini2022]: Pantolini et al. (2022) "Embedding-based alignment: combining protein language models and alignment approaches to detect structural similarities in the twilight-zone." https://doi.org/10.1101/2022.12.13.520313
[^ashrafzadeh2023]: Ashrafzadeh et al. (2023) "Scoring alignments by embedding vector similarity." https://doi.org/10.1101/2023.08.30.555602
