---
tags:
  - protein-folding/misc
created: "2024-07-15T02:51:15"
modified: "2026-04-05T23:14:54"
---

#### Summary

Backbone information is lost when coarse-grained models are rebuilt using only alpha carbons. [10.1101__2023.05.22.541652|Heo and Feig 2023] found that the N-C peptide bond tended to have 3x larger errors when rebuilt alpha carbons compared to when they are rebuilt from experimental density. CA-only ProteinMPNN showed a consistent 10% drop in sequence recovery compared to the default program, implying that it was unable to recover information provided by the explicit inclusion of other backbone atoms.

#### See also

* [[Alpha carbon-only representations are sufficient for ML force fields]]
