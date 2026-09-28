---
tags:
  - design/backbones
  - inference/conditioning
created: "2026-09-25"
modified: "2026-09-25"
---

#### Summary

**Conditioning on pairwise distances between motif atoms can preserve their relative geometry while allowing their placement to change jointly with a designed scaffold** [@bai2026]. The motif need not be fixed to absolute Cartesian coordinates.

#### Details

PANDA applies this conditioning within an all-atom denoising architecture. Its stated design goal is to retain functional-atom geometry while permitting the surrounding protein and motif placement to be generated together. This is a constraint on relative geometry, not a measurement of catalytic activity.

The strategy is another choice within [[No one-size-fits-all best approach to motif scaffolding protein design|motif-scaffolding design]], where comparative success depends on the motif and benchmark. It does not establish that distance conditioning is universally preferable to fixed-coordinate constraints.

#### See also

- [[notes/Protein backbone design|Protein backbone design]]
- [[notes/Diffusion models|Diffusion models]]
