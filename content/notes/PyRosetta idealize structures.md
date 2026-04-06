---
tags:
  - protein-design/misc
created: "2025-07-14T13:01:20"
modified: "2026-04-05T23:14:54"
---
#### Summary
Idealize structures using [[Rosetta|PyRosetta]], only in regions with significant chain breaks. From the [[RosettaFold]] GitHub repository. Cartesian relax after this is recommended to optimize further.

#### Code
```python
# pyrosetta=2025.03
import pyrosetta

def idealize(pose: pyrosetta.Pose, cutoff: float = 50):
    mover = pyrosetta.rosetta.protocols.idealize.IdealizeMover()
    mover.fast(True)
    sfxn = pyrosetta.create_score_function('empty')
    sfxn.set_weight(pyrosetta.rosetta.core.scoring.cart_bonded, 1.0)
    to_idealize = pyrosetta.rosetta.utility.vector1_unsigned_long()
    emap = pose.energies()
    for r in range(1, pose.total_residues() + 1):
        if emap.residue_total_energy(r) > cutoff:
            to_idealize.append(r)
    mover.set_pos_list(to_idealize)
    mover.apply(pose)
    return pose
```
