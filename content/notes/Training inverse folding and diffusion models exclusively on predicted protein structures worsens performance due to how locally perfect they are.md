---
tags:
  - diffusion-models/training
  - protein-design/training
created: "2026-03-21T17:43:50"
modified: "2026-04-20T07:46:00"
---
#### Summary
**Training machine learning models for either [[Inverse folding|inverse folding]] or [[Protein backbone design|protein backbone design]] via [[Diffusion models|diffusion]] exclusively on predicted models worsens performance** [@hsu2022; @su2023]. This was observed when training [[ESM-IF]] and [[Geometric Vector Perceptrons|GVP]] as well as when training using the (Evoformer) or the [[Hybrid sequence-structure models|hybrid sequence-structure method]] MIF-ST, but not (SaProt) (which uses tokens from the (Foldseek) alphabet). The latter study also looked at downstream performance and saw worse results. This was shown to be because predicted models are "too perfect" at a local level [@tan2025].

#### Details
[@huguet2024] found that training their diffusion model on both predicted models and experimental structures worsened designability and novelty relative to a model trained on experimental structures only.

[@lin2023generating] trained a version of the [[Protein backbone design|backbone]] [[Diffusion models|diffusion model]] GENIE on (AlphaFold2) models from SwissProt and found that although designability increased was greater than a model trained on the PDB, diversity was lower.

#### Figures

| | Exp only | AF2+Exp | AF2 only |
| --------------- | -------- | ------- | -------- |
| GVP-GNN | 5.43 | 6.06 | 6.52 |
| GVP-GNN-Large | 6.17 | 4.08 | 11.51 |
| GVP-Transformer | 6.44 | 4.01 | 10.95 |

*Table from [@hsu2022]*

![[Pasted-Graphic-4-1.png]]
*Figure from [@su2023]*

![[bafkreiawfxhyqc4grpfhhgjsyezzahtsrehsxzughw6vmpsuw2tqsazz64@jpeg.jpg]]
![[Pasted-image-20250722113536.png]]
*Figures from [@tan2025]*

#### See also
* [[Inverse folding models trained on all proteins outperform those trained on Abs for CDR prediction]]
* [[Adding noise while training non-Ab inverse folding models improves self-consistency while worsening sequence recovery]]
* [[Focused protein sequence libraries are poor training sets]]
* [[Computational models are less designable than experimental structures]]

21 March 2026: https://biomlzk.ghost.io/training-protein-structure-based-neural-networks-exclusively-on-predicted-protein-structures-worsens-performance-on-experimental-structures-due-to-how-locally-perfect-the-training-data-/
