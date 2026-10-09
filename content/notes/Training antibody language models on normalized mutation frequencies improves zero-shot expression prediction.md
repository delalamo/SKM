---
tags:
  - prediction/stability-expression
  - training/pretraining-and-scaling
  - antibodies/maturation
created: "2026-04-10T00:00:00"
modified: "2026-10-09T06:14:45"
---
#### Summary
**Training antibody [[notes/Protein language models|language models]] on normalized mutation frequencies improves zero-shot [[notes/Antibody developability|expression prediction]]** [@elife109644]. This approach relies on A) normalizing amino acid mutation frequencies by their likelihood in the codon table as well as substitution rates in non-transcribed regions of DNA, and B) germline-descendant substitution pairs observed in phylogenies derived from next-generation sequencing of antibody repertoires.

#### Figures
![[training-ablm-normalized-mutation-frequencies.png]]
*Ref [@elife109644]*

#### See also
- [[Random splits overestimate protein language model generalization on antibody expression prediction]]
