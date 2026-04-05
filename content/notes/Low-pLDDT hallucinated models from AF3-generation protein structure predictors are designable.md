---
tags:
  - protein-design/misc
---
#### Summary
 **Low-[[pLDDT]] hallucinations from [[AlphaFold|AF3]]-generation methods are designable** (Cho et al 2025[^cho2025]). Out of the various methods tested, Boltz showed the best designability, with poly-"X" sequences adopting designable backbones. Design benefit from multiple iterations. 

#### See also
* [[Protein backbone design]]

#### References
```base
filters:
  and:
    - this.file.hasLink(file.file)
    - file.infolder("Sorted_notes/Raw_data/Paper_notes/")
views:
  - type: list
    name: List
    order:
      - Title
      - Year
      - file.name
    sort: []

```

[^cho2025]: Cho et al. (2025) "Protein Hunter: exploiting structure hallucination within diffusion for protein design." https://doi.org/10.1101/2025.10.10.681530
