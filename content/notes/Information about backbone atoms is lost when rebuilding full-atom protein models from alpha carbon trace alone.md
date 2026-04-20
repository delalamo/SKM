---
tags:
created: 2024-07-15T02:51:15
modified: "2026-04-20T10:13:23"
---

#### Summary

Backbone information is lost when coarse-grained models are rebuilt using only alpha carbons. [^heo2023] found that the N-C peptide bond tended to have 3x larger errors when rebuilt alpha carbons compared to when they are rebuilt from experimental density. CA-only ProteinMPNN showed a consistent 10% drop in sequence recovery compared to the default program, implying that it was unable to recover information provided by the explicit inclusion of other backbone atoms.

#### See also

* [[Alpha carbon-only representations are sufficient for ML force fields]]

[^heo2023]: Heo & Feig (2023) "One particle per residue is sufficient to describe all-atom protein structures." https://doi.org/10.1101/2023.05.22.541652
