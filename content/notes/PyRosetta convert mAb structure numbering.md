---
tags:
  - antibodies/architecture
  - prediction/antibody-structure
created: 2025-07-14T12:54:40
modified: "2026-10-09T05:36:09"
---
#### Summary
Renumber [[tags/antibodies|antibody]] structures using [[Rosetta|PyRosetta]]. This example converts Chothia to IMGT numbering; see [[Antibody numbering]] for the scheme definitions, supported molecule types, and residue equivalences.

#### Code
```python
# pyrosetta=2025.03
import pyrosetta
from pyrosetta.rosetta.protocols import antibody

def convert_numbering(pose: pyrosetta.Pose):
 mover = antibody.AntibodyNumberingConverterMover()
 mover.set_scheme_conversion(
 antibody.AntibodyNumberingSchemeEnum.ChothiaScheme,
 antibody.AntibodyNumberingSchemeEnum.IMGT_Scheme)
 mover.apply(pose)
 return pose
```
