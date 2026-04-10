---
title: Normalizing flows
tags:
  - normalizing-flows
created: "2026-04-10T14:30:55"
modified: "2026-04-10T14:30:55"
---

**Normalizing flows** ($f$ below) are a type of invertible deep learning framework capable of generating samples from a target distribution. It maps configuration $\textbf{x}$ drawn from a prior distribution $q(\textbf{x})$ to a target distribution $q'(\textbf{x})$.

#### Details
Since $f$ is invertible, the output probability distribution can be mapped as:
$$q'(\textbf{x}') = q(\textbf{x})|\det J_{f}(\textbf{x})|^{-1}$$
where $\det J_{f}$ is the determinant of the Jacobian of $f$ and $|\det J_{f}(\textbf{x})|^{-1} = |\det J_{f^{-1}}(\textbf{x'})|$

The entirety of this note liberally cites from [[10.1021__acs.jpclett.2c03327|Invernizzi et al 2022]].

#### Applications
- They have been used in conjunction with [[Replica-exchange molecular dynamics]] ([[10.1021__acs.jpclett.2c03327|Invernizzi et al 2022]])
- They have been used for [[Structure prediction#Conformational sampling methods|conformational sampling]] via fine-tuned [[AlphaFold|AlphaFold2]] and [[ESMFold]] ([[10.48550__ARXIV.2308.16713|Jing et al 2023]])

<!-- generated -->
