---
title: Weight averaging
tags:
  - weight-averaging
---

**Weight averaging** refers to the averaging of different checkpoints of a single model during training.

#### Types
- **Stochastic weight averaging**: Averages the same model's weights at different points near the end of the training process, maintaining high-ish learning rates
- **Exponentially moving average**: Decreases the contribution of older states
- **Latest weight averaging**: Uses states from the end of an epoch

<!-- generated -->
