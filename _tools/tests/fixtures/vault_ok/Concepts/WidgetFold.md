---
type: concept
aliases: [Widget Fold]
introduced_by: ["[[alpha2020]]"]
topics: ["[[Widget loops]]"]
tags: [concept]
---

WidgetFold assigns each loop to the nearest [[Canonical loop|canonical loop]] by a distance over backbone dihedral angles:

$$
d(a, b) = \sum_i \left(1 - \cos(\phi^a_i - \phi^b_i)\right)
$$

Loops farther than a cutoff from every shape are left unassigned.
