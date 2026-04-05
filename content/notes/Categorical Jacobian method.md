---
tags:
  - protein-folding/misc
---
#### Summary
The **categorical Jacobian method** was developed by Zhang et al 2024[^zhang2024] to predict protein contacts using [[Protein language models]]. Unlike [[ESMFold]] and the [[ESM]] contact prediction head, it is entirely unsupervised and requires no training. It works for [[Transformer|transformers]] but not CNNs.

#### Details
For a sequence of length $L$ with $A$ possible tokens, the categorical Jacobian $J$ has shape $L \times A \times L \times A$. Each residue is mutated to all $A$ possible tokens, and the perturbation to output logits across all positions is recorded. From the authors:

> "Applying the same procedure to a Markov Random Field (MRF) or multivariate Gaussian (MG) model results in exactly returning the pairwise coupling tensor... yet in ESM-2, a small perturbation to the one-hot encoded input is insufficient to perturb the output. Increasing the step size improves contact map accuracy, and changing the actual category (amino acid type) results in the best contact accuracy."

#### Figures
![](/assets/Pasted-image-20240416123902.png)
*Figure from Zhang et al 2024[^zhang2024]*

#### Code
```python
def get_categorical_jacobian(seq):
    x, ln = alphabet.get_batch_converter()([("seq", seq)])[-1], len(seq)
    with torch.no_grad():
        f = lambda x: model(x)["logits"][..., 1:(ln+1), 4:24].cpu().numpy()
        fx = f(x.to(device))[0]
        x = torch.tile(x, [20, 1]).to(device)
        fx_h = np.zeros((ln, 20, ln, 20))
        for n in range(ln):
            x_h = torch.clone(x)
            x_h[:, n+1] = torch.arange(4, 24)
            fx_h[n] = f(x_h)
        return fx_h - fx
```

[^zhang2024]: Zhang et al. (2024) "Protein language models learn evolutionary statistics of interacting sequence motifs." *Proceedings of the National Academy of Sciences*. https://doi.org/10.1073/pnas.2406285121
