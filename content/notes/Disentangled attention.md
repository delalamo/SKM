---
tags:
  - protein-folding/misc
created: "2024-05-17T17:12:12"
modified: "2026-04-05T23:14:54"
---
#### Summary
Disentangled attention is an alternative way to represent position in encoder-type [[Transformer|transformers]].

#### Details
- Disentangled attention splits word info and position info. This leads to four types of attention, though they don't use position-to-position attention
- Final attention matrix adds these together
- New K Q matrices for position vectors
- P vector is not changed, but the initial assignment matrix is learned
- Absolute position encodings still required, and added in the last transformer layer - shown to work better
- The combination is what gives them the performance boost
