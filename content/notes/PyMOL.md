---
title: PyMOL
created: 2026-04-10T14:30:55
modified: "2026-04-21T07:28:09"
---

**PyMOL** is a modeling visualization program for proteins.

#### Shortcuts
###### Color a protein by b-factor (or [[plddt|pLDDT]])

```
spectrum b, minimum=0, maximum=100, selection=obj01
```

###### Color viridis-like

```
spectrum count, gold yellow green cyan slate violet
```

###### Change chain ID

```
select target_chain, object protein and chain B
alter target_chain, chain = 'Z'
sort
```

###### Morph PDBs

```
# requires that PDBs be aligned
morph morph_out1, model1, model2
morph morph_out2, model2, model3

# to combine multiple morphs
join_states combined_morph, morph_out1
join_states combined_morph, morph_out2
```
