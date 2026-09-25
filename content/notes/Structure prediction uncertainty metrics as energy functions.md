---
tags:
  - prediction/confidence
  - model-design/generative-models
created: "2026-03-06T12:45:58"
modified: "2026-09-25"
---
#### Summary
In protein [[notes/Structure prediction|structure prediction]], **uncertainty metrics can be repurposed as energy-like functions for ranking or optimizing candidate structures.** [[notes/AlphaFold2|AlphaFold]] without coevolutionary input ranks structural decoys with state-of-the-art accuracy [@roney2022], and [[notes/Diffusion models|diffusion]]-model scores can be interpreted as statistical potentials for structure ranking, mutation-effect prediction, and conformational sampling [@roney2025]. The analogy concerns relative ranking and sampling objectives, not calibrated thermodynamic free energy; raw confidence scores still need not predict [[notes/Stability and thermostability|stability]] or binding affinity.

#### Scoring supplied coordinates without denoising

TorchScore bypasses diffusion generation and evaluates supplied coordinates through the TorchFold confidence pathway, returning confidence measures without training a separate scoring network [@torchfold2026, Appendix C]. With the antibody–antigen checkpoint, its ipTM correlated with DockQ at Pearson 0.869 on pooled PDB55 candidates.

This is structural-quality scoring. It is distinct from [[Boltz-2 intermediate representations can predict protein-protein binding affinity|training an affinity predictor on internal representations]], and scores from different checkpoints need not share [[Different AlphaFold3 clones have differently calibrated confidence heads|the same calibration]]. A pooled candidate-level correlation also need not imply equally strong ranking within each target's ensemble.

#### Related notes
- [[Diffusion-based protein structure prediction methods double as energy methods comparable to traditional force fields]]
- [[Protein structure prediction and design metrics don't correlate with expression probability]]
- [[Confidence metrics for diffusion-based structure prediction methods can be improved with minimal changes to conditioning representations]]
- [[Including structure prediction confidence while training inverse folding improves sequence diversity but not sequence recovery]]
- [[Most ML quality metrics cannot effectively predict enzyme activity after controlling for similarity to native]]
- [[pLDDT correlates with number of homologous sequences provided during runtime]]
- [[Protein structure prediction and design confidence metrics do not correlate with binding affinity]]
- [[pLDDT and PAE inversely correlated with protein dynamics in dynamic naturally occurring proteins, but not de novo proteins]]
- [[pLDDT is inversely correlated with CDRH3 length]]
- [[Protein folding neural networks cannot predict protein stability]]
- [[Self-consistency perplexity is correlated with pLDDT]]
- [[AlphaFold3 ipTM can distinguish between antibody binders and nonbinders]]
- [[Inverse folding sequence perplexities correlate with Rosetta energies, forward folding TM-scores, and sequence recovery]]
- [[PAE weakly correlates with Ab-Ag binding]]
