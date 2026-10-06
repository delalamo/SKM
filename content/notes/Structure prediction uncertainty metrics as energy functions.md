---
tags:
  - prediction/confidence
  - model-design/generative-models
created: "2026-03-06T12:45:58"
modified: "2026-10-05T20:01:20"
---
#### Summary
In protein [[notes/Structure prediction|structure prediction]], **uncertainty metrics can be repurposed as energy-like functions for ranking or optimizing candidate structures.** [[notes/AlphaFold2|AlphaFold]] without coevolutionary input ranks structural decoys with state-of-the-art accuracy [@roney2022], and [[notes/Diffusion models|diffusion]]-model scores can be interpreted as statistical potentials for structure ranking, mutation-effect prediction, and conformational sampling [@roney2025]. The analogy concerns relative ranking and sampling objectives, not calibrated thermodynamic free energy; raw confidence scores still need not predict [[notes/Stability and thermostability|stability]] or binding affinity.

Confidence modules from diffusion-based structure prediction methods can also score supplied structures while bypassing diffusion generation. AF3Score feeds input coordinates directly into the [[notes/AlphaFold3|AlphaFold3]] confidence head, allowing candidate structures to be evaluated without first refining them through the structure-generation module [@liu2025af3score].

AF3Score was evaluated on monomers, protein complexes, designed binders, fold-switching proteins, and protein–ligand complexes. In the authors' designed-binder screening benchmark, it outperformed comparator methods on eight of ten targets; combining it with AlphaFold2-derived methods increased the success rate from 15.2% to 31.6% [@liu2025af3score]. Its ability to score alternative folds also connects to the observation that [[Structure prediction methods undersample the conformational space they find to be high-confidence|predictors can assign high confidence to conformations they fail to generate]].

TorchScore similarly evaluates supplied coordinates through the TorchFold confidence pathway with the same model weights and no separately trained scoring network. With the antibody–antigen checkpoint, its [[notes/TM-score|ipTM]] correlated with [[DockQ]] at Pearson 0.869 on pooled PDB55 candidates [@torchfold2026, Appendix C].

These scores estimate structural quality. Their usefulness for ranking candidates or enriching binders does not establish [[Protein structure prediction and design confidence metrics do not correlate with binding affinity|general binding-affinity prediction]] or calibrated thermodynamic energies. [[Different AlphaFold3 clones have differently calibrated confidence heads|Calibration depends on the checkpoint]], and a pooled candidate-level correlation need not imply equally strong ranking within each target's ensemble.

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
