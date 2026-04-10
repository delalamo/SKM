---
tags:
  - protein-folding/misc
  - alphafold3
created: "2026-04-05T17:34:36"
modified: "2026-04-10T10:46:24"
---

#### Summary

Flow matching and diffusion perform comparably for biomolecular structure prediction ([10.48550__ARXIV.2507.11839|Gong et al 2025]).

#### Figures

| Model / Domain | Prot-Prot | Lig-Prot | DNA-Prot | RNA-Prot | Intra-Prot | Complex LDDT |
|---|---|---|---|---|---|---|
| Protenix | 0.501 | 0.650 | 0.593 | 0.363 | 0.844 | 0.820 |
| PTX-Mini | 0.490 | 0.622 | 0.584 | 0.339 | 0.818 | 0.802 |
| PTX-Mini-Flow | 0.488 | 0.619 | 0.596 | 0.348 | 0.814 | 0.797 |
| PTX-Mini-ESM | 0.408 | 0.568 | 0.602 | 0.294 | 0.792 | 0.775 |
| PTX-Mini-ESM-Flow | 0.405 | 0.577 | 0.585 | 0.297 | 0.787 | 0.772 |
| Protenix-Tiny | 0.428 | 0.594 | 0.567 | 0.338 | 0.798 | 0.783 |
| PTX-Tiny-Flow | 0.422 | 0.594 | 0.569 | 0.338 | 0.806 | 0.780 |
*Figure from [10.48550__ARXIV.2507.11839|Gong et al 2025]*
