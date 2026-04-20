---
tags:
created: 2024-07-08T02:37:17
modified: "2026-04-20T07:46:00"
---

#### Summary

**For ML-based [[MD simulations|MD]] potentials, alpha carbon-only representations are sufficient to recapitulate the dynamics of small proteins** [@majewski2023; @doerr2021]. Models that use both alpha and beta carbons were found to be less stable than those using only alpha carbons [@doerr2021]. These potentials were calculated using [[Graph neural networks|graph neural networks]] with TorchMD.

#### Figures

![[Pasted-image-20240708082007.png]]

*Figure from [@doerr2021]*

#### See also

- [[Information about backbone atoms is lost when rebuilding full-atom protein models from alpha carbon trace alone]]
