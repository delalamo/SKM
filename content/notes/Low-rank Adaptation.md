---
tags:
  - protein-folding/misc
created: "2026-02-26T15:37:43"
modified: "2026-04-10T14:30:55"
---
#### Summary
**Low-rank adaptation** (LoRA) is an approach to speed up fine-tuning of neural networks, typically [[Transformer|transformers]] such as language models, originally proposed by [^hu2021]. In contrast with standard fine-tuning that updates all weights, LoRa updates only a few via: $W' = W + AB$ where $A$ and $B$ are two small weight matrices.

#### Details
- $AB$ is proposed to be mostly equivalent to $\delta W$ (the derivative of $W$ that is typically calculated during backdrop)
- $A$ and $B$ will have a shape $(W.shape[0], r)$ and $(r, W.shape[1])$ where $r$ is much less than $W.shape[0]$ or $W.shape[1]$
- In practice, the new $AB$ weight matrix can be kept separate from the original matrix $W$
- Two hyper parameters:
 - $r$: The rank of the LoRA matrices
 - $\alpha$: Scales the influence of the $AB$ matrices relative to the original weight matrix

#### Figures
\![[Weight-update-in-regular-finetuning.jpeg]]
*From https://magazine.sebastianraschka.com/p/lora-and-dora-from-scratch*

#### See also
- [[Low-rank adaptation changes the magnitude, but not directionality, of matrix operations relative to fine-tuning]]
- [[Low-rank adaptation causes models to learn less and forget less]]
- [[Different versions of low-rank adaptation have equivalent performance after controlling for learning rate]]
- [[Language models can be infused with structure via low-rank adapter layers]]

[^hu2021]: Hu et al. (2021) "LoRA: Low-Rank Adaptation of Large Language Models." https://doi.org/10.48550/ARXIV.2106.09685
