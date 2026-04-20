---
tags:
  - fine-tuning
created: 2026-04-05T17:17:55
modified: "2026-04-20T08:16:13"
---
#### Summary
**Fine-tuning deep learning models leads to small differences in parameter values in L2 space** [^neyshabur2020]. The foundation model and fine-tuned model often occupy the same basin of the loss landscape. Output features of each layer were examined using centered kernel alignment.

#### Details
| models/layer | conv1 | layer 1 | layer 2 | layer 3 | layer 4 |
|---|---|---|---|---|---|
| P-T & P | 0.6225 | 0.4592 | 0.2896 | 0.1877 | 0.0453 |
| P-T & P-T | 0.6710 | 0.8230 | 0.6052 | 0.4089 | 0.1628 |
| P-T & RI-T | 0.0036 | 0.0011 | 0.0022 | 0.0003 | 0.0808 |
| RI-T & RI-T | 0.0016 | 0.0088 | 0.0004 | 0.0004 | 0.0424 |
*Ref [^neyshabur2020]*

#### See also
- [[Fine-tuning can be detrimental to performance]]
- [[Low-rank adaptation causes models to learn less and forget less]]
- [[Low-rank adaptation changes the magnitude, but not directionality, of matrix operations relative to fine-tuning]]

[^neyshabur2020]: Neyshabur et al. (2020) "What is being transferred in transfer learning?." NeurIPS. https://proceedings.neurips.cc/paper/2020/hash/0607f4c705595b911a4f3e7a127b44e0-Abstract.html
