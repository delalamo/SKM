---
tags:
created: 2024-06-01T00:33:31
modified: "2026-04-21T05:01:15"
---
#### Summary
When training neural networks, **learning rate decay** is used to gradually lower the learning rate over a fixed training duration. Typically cosine decay is used, though this has the disadvantage of being carried out over a predefined duration that cannot easily be extended. [@hgele2024] found that [[Weight averaging]] can work in tandem with this but cannot replace it.

#### Figures
![[Pasted-image-20240601062539.png]]
*Ref [@hgele2024]*

#### Types
- Cosine decay
- Linear decay (or "trapezoidal" decay)
- Square root decay: $1-\sqrt{\frac{n-(N-N_{decay})}{n_{decay}}}$, with 5% of training steps dedicated to cooldown [@hgele2024]
- Schedule-free optimization
