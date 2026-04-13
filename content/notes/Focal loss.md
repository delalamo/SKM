---
tags:
  - protein-folding/misc
created: "2024-05-15T10:13:01"
modified: "2026-04-11T07:41:30"
---
#### Summary
**Focal loss** is a type of loss function that downweighs well-predicted labels.

#### Details
Focal loss ($FL$) is defined by $FL(p_{i}) = - \alpha(1-p_{i})^{\gamma} \log(p_{i})$ where $\gamma$ is a user-picked modulating factor that decreases the gradient of easy examples as it increases, and $\alpha$ is a weight. A value of zero reverts to cross-entropy.

#### Figures
![[Pasted-image-20240515101039.png]]
*From https://medium.com/swlh/focal-loss-what-why-and-how-df6735f26616*

#### See also
- [[PLMs are biased toward germline antibodies]]
