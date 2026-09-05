---
tags:
  - design/backbones
  - design/sequence-generation
created: "2025-03-03T00:28:27"
modified: "2026-04-21T07:28:09"
review:
  - "citation-fix"
---

#### Summary
**Coupling backbone and side chain prediction or design does not necessarily lead to better performance** [@chu2023; @vangaru2025; @didi2026a]. Methods from early 2026 found strong performance in binder design when combining [[notes/protein-backbone-design|backbone design]] and [[notes/inverse-folding|inverse folding]], and degraded performance when backbones were redesigned with [[ProteinMPNN]] afterwards. However, prior work found the opposite conclusion in protein backbone design [@chu2023; @vangaru2025]. In parricular, [[notes/alphafold3|Alphafold3]] was found to be worse than [[notes/alphafold2|Alphafold2]] at sidechain packing [@vangaru2025].
