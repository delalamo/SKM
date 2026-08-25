---
tags:
  - affinity-maturation
  - antibody-antigen-interactions/binding-affinity
created: 2024-11-14T02:47:10
modified: "2026-08-25T13:38:32"
---
#### Summary
**[[thermostability|Stabilization]] can improve the [[Antibody-antigen binding affinity prediction|affinity]] of [[antibodies|antibodies]] and [[Nanobodies|nanobodies]], but the relationship between stability and affinity is non-monotonic.** For antibodies, [@hie2023; @shanker2024] improved affinity using [[protein-language-models|protein language models]] and [[inverse-folding|inverse-folding models]], respectively, as evidenced by mutations at [[Framework region|framework]] residues. For nanobodies, [@ketaren2023] targeted residues in [[Framework region|FR3]] using what they call a "stabilization code".

#### Details

In S1-RBD-14, the destabilizing E89K substitution increased affinity from $K_D = 25$ nM to $0.3$ nM, while further stabilization reduced binding [@ketaren2023]. Stabilization can therefore improve affinity from some starting points without making maximal stability the optimum.

#### Figures
![[Pasted-image-20231023071242.png]]
*Ref [@ketaren2023] — teal and purple are the non-stabilized and stabilized nanobodies, respectively*

#### See also
- [[Stability-activity trade-off during enzyme design and evolution is highly local and not global]]
- [[Mutations that give rise to new functions are not more destabilizing than mutations in general]]
- [[Conformational entropy in antibodies is inversely proportional to antigen affinity]]
