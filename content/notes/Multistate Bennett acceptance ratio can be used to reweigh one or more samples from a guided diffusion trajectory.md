---
tags:
  - diffusion-models/structure-prediction
  - diffusion-guidance/structure-prediction
created: "2026-03-11T09:23:58"
modified: "2026-04-11T06:15:31"
---

#### Summary

**Multistate Bennett acceptance ratio can be used to reweight one or more weighted samples from a [[Diffusion guidance|guided]] [[Diffusion models|diffusion]] trajectory** [^xie2026]. It does not work unless the samples are pre-weighted; [^xie2026] use the steering importance weights from Feynman-Kac guidance.

#### Details

Originally presented by [^shirts2008].

Given $K$ states, each with a potential energy function $u_k$, and $N_k$​ samples drawn from state $k$, MBAR finds the free energies $f_k$​ that satisfy the self-consistent equations:

$$\hat{f}_k = -\ln \sum_{n=1}^{N} \frac{\exp(-u_k(x_n))}{\sum_{l=1}^{K} N_l \exp(f_l - u_l(x_n))}​$$

These are solved iteratively. The solution is the **maximum likelihood estimator** for the free energies, which is a key theoretical strength — it's provably optimal given the data you have.

Once you have the $f_k$​, you can compute the **importance weight** $W_n$ for any sample $x_n$​ under a target distribution $t$:

$$W_n \propto \frac{\exp(-u_t(x_n))}{\sum_l N_l \exp(f_l - u_l(x_n))}​$$

[^xie2026]: Xie et al. (2026) "Enhanced Diffusion Sampling: Efficient Rare Event Sampling and Free Energy Calculation with Diffusion Models." https://doi.org/10.48550/ARXIV.2602.16634
[^shirts2008]: Shirts & Chodera (2008) "Statistically optimal analysis of samples from multiple equilibrium states." *The Journal of Chemical Physics*. https://doi.org/10.1063/1.2978177
