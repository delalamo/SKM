---
tags:
  - protein-folding/misc
---

#### Summary

**For ML-based [[MD simulations|MD]] potentials, alpha carbon-only representations are sufficient to recapitulate the dynamics of small proteins** (Majewski et al 2023[^majewski2023], Doerr et al 2021[^doerr2021]). Models that use both alpha and beta carbons were found to be less stable than those using only alpha carbons (Doerr et al 2021[^doerr2021]). These potentials were calculated using [[Graph neural networks|graph neural networks]] with TorchMD.

#### Figures

![](/assets/Pasted-image-20240708082007.png)

*Figure from Doerr et al 2021[^doerr2021]*

#### See also

- [[Information about backbone atoms is lost when rebuilding full-atom protein models from alpha carbon trace alone]]

[^majewski2023]: Majewski et al. (2023) "Machine learning coarse-grained potentials of protein thermodynamics." *Nature Communications*. https://doi.org/10.1038/s41467-023-41343-1
[^doerr2021]: Doerr et al. (2021) "TorchMD: A Deep Learning Framework for Molecular Simulations." *Journal of Chemical Theory and Computation*. https://doi.org/10.1021/acs.jctc.0c01343
