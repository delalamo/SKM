---
tags:
  - design/backbones
  - evidence/generalization
created: "2026-08-25"
modified: "2026-08-25T10:55:31"
---
#### Summary
**Diffusion- and flow matching-based [[notes/protein-backbone-design|protein backbone design]] methods show fold-level novelty by recycling memorized subdomain structures** [@xu2026retrieval].

#### Details
Across eight [[notes/diffusion-models|diffusion]] and [[Flow matching|flow-matching]] generators, 80.2-98.2% of outputs contained at least one domain alignable to CATH S40 at an aligned-length [[notes/tm-score|TM]] threshold of 0.5; requiring every domain to match reduced the range to 28.4-87.6%. These retrieval rates establish local alignability, not that every matched domain was memorized during training. RetFold, a retrieval-only baseline, reached 96.0% any-domain and 83.8% all-domain retrieval at roughly two orders of magnitude lower computational cost.

#### Figures

![[domain-level-and-full-chain-protein-backbone-retrieval.png]]

*Figure 3 from [@xu2026retrieval]*

#### See also
- [[Protein backbone diffusion models undersample loop-rich and alpha-beta domains and functional motifs]]
- [[Nearly half of CATH domains do not pass designability filters used to evaluate protein backbone design performance]]
