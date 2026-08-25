---
tags:
  - diffusion-models/protein-design
  - protein-design/design
created: "2026-08-25"
modified: "2026-08-25T10:55:31"
---
#### Summary
**Low full-chain similarity can overstate the structural novelty of generated [[protein-backbone-design|protein backbones]] because locally alignable known domains remain common** [@xu2026retrieval]. Across eight diffusion and flow-matching generators, 80.2-98.2% of outputs contained at least one domain alignable to CATH S40 at an aligned-length TM threshold of 0.5; requiring every domain to match reduced the range to 28.4-87.6%. These retrieval rates establish local alignability, not that every matched domain was memorized during training. RetFold, a retrieval-only baseline, reached 96.0% any-domain and 83.8% all-domain retrieval at roughly two orders of magnitude lower computational cost.

#### Details

| Method | Any ($\tau = 0.5$) | All ($\tau = 0.5$) | Any ($\tau = 0.7$) | All ($\tau = 0.7$) |
| --- | ---: | ---: | ---: | ---: |
| RFDiffusion | 96.2 | 60.6 | 65.2 | 20.6 |
| FrameDiff | 89.4 | 47.8 | 30.2 | 10.0 |
| Chroma | 98.0 | 69.0 | 58.2 | 12.8 |
| FoldFlow | 83.2 | 28.4 | 37.2 | 7.2 |
| FrameFlow | 92.6 | 49.6 | 43.0 | 10.2 |
| ProtPardelle | 91.6 | 47.0 | 49.0 | 14.0 |
| BoltzGen | 80.2 | 64.4 | 67.8 | 51.4 |
| PXDesign | 98.2 | 87.6 | 94.4 | 82.0 |
| RetFold | 96.0 | 83.8 | 95.8 | 81.8 |

*Any- and all-domain retrieval rates (%); Table 1 from [@xu2026retrieval]*

#### Figures

![[domain-level-and-full-chain-protein-backbone-retrieval.png]]

*Figure 3 from [@xu2026retrieval]*

#### See also
- [[Protein backbone diffusion models undersample loop-rich and alpha-beta domains and functional motifs]]
- [[Nearly half of CATH domains do not pass designability filters used to evaluate protein backbone design performance]]
