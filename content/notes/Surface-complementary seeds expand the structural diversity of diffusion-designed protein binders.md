---
tags:
  - design/binders
  - design/backbones
  - inference/conditioning
created: "2026-09-25"
modified: "2026-09-25"
---

#### Summary

**PDB-derived fragments selected for surface complementarity can guide diffusion toward more structurally diverse binders** [@britton2026]. Seed-guided RFdiffusion generated RelE binders with more target contacts and greater backbone diversity than unguided generation.

#### Details

The seeds supply complementary contact geometry for motif scaffolding, helping designs span the toxin's extended interaction surface. Screening 1,402 seed-guided designs identified functional binders. This validates the seeded designs, but does not by itself establish a higher experimental hit rate than an equally screened unguided control.

The result provides a possible route around [[Protein backbone diffusion models undersample loop-rich and alpha-beta domains and functional motifs|structural sampling biases]]. It broadens the sampled scaffolds without establishing why other generators favor [[Proteins designed by diffusion are more compact than those designed by hallucination|compact proteins]].

#### See also

- [[No one-size-fits-all best approach to motif scaffolding protein design]]
- [[Diffusion-based protein design methods undersample structural diversity in specific topologies]]
