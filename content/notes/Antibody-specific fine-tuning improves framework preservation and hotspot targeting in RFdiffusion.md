---
tags:
  - design/antibodies
  - training/fine-tuning
created: "2026-09-25"
modified: "2026-09-25"
---

#### Summary

**Antibody-specific fine-tuning improves preservation of supplied frameworks and targeting of specified antigen hotspots during RFdiffusion design** [@bennett2024]. The framework/hotspot ablation covers both [[notes/Nanobodies|VHHs]] and scFvs; it does not establish a universal need to fine-tune models for natural-antibody structure prediction.

#### Details

Framework sequence and pairwise structural information condition the generator while allowing the antibody's rigid-body placement relative to the antigen to change. Fine-tuning improves joint framework recovery and hotspot targeting in the tested design settings. Vanilla RFdiffusion can already recover a monomeric VHH framework accurately, so “required for framework modeling” is too broad.

#### Figures

![[rfdiffusion-antibody-framework-hotspot-ablation.png]]
*Framework and hotspot ablation from [@bennett2024], supplied in issue #901; Supplementary Figure 1 in the published version.*

#### See also

- [[notes/Framework region|Framework region]]
- [[Heavy-chain templates and self-distillation improve nanobody structure prediction]] — a different training intervention for structure prediction.
- [[Protein backbone diffusion models undersample loop-rich and alpha-beta domains and functional motifs]]
