---
tags:
  - protein-design/misc
created: "2025-07-14T13:08:01"
modified: "2026-04-05T23:36:09"
---
#### Summary
Convert between a [[Rosetta|PyRosetta]] pose object and a PDB string. Useful to avoid unnecessary file I/O.

#### Code
```python
# pyrosetta=2025.03
import pyrosetta
from pyrosetta.rosetta import core

def pose_to_string(pose):
 mover = core.io.pose_to_sfr.PoseToStructFileConverter()
 mover.init_from_pose(pose)
 return core.io.pdb.create_pdb_contents_from_sfr(mover.sfr())

def string_to_pose(pdbstring):
 pose = pyrosetta.Pose()
 core.import_post.pose_from_pdbstring(pose, pdbstring)
 return pose
```
