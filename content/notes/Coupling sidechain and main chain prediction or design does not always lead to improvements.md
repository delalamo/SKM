---
tags:
  - protein-structure-prediction/limitations
  - protein-backbone-design
  - citation-fix
created: "2025-03-03T00:28:27"
modified: "2026-04-21T07:03:26"
---

#### Summary
**Coupling backbone and side chain prediction or design does not necessarily lead to better performance** [@chu2023; @vangaru2025; @didi2026a]. Methods from early 2026 found strong performance in binder design when combining [[tags/protein-backbone-design|backbone design]] and [[tags/inverse-folding|inverse folding]], and degraded performance when backbones were redesigned with [[ProteinMPNN]] afterwards. However, prior work found the opposite conclusion in protein backbone design [@chu2023; @vangaru2025]. In parricular, [[tags/alphafold3|Alphafold3]] was found to be worse than [[tags/alphafold2|Alphafold2]] at sidechain packing [@vangaru2025].
