---
tags:
  - low-rank-adaptation
created: 2024-05-20T04:20:58
modified: "2026-04-21T05:01:15"
---
#### Summary
**Weight-decomposed low-rank adaptation** (abbreviated DoRA) is a modification of [[Low-rank Adaptation]] introduced by [@liu2024dora] that first decomposes the modified weights into a directional matrix and a magnitude vector. For a constant rank, this adds slightly more parameters, but the authors found that rank can be halved relative to DoRA without any issue and that it made the method more robust in general.

#### Code
```python
class LinearWithDoRAMerged(nn.Module):

 def __init__(self, linear, rank, alpha):
 super().__init__()
 self.linear = linear
 self.lora = LoRALayer(
 linear.in_features, linear.out_features, rank, alpha
 )
 # dynamic normalization
 self.m = nn.Parameter(
 self.linear.weight.norm(p=2, dim=0, keepdim=True))

 # Code loosely inspired by
 # https://github.com/catid/dora/blob/main/dora.py

 def forward(self, x):
 lora = self.lora.A @ self.lora.B
 numerator = self.linear.weight + self.lora.alpha*lora.T
 denominator = numerator.norm(p=2, dim=0, keepdim=True)
 directional_component = numerator / denominator
 new_weight = self.m * directional_component
 return F.linear(x, new_weight, self.linear.bias)
```
*Code from https://magazine.sebastianraschka.com/p/lora-and-dora-from-scratch*

#### Figures
![[Pasted-image-20240520090643.png]]
*Ref https://magazine.sebastianraschka.com/p/lora-and-dora-from-scratch*
