---
tags:
  - diffusion-models/protein-design
  - protein-design/design
created: "2026-08-25"
modified: "2026-08-25T10:16:02"
---
#### Summary
**Low full-chain similarity can overstate the structural novelty of generated [[protein-backbone-design|protein backbones]] because locally alignable known domains remain common** [@xu2026retrieval]. Across eight diffusion and flow-matching generators, 80.2-98.2% of outputs contained at least one domain alignable to CATH S40 at an aligned-length TM threshold of 0.5; requiring every domain to match reduced the range to 28.4-87.6%. These retrieval rates establish local alignability, not that every matched domain was memorized during training. RetFold, a retrieval-only baseline, reached 96.0% any-domain and 83.8% all-domain retrieval at roughly two orders of magnitude lower computational cost.

#### See also
- [[Protein backbone diffusion models undersample loop-rich and alpha-beta domains and functional motifs]]
- [[Nearly half of CATH domains do not pass designability filters used to evaluate protein backbone design performance]]
