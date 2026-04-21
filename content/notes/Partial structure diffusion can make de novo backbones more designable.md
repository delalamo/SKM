---
tags:
  - diffusion-models/protein-design
  - protein-design/design
created: "2024-05-30T05:30:22"
modified: "2026-04-21T05:01:15"
---

#### Summary

**Partial [[Protein backbone design#Diffusion|structure diffusion]] can improve the designability of *de novo* designed backbones.**

#### Details

Partial RF-diffusion was applied to [[Chroma]] designs, followed by sequence design using [[ProteinMPNN]] and refolding with [[ESMFold]] (see below). Sequence design on out-of-the-box Chroma designs led to poor refolding rates, but partial diffusion prior to sequence design rescued those designs.

#### Figures

![[Pasted-image-20231119134803.png]]

*Ref https://bsky.app/profile/sokrypton.org/post/3keibpabwtd24*

#### See also

* [[Protein backbone design]]
