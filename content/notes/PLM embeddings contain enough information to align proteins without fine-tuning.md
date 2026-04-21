---
tags:
  - protein-language-models/representations
  - alignment/sequence-based
created: "2025-02-10T07:37:30"
modified: "2026-04-21T05:01:15"
---

## Summary

**[[Protein language models|PLM]] embeddings contain enough information to be aligned without fine-tuning** [@kaminski2023], **and these alignments outperform purely sequence-based but not structure-based methods** ([@llinareslpez2022], [@hamamsy2023]). This could be since the embeddings of aligned positions in related sequences tend to co-[[Clustering|cluster]] [@mcwhite2023]. Alignment quality can be further improved by normalization [@pantolini2022], which does not require PLM fine-tuning. [@ashrafzadeh2023] surmise that the distance matrices implied by these embeddings are more effective than the [[BLOSUM62]] matrix used by many sequence alignments by default.

## Details

TM-vec, a fine-tuned model, was found to be worse than non-fine-tuned models [@hamamsy2023].

To improve alignment quality using "normalization" (per [@pantolini2022]), all distances (for their paper, Euclidean distances are used) are computed and converted to Z-scores to normalize relative to other entries in the same column and row. This was shown to improve performance relative to using non-normalized/enhanced values for alignment calculation.

## Figures

![[MSA-and-embeddings-with-glycines-in-rec.png]]
*Ref [@mcwhite2023]*

![[Malidup.png]]
*Ref [@hamamsy2023]*

![[ProtTuker.png]]
*Ref [@pantolini2022]; EBA and EBA-plain refer to PLM-based alignment with and without normalization*

## See also

* [[Multiple sequence alignments]]
* [[PLMs learn family-specific protein contacts from sequence context windows of about 20-40 amino acids]]
