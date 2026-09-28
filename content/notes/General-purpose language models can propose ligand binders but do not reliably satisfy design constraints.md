---
tags:
  - design/sequence-generation
  - evidence/design-validation
  - prediction/ligand-docking
created: "2026-09-15"
modified: "2026-09-25"
---

#### Summary

**General-purpose language models can propose experimentally active ligand-binding proteins from natural-language prompts, but the resulting proteins can deviate from the requested topology, binding motif, or oligomeric state** [@kim2026llmdesign]. Plausible verbal design rationales do not establish that those constraints were satisfied.

#### Details

The initial design models were ChatGPT 5 and its advanced-thinking variant, Claude Sonnet 4.5, and Gemini 2.5. Structure prediction and human filtering selected candidates for experimental testing.

| Design task | Experimentally tested | Reported binding hits |
| --- | ---: | ---: |
| Metal-binding proteins | 12 | 3 |
| PFOA binding, five-helix first round | 6 | 0 appreciable hits |
| PFOA binding, six-helix second round | 8 | 2 |

The PFOA redesign followed a human-proposed topology change and literature guidance. Its two hits showed ligand-dependent fluorine NMR broadening, but neither was monodisperse by size-exclusion chromatography.

[[ProteinMPNN]] or LigandMPNN redesign of selected backbones generally improved subsequent structure-prediction confidence. This is a computational comparison, not experimental evidence that a tool-augmented LLM produces better binders. Later models were used to critique sequences, not to repeat the initial experimental benchmark.

#### See also

- [[Protein structure prediction and design confidence metrics do not correlate with binding affinity]]
- [[De novo designed proteins (from language models) and naturally occurring proteins borrow heavily from other functionally similar sequences]]
- [[Protein-ligand co-folding]]
