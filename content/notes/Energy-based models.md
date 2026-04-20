---
title: Energy-based models
created: 2026-04-10T14:30:55
modified: "2026-04-17T06:40:29"
---

**Energy-based models** are statistical models or neural networks that attempt to learn the energy characterizing a distribution of data, rather than recovery of individual data points themselves. These are typically described as $p(A|B)=\frac{\exp \left(-E_{\theta}(A, B)/\beta \right)}{Z_{\theta,B}}$ where $\beta$ is the inverse temperature and $Z$ is a usually unknown partition function $\int_{\Omega} e^{-\beta E_{\theta}(A, B)}$. In the context of [[Structure prediction|protein structure prediction]], energy-based models are useful for learning the full conformational distribution, e.g., $p(str|seq)$.

#### Details

Some of these methods adapt [[Diffusion models|diffusion models]] by teaching the neural network $s_{\theta}(x,t)$ that normally learns to approximate the time-dependent score function $\nabla_{x} \log p_{t}(X)$ to instead directly approximate $- \nabla_{x} E_{\theta}(x,t)$.

ProteinEBM ([[10.64898__2025.12.09.693073|Roney et al 2025]]) trained using a denoising score matching framework with the following loss:

$$
\frac{1}{N_r} \bigg\| -\nabla_x E_\theta(x_t, s, t) - \frac{x_t - \sqrt{\beta_t}x_0}{1-\beta_t}\bigg\|^2
$$

$N_{r}$: Number of residues
$x_{t}=\mathcal{N}(\sqrt{\beta_{t}}x_{0}, 1-\beta_{t})$: Noised version of input $x_{0}$


