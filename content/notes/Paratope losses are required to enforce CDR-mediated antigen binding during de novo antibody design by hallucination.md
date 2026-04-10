---
tags: antibodies/misc
created: "2025-12-19T11:25:57"
modified: "2026-04-10T14:30:55"
---

#### Summary

**Paratope losses are required to enforce [[Complementarity-determining regions|CDR]]-mediated antigen binding during [[De novo antibody design|de novo antibody design]] by [[Inversion of protein folding neural networks|hallucination]]** [^millefragoso2025].

#### Details

The exact paratope loss implementation:

$$
\mathcal{L}_{\text{paratope}} =
\frac{\mathcal{L}_{\text{CDR}}}{\mathcal{L}_{\text{framework}} - \lambda}
$$

where $\mathcal{L}_{\text{CDR}}$ and $\mathcal{L}_{\text{framework}}$ decrease as the respective regions gain more contacts with the antigen, and $\lambda$ is a user-defined parameter.

#### Figures

\![[Pasted-image-20251027120017.png]]

*Figure from [^millefragoso2025]*

#### See also

* [[Secondary structure losses are required to enforce CDR loopiness during de novo antibody design by hallucination]]

[^millefragoso2025]: Mille-Fragoso et al. (2025) "Efficient generation of epitope-targeted
                  de novo
                  antibodies with Germinal." https://doi.org/10.1101/2025.09.19.677421
