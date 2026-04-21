---
title: Flow matching
created: 2026-04-10T14:30:55
modified: "2026-04-21T07:03:26"
---

**Flow matching** is a generative AI approach that builds upon [[tags/diffusion-models|diffusion]] to denoise Gaussian noise into a complex distribution of interest. In contrast with diffusion, flow matching learns a velocity operation to push samples along a path from a (usually) normal distribution to an arbitrarily complex distribution.

#### Details

Flow matching uses learned velocity operations $v_{\theta}(x_{t}, t)$ to convert a set of normally distributed noise $p_0$ to a data distribution $p_D$. The generative process proceeds by stepwise integration of the ordinary differential equation: $dx_{t} = v_{\theta}(x_{t}, t)dt$.

During training, the data distribution consists of $x \sim p_{D}$ and noise samples $\epsilon \sim N(0, \mathbf{I})$. Training data at time point $t$ is just a linear combination of ground truth and noise $x_{t}=tx + \epsilon*(1-t)$. The network being trained tries to reproduce this velocity and movement. For example, [[SimpleFold]] uses L2 regression: $\ell_{\mathrm{FM}}= \mathbb{E}_{x,s,\epsilon,t} \left[\frac{1}{N_a} \left\| v_{\theta}(x_t, s, t) - (x - \epsilon) \right\|^2\right]$.
