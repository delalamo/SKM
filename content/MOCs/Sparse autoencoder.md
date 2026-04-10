---
title: Sparse autoencoder
tags:
  - sparse-autoencoder
created: "2026-04-05T23:36:09"
modified: "2026-04-10T14:30:55"
---

**Sparse autoencoders** are a type of deep learning model used in explainability research that attempt to recapitulate the activations of intermediate layers of [[Transformer|transformer]] models. Unlike other autoencoders (such as [[Variational autoencoders|VAEs]]), these usually have a larger embedding dimension than the input and output representations. This is counteracted with a training constraint that enforces sparsity. One famous example of this being used is for the "Golden Gate" version of Claude 3.

#### Details
In the context of [[Protein language models|protein language models]], the features extracted from intermediate layers [[Sparse autoencoder-derived features do not outperform PLM-derived embeddings for downstream prediction|do not outperform the embeddings from which they are derived on property prediction]].

#### Figures
\![[Original-Model-Activations.png]]
*Figure from https://adamkarvonen.github.io/*

#### See also
- [[Ordered SAEs are more steerable than top-k SAEs]]

#### Code
```python
import torch
import torch.nn as nn
# D = d_model, F = dictionary_size
# e.g. if d_model = 12288 and dictionary_size = 49152
# then model_activations_D.shape = (12288,) and encoder_DF.weight.shape = (12288, 49152)
class SparseAutoEncoder(nn.Module):
 """
 A one-layer autoencoder.
 """

 def __init__(
		 self,
		 activation_dim: int,
		 dict_size: int):
 super().__init__()
 self.activation_dim = activation_dim
 self.dict_size = dict_size
 self.encoder_DF = nn.Linear(activation_dim, dict_size, bias=True)
 self.decoder_FD = nn.Linear(dict_size, activation_dim, bias=True)

 def encode(
		 self,
		 model_activations_D: torch.Tensor) -> torch.Tensor:
 return nn.ReLU()(self.encoder_DF(model_activations_D))

 def decode(
		 self,
		 encoded_representation_F: torch.Tensor) -> torch.Tensor:
 return self.decoder_FD(encoded_representation_F)

 def forward_pass(
		 self,
		 model_activations_D: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
 encoded_representation_F = self.encode(model_activations_D)
 reconstructed_model_activations_D = self.decode(encoded_representation_F)
 return reconstructed_model_activations_D, encoded_representation_F

# B = batch size, D = d_model, F = dictionary_size
def calculate_loss(
		 autoencoder: SparseAutoEncoder,
		 model_activations_BD: torch.Tensor,
		 l1_coeffient: float) -> torch.Tensor:
 reconstructed_model_activations_BD, encoded_representation_BF = autoencoder.forward_pass(model_activations_BD)
 reconstruction_error_BD = (reconstructed_model_activations_BD - model_activations_BD).pow(2)
 reconstruction_error_B = einops.reduce(reconstruction_error_BD, 'B D -> B', 'sum')
 l2_loss = reconstruction_error_B.mean()
 l1_loss = l1_coefficient * encoded_representation_BF.sum()
 loss = l2_loss + l1_loss
 return loss
```

<!-- generated -->
