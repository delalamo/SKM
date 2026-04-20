---
tags:
created: 2025-07-14T12:54:40
modified: "2026-04-20T10:13:23"
---
#### Summary
Renumber [[Antibodies|antibody]] structures using [[Rosetta|PyRosetta]].

#### Code
```python
# pyrosetta=2025.03
import pyrosetta
from pyrosetta.rosetta.protocols import antibody

def convert_numbering(pose: pyrosetta.Pose):
 mover = antibody.AntibodyNumberingConverterMover()
 mover.set_scheme_conversion(
   antibody.AntibodyNumberingSchemeEnum.IMGT_Scheme,
   antibody.AntibodyNumberingSchemeEnum.ChothiaScheme)
 mover.apply(pose)
 return pose
```
